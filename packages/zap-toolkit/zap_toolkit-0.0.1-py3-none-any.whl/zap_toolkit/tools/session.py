from pydantic import model_validator, BaseModel, Field
import logging
from typing import Any, Dict, Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from zapv2 import ZAPv2

logger = logging.getLogger(__name__)


class SessionInitToolInput(BaseModel):
    """Input for the ZAP API session management tools."""

    session_name: str = Field(
        description="The name of the session."
        )


class SessionInitTool(BaseTool):
    """Tool that initializes a session in ZAP API.
    """

    zap_api_key: str = ""  #: :meta private:
    zap_api_endpoint_http: str = ""  #: :meta private:
    zap_api_endpoint_https: str = ""  #: :meta private:

    name: str = "zap_init_session_tool"
    description: str = (
        "A tool to initialize a session in ZAP API. "
        "Useful for when you are engaging a target and want to contain "
        "all the subsequent tool results in a single session. "
        "Input should be a name of a session."
    )

    args_schema: Type[BaseModel] = SessionInitToolInput

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that api key and endpoint information exists in environment."""

        values["zap_api_key"] = get_from_dict_or_env(
            values, "zap_api_key", "ZAP_API_KEY"
        )
        values["zap_api_endpoint_http"] = get_from_dict_or_env(
            values, "zap_api_endpoint_http", "ZAP_API_ENDPOINT_HTTP"
        )
        values["zap_api_endpoint_https"] = get_from_dict_or_env(
            values, "zap_api_endpoint_https", "ZAP_API_ENDPOINT_HTTPS"
        )

        return values

    def _run(
        self,
        session_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:

        zap_api_client = ZAPv2(
            apikey=self.zap_api_key,
            proxies={
                "http": self.zap_api_endpoint_http,
                "https": self.zap_api_endpoint_https
                }
            )

        try:
            zap_api_client.core.new_session(name=session_name, overwrite=True)
            return f"Session {session_name} initialized successfully."
        except Exception as e:
            logger.exception(f"Error initializing session {session_name}.")
            raise RuntimeError(
                f"Error while running zap_init_session_tool: {e}"
            )


class SessionCloseToolInput(BaseModel):
    """Input for the ZAP API session management tools."""

    session_name: str = Field(
        description="The name of the session."
        )


# Simply overwrite the session for now
class SessionCloseTool(BaseTool):
    """Tool that closes a session in ZAP API.
    """

    zap_api_key: str = ""  #: :meta private:
    zap_api_endpoint_http: str = ""  #: :meta private:
    zap_api_endpoint_https: str = ""  #: :meta private:

    name: str = "zap_close_session_tool"
    description: str = (
        "A tool to close a session in ZAP API. "
        "Useful for when you finished engaging a target and want to remove "
        "all the created artifacts. "
        "Input should be a name of a session."
    )

    args_schema: Type[BaseModel] = SessionCloseToolInput

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that api key and endpoint information exists in environment."""

        values["zap_api_key"] = get_from_dict_or_env(
            values, "zap_api_key", "ZAP_API_KEY"
        )
        values["zap_api_endpoint_http"] = get_from_dict_or_env(
            values, "zap_api_endpoint_http", "ZAP_API_ENDPOINT_HTTP"
        )
        values["zap_api_endpoint_https"] = get_from_dict_or_env(
            values, "zap_api_endpoint_https", "ZAP_API_ENDPOINT_HTTPS"
        )

        return values

    def _run(
        self,
        session_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:

        zap_api_client = ZAPv2(
            apikey=self.zap_api_key,
            proxies={
                "http": self.zap_api_endpoint_http,
                "https": self.zap_api_endpoint_https
                }
            )

        try:
            zap_api_client.core.new_session(name=session_name, overwrite=True)
            return f"Session {session_name} initialized successfully."
        except Exception as e:
            logger.exception(f"Error initializing session {session_name}.")
            raise RuntimeError(
                f"Error while running zap_close_session_tool: {e}"
            )
