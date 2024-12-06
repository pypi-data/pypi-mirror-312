from pydantic import model_validator, BaseModel, Field
import logging
from typing import Any, Dict, Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from zapv2 import ZAPv2
import time

logger = logging.getLogger(__name__)


class PassiveScannerRetrieveFindingsToolInput(BaseModel):
    """Input for the ZAP API passive scanner tool."""

    session_name: str = Field(
        description="The name of the session."
        )


class PassiveScannerRetrieveFindingsTool(BaseTool):
    """Tool that retrieves findings from ZAP API passive scanner.
    """

    zap_api_key: str = ""  #: :meta private:
    zap_api_endpoint_http: str = ""  #: :meta private:
    zap_api_endpoint_https: str = ""  #: :meta private:

    name: str = "zap_retrieve_pscan_findings_tool"
    description: str = (
        "A tool to retrieve findngs from the passive scanner in ZAP API. "
        "Useful for when you are engaging a target and want to retrieve "
        "all the findings within the current session. "
    )

    args_schema: Type[BaseModel] = PassiveScannerRetrieveFindingsToolInput

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
            # Load the session
            logger.info(f"Initializing session {session_name}")

            zap_api_client.core.load_session(name=session_name)

            while int(zap_api_client.pscan.records_to_scan) > 0:
                # Loop until the passive scan has finished
                logger.info(f"Records to passive scan : {zap_api_client.pscan.records_to_scan}")
                time.sleep(2)

            logger.info("Passive scan finished.")

            # We simply convert to pretty string
            return str(zap_api_client.core.alerts())

        except Exception as e:
            logger.exception(f"Error while retrieving findings for session {session_name}.")
            raise RuntimeError(
                f"Error while running zap_retrieve_pscan_findings_tool: {e}"
            )
