from pydantic import model_validator, BaseModel, Field
import logging
from typing import Any, Dict, Optional, Type, List
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from zapv2 import ZAPv2
import time


logger = logging.getLogger(__name__)


class CrawlingToolInput(BaseModel):
    """Input for the CrawlingTool tool."""

    session_name: str = Field(
        description="The name of the ZAP API session."
        )

    uris_seed: List[str] = Field(
        description="List of seed URIs for starting the crawling process"
        )


class CrawlingTool(BaseTool):
    """Tool that crawls a web application using ZAP API.
    """

    zap_api_key: str = ""  #: :meta private:
    zap_api_endpoint_http: str = ""  #: :meta private:
    zap_api_endpoint_https: str = ""  #: :meta private:

    name: str = "zap_crawling_tool"
    description: str = (
        """
A penetration testing tool optimized for crawling a web application
using ZAP API. Useful for when you need have a set of seed URLs and
want to discover more URLs.

Input should be a list of seed URIs.
        """
    )

    args_schema: Type[BaseModel] = CrawlingToolInput

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
        uris_seed: List[str],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[str]:
        """Use the tool."""

        zap_api_client = ZAPv2(
            apikey=self.zap_api_key,
            proxies={
                "http": self.zap_api_endpoint_http,
                "https": self.zap_api_endpoint_https
                }
            )

        uris_found = set([])

        try:
            # Create new session
            zap_api_client.core.load_session(name=session_name)

            for target in uris_seed:
                logger.info(f'Crawling {target}')

                zap_api_client.urlopen(target)
                # Give the sites tree a chance to get updated
                time.sleep(2)

                scanid = zap_api_client.spider.scan(target)
                # Give the Spider a chance to start
                time.sleep(2)

                while (int(zap_api_client.spider.status(scanid)) < 100):
                    # Loop until the spider has finished
                    logger.info('Spider progress %: {}'.format(
                        zap_api_client.spider.status(scanid)
                        ))
                    time.sleep(2)

                logger.info(f'Spidering completed for {target}')

            for uri_found in zap_api_client.core.urls():
                uris_found.add(uri_found)

            return list(uris_found)
        except Exception as e:
            logger.exception(f"Error while crawling targets for session {session_name}.")
            raise RuntimeError(
                f"Error while running zap_crawling_tool: {e}"
            )
