import websockets
import asyncio
from threading import Lock, Thread
import os
from pydantic import BaseModel, ValidationError
from typing import Literal, Optional
import json
import requests
import datetime
import re
from dotenv import load_dotenv

from . import config

configs_read = False


def load_environment() -> None:
    """
    Load environment variables from a .env file if it exists.
    Sets the following config object variables:
    - LOCAL_DEV
    - LOCAL_CONFIGS

    """
    global configs_read

    if configs_read:
        return
    env_filename = os.path.join(os.getcwd(), ".env")
    if os.path.isfile(env_filename):
        load_dotenv(os.path.join(os.getcwd(), ".env"), override=True)
        config.LOCAL_DEV = True

    if os.environ.get("CONFIDENTIAL_MIND_LOCAL_CONFIG") == "True":
        config.LOCAL_CONFIGS = True

    configs_read = True
    print(
        f"Done loading environment configs: \n \
        LOCAL_DEV: {config.LOCAL_DEV} \n \
        LOCAL_CONFIGS: {config.LOCAL_CONFIGS}"
    )


def get_api_parameters(config_id: str) -> tuple[str, Optional[str]]:
    """
    Construct and return the URL associated with a given configuration ID based on its stack ID and type. In case of .env file values from the file are used.
    It handles different environments, such as local development and production.

    Args:
        config_id (str): The identifier for the configuration.

    Returns:
        tuple: A tuple containing the base URL (str) and a header dictionary with api-key (dict).
               A dictionary for request headers in the format {"X-API-Key": api-key-value}. The API key is only used in local development environments.
    """
    load_environment()
    if config.LOCAL_DEV:
        url_base = os.environ.get(f"{config_id}_URL", None)
        # remove the trailing / if it exists with regex
        if url_base is not None:
            url_base = re.sub(r"/$", "", url_base)
        apikey = os.environ.get(f"{config_id}_APIKEY", None)
        headers = {}
        # check that the api key is valid uuid v4 if it exists
        if apikey is not None:
            try:
                if not re.match(
                    r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$", apikey
                ):
                    raise ValueError
            except ValueError:
                raise ValueError(f"API key for {config_id} is not the right format")
            headers = {"Authorization": f"Bearer {apikey}"}
    else:
        configManager = ConfigManager()
        url_base = configManager.getUrlForConnector(config_id)
        headers = {}  # not used

    return (url_base, headers)


class ConnectorSchema(BaseModel):
    """
    A schema representing a connector. A connector connects two services running inside the stack.

    Attributes:
        type (Literal["llm", "bucket", "database", "api"]): The type of the service to be connected.
        label (str): Label to be shown in admin UI.
        config_id (int): Id that can be used in code to create connection class.
        stack_id (str): The unique identifier of the resource.
    """

    type: Literal["llm", "bucket", "database", "api"]
    label: str
    config_id: str
    stack_id: Optional[str] = None


class ConnectorsDBSchema(BaseModel):
    """A schema encapsulating a list of connectors."""

    connectors: list[ConnectorSchema]


class ConfigPatch(BaseModel):
    # TODO should this be optional?
    config: Optional[dict] = None
    connectors: Optional[ConnectorsDBSchema] = None
    config_schema: Optional[dict] = None
    deployment_state: Literal["deployed"] = "deployed"


class SingletonClass(object):
    _lock = Lock()

    def __new__(cls):
        # two checks are on purpose, check-lock-check pattern
        if not hasattr(cls, "instance"):
            with cls._lock:
                if not hasattr(cls, "instance"):
                    print("Creating new instance")
                    cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance

    # TODO come up with way to check if instance is initialized


# Singleton class for managing the configuration of the application
class ConfigManager(SingletonClass):
    """
    The ConfigManager class handles configuration management between the application and the server,
    including fetching and updating configurations. It uses websockets for real-time updates
    and HTTP requests for initial fetches or patches to the configuration manager.

    Attributes:
        __manager_url (str): The URL of the configuration manager.
        __config_model (BaseModel): The model representing the app config schema.
        __lock (RLock): A lock used for thread-safe operations on configurations.
        __initialized (bool): A flag indicating whether the manager is initialized.
        __connectors (list[ConnectorSchema]): Current list of connectors managed by the application.
        __config (BaseToolConfig | None): The current configuration object.
    """

    def init_manager(
        self,
        config_model: Optional[BaseModel],
        connectors: Optional[list[ConnectorSchema]] = None,
    ):
        """
        Initializes the configuration manager. This method should be called before any other operations
        to ensure that configurations are properly fetched and initialized.

        Args:
            config_model (BaseModel, optional): The app config model.
            connectors (list[ConnectorSchema], optional):  List of connectors the app may use.
        """
        # TODO should initialized be a state with initalizing variable if multiple FEs are open
        # TODO this is most likely issue only for local development with multiple frontends open
        print("Initializing config manager")
        try:
            # TODO this should use lock?
            if self.__initialized:
                print("Config manager already initialized")
                return
        except AttributeError:
            # Setting initiliazed to True immediadly to prevent multiple init calls
            self.__initialized = True

        # initialize the environment variables
        load_environment()
        # Always use env variable if it exists, prevents accidental use of old id
        # TODO should we remove the ID parameter?
        self.__id = os.environ.get("SERVICE_NAME")
        self.__manager_url = None
        self.__realtime_url = None

        # id is needed if we don't use local configs
        assert not (
            self.__id is None and config.LOCAL_CONFIGS is False
        ), "Service name (id) must be set in env variable SERVICE_NAME if not using local configs"

        if config.LOCAL_DEV:
            # try to read from env variables
            # TODO move these to environment initialization?
            if os.environ.get("MANAGER_URL") is not None:
                print("Using manager url from env")
                self.__manager_url = (
                    os.environ.get("MANAGER_URL") + f"/internal/{self.__id}"
                )
            if os.environ.get("REALTIME_URL") is not None:
                print("Using realtime url from env")
                self.__realtime_url = (
                    os.environ.get("REALTIME_URL") + f"/internal/{self.__id}"
                )

        # if not in local dev, use  the default urls
        if self.__manager_url is None:
            self.__manager_url = f"http://manager.api-services.svc.cluster.local:8080/internal/{self.__id}"
        if self.__realtime_url is None:
            self.__realtime_url = f"ws://realtime.api-services.svc.cluster.local:8080/internal/{self.__id}"
        self.__lock = Lock()

        self.__config_model = config_model
        # TODO should connectors be defaulted to empty array in sql
        self.__connectors = None
        self.__config = None

        if config.LOCAL_CONFIGS:
            if connectors is None:
                temp_connectors = None
            else:
                temp_connectors = ConnectorsDBSchema(connectors=connectors)

            if config_model is None:
                temp_model = None
            else:
                temp_model = config_model.model_dump()

            self.__set_configs({"config": temp_model, "connectors": temp_connectors})
        else:
            # Fetch initial config
            self.__fetch_config(initial_request=True)

            # TODO call update config here
            self.__update_config(config_model, connectors)

            # Fetch updated configs
            self.__fetch_config()

        # After this we should have all the configs, error if not?
        # TODO check if config is None still?

        self.__close_sockets = False

        # Create a thread and loop for websocket
        # Loop is for using asyncio in the thread (required for the websockets library)
        # Daemon thread is automatically closed when main thread is closed
        if not config.LOCAL_CONFIGS:
            loop = asyncio.new_event_loop()
            thread = Thread(target=self.__start_loop, args=(loop,), daemon=True)
            thread.start()
            asyncio.run_coroutine_threadsafe(self.__run_websocket_for_ever(), loop)

        print("setting initliazed")
        self.__initialized = True

    # Wrapper for websocket thread
    def __start_loop(self, loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    # Protect so that can be running only once
    async def __run_websocket_for_ever(self):
        print("Starting websocket connection")
        # TODO do we want to wait for succesful connection before letting the application start?
        sleep = 0
        while not self.__close_sockets:
            try:
                # TODO should we fetch configs separately if websocket fails to catch missed notifications
                # max sleep time is 5 seconds
                if sleep < 5:
                    sleep += 1

                print(f"{datetime.datetime.now()} - Starting websocket connection")
                async with websockets.connect(self.__realtime_url) as websocket:
                    # Reset sleep time after succesful connection
                    sleep = 0
                    print(f"{datetime.datetime.now()} - New websocket connection")
                    # Process messages received on the connection.
                    async for message in websocket:
                        # TODO test only connector patch from websocket, does it have config in addition to connectors?
                        parsed = json.loads(message)
                        configs = parsed["payload"]
                        self.__set_configs(configs)

            except websockets.ConnectionClosed as e:
                print(
                    f"{datetime.datetime.now()} - Exception from websocket connection closed"
                )
                print(e)
                await asyncio.sleep(sleep)
                continue
            except ConnectionRefusedError as e:
                print(
                    f"{datetime.datetime.now()} - ConnectionRefused, likely the server is not running"
                )
                print(e)
                await asyncio.sleep(sleep)
                continue
            except Exception as e:
                print(f"{datetime.datetime.now()} - Exception from websocket")
                print(e)
                await asyncio.sleep(sleep)
                continue
        print(f"{datetime.datetime.now()} - Exited websocket setup")

    # This is blocking request on purpose!
    def __fetch_config(self, initial_request=False):
        # TODO for local development it is possible to get non-entry case
        response = requests.get(self.__manager_url)
        self.__set_configs(response.json(), initial_request)

    def __set_configs(self, json_configs, initial_request=False):
        try:
            # print(json_configs)
            if initial_request:
                config = json_configs["config"]
                config_schema = json_configs["config_schema"]
                if config is None and config_schema is None:
                    print("No config or config schema found, skipping")
                    return
            # some apps don't have connectors
            if json_configs["connectors"] is not None:
                connectors = ConnectorsDBSchema.model_validate(
                    json_configs["connectors"]
                )
            else:
                connectors = None
            if json_configs["config"] is not None:
                config = self.__config_model.model_validate(json_configs["config"])
            else:
                config = None
            config = self.__config_model.model_validate(json_configs["config"])
        except (ValidationError, ValueError) as e:
            print("Failed to validate configs")
            print(e)
            return
        # lock makes sure that websocket thread and db funcs dont run at the same time
        with self.__lock:
            if connectors is not None:
                self.__connectors = connectors.connectors
                print("Succesfully set connectors")
            if config is not None:
                self.__config = config
                print("Succesfully set configs")

    def __update_config(
        self, config_model: BaseModel, connectors: list[ConnectorSchema]
    ):
        update_body = ConfigPatch()

        # Merge existing connectors with possible new ones
        if connectors is not None:
            update_body.connectors = ConnectorsDBSchema(connectors=connectors)

        # if there is no schema and configs. Write them
        if self.__config is None and config_model is not None:
            update_body.config = config_model.model_dump()
            update_body.config_schema = config_model.model_json_schema()

        response = requests.patch(self.__manager_url, json=update_body.model_dump())
        print(response.status_code)
        # response is only status ok, not object

    @property
    def config(self):
        """Get the config object for reading values."""
        if self.__initialized is False:
            print("Config is not set yet, did you run init_manager?")
        return self.__config

    @property
    def connectors(self):
        """Get the connectors list."""
        if self.__initialized is False:
            print("Connectors are not set yet, did you run init_manager?")
        return self.__connectors

    def getStackIdForConnector(self, config_id):
        """
        Return the stack ID associated with a given configuration ID.

        Args:
            config_id (int): The configuration ID to find the stack ID for.

        Returns:
            str | None: The stack ID if found, otherwise None.
        """
        connector: ConnectorSchema
        for connector in self.__connectors:
            if connector.config_id == config_id:
                return connector.stack_id
        return None

    def getNamespaceForConnector(self, config_id):
        """
        Determine the namespace associated with a given configuration ID based on its type.

        Args:
            config_id (int): The configuration ID to find the namespace for.

        Returns:
            str | None: The namespace if found, otherwise None.
        """
        connector: ConnectorSchema
        for connector in self.__connectors:
            if connector.config_id == config_id:
                if connector.type == "bucket":
                    return "rook-ceph"
                elif connector.type == "database":
                    return "databases"
                else:
                    return "api-services"
        return None

    def getUrlForConnector(self, config_id):
        # TODO: update example with OpenAI 1.0.0 client API.
        """
        Construct and return the URL associated with a given configuration ID based on its stack ID and type.

        Args:
            config_id (int): The configuration ID to find the URL for.

        Returns:
            str | None: The constructed URL if valid information is available, otherwise None.

        Example:
            configManager = ConfigManager()
            url_base = configManager.getUrlForConnector(LLM_CONFIG_ID)
            if LOCAL_DEV:
                url_base = "http://localhost:8083"
            llm_service = OpenAI(
                model="gpt-3.5-turbo",
                api_base=url_base + "/v1",
                api_key="dummy_key",
                use_chat_completions=True,
                timeout=6000,
            )
        """
        stack_id = self.getStackIdForConnector(config_id)
        if stack_id is None:
            return None
        namespace = self.getNamespaceForConnector(config_id)
        if namespace is None:
            return None

        if namespace == "databases":
            return f"{stack_id}-rw.{namespace}.svc.cluster.local"
        # TODO change this to new url format
        return f"http://{stack_id}.{namespace}.svc.cluster.local:8080"


class BaseToolConfig(BaseModel):
    name: str = "undefined"
    type: Literal["undefined"] = "undefined"
