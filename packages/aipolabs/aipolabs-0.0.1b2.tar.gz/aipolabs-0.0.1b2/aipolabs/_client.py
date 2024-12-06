from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from aipolabs._constants import DEFAULT_AIPOLABS_BASE_URL
from aipolabs._exceptions import APIKeyNotFound
from aipolabs.meta_functions import (
    AipolabsExecuteFunction,
    AipolabsGetFunctionDefinition,
    AipolabsSearchApps,
    AipolabsSearchFunctions,
)
from aipolabs.resource.apps import AppsResource
from aipolabs.resource.functions import FunctionsResource

logger: logging.Logger = logging.getLogger(__name__)


class Aipolabs:
    """Client for interacting with the Aipolabs API.

    This class provides methods to interact with various Aipolabs API endpoints,
    including searching apps and functions, getting function definitions, and
    executing functions.

    Attributes:
        api_key (str): The API key used for authentication.
        base_url (str | httpx.URL): The base URL for API requests.
        inference_provider (str): The inference provider (currently only 'openai').
        headers (dict): HTTP headers used in requests.
        client (httpx.Client): The HTTP client for making requests.
    """

    def __init__(
        self, *, api_key: str | None = None, base_url: str | httpx.URL | None = None
    ) -> None:
        """Create and initialize a new Aipolabs client.

        Args:
            api_key: The API key to use for authentication.
            base_url: The base URL to use for the API requests.
            If values are not provided it will try to read from the corresponding environment variables.
            If no value found for api_key, it will raise APIKeyNotFound.
            If no value found for base_url, it will use the default value.
        """
        if api_key is None:
            api_key = os.environ.get("AIPOLABS_API_KEY")
        if api_key is None:
            raise APIKeyNotFound("The API key is not found.")
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("AIPOLABS_BASE_URL", DEFAULT_AIPOLABS_BASE_URL)
        self.base_url = self._enforce_trailing_slash(httpx.URL(base_url))
        # TODO: currently only openai is supported
        self.inference_provider = "openai"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }
        self.httpx_client = httpx.Client(base_url=self.base_url, headers=self.headers)

        # Initialize resource clients
        self.apps = AppsResource(self.httpx_client)
        self.functions = FunctionsResource(self.httpx_client, self.inference_provider)

    def handle_function_call(self, function_name: str, function_parameters: dict) -> Any:
        """Routes and executes function calls based on the function name.
        This can be a convenience function to handle function calls from LLM without you checking the function name.

        It supports handling built-in meta functions (AIPOLABS_SEARCH_APPS, AIPOLABS_SEARCH_FUNCTIONS,
        AIPOLABS_GET_FUNCTION_DEFINITION, AIPOLABS_EXECUTE_FUNCTION) and also handling executing third-party functions
        directly like BRAVE_SEARCH__WEB_SEARCH.

        Args:
            function_name: Name of the function to be called.
            function_parameters: Dictionary containing the parameters for the function.

        Returns:
            Any: The result (serializable) of the function execution. It varies based on the function.
        """
        logger.info(
            f"Handling function call with name: {function_name} and params: {function_parameters}"
        )
        if function_name == AipolabsSearchApps.NAME:
            apps = self.apps.search(**function_parameters)

            return [app.model_dump() for app in apps]

        elif function_name == AipolabsSearchFunctions.NAME:
            functions = self.functions.search(**function_parameters)

            return [function.model_dump() for function in functions]

        elif function_name == AipolabsGetFunctionDefinition.NAME:
            return self.functions.get(**function_parameters)

        elif function_name == AipolabsExecuteFunction.NAME:
            # TODO: sometimes when using the fixed_tool approach llm most time doesn't put input parameters in the
            # 'function_parameters' key as defined in AIPOLABS_EXECUTE_FUNCTION schema,
            # so we need to handle that here. It is a bit hacky, we should improve this in the future
            # TODO: consider adding post processing to auto fix all common errors in llm generated input parameters
            function_parameters = AipolabsExecuteFunction.wrap_function_parameters_if_not_present(
                function_parameters
            )
            result = self.functions.execute(**function_parameters)
            return result.model_dump(exclude_none=True)

        else:
            # If the function name is not a meta function, we assume it is a direct function execution of
            # an aipolabs indexed function
            # TODO: check function exist if not throw excpetion?
            result = self.functions.execute(function_name, function_parameters)
            return result.model_dump(exclude_none=True)

    def _enforce_trailing_slash(self, url: httpx.URL) -> httpx.URL:
        """Ensures the URL ends with a trailing slash.

        Args:
            url: The URL to process.

        Returns:
            httpx.URL: URL with a guaranteed trailing slash.
        """
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")
