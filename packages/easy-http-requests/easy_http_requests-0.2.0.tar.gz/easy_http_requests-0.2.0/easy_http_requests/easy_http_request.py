import requests
from typing import Optional, Dict, Any
from easy_http_requests.easy_http_response import EasyHttpResponse
from easy_http_requests.exceptions.easy_http_error import (
    EasyHttpRequestError,
    EasyHttpTimeoutError,
    EasyHttpConnectionError,
)


class EasyHttpRequest:
    """
    A simple HTTP client for making requests to a specified base URL.

    Attributes:
        base_url (str): The base URL for all requests. Defaults to an empty string.
    """

    def __init__(self, base_url: Optional[str] = None):
        """
        Initializes the EasyHttpRequest client.

        Args:
            base_url (Optional[str]): The base URL for all requests. If None, requests
                will be made to absolute URLs.
        """
        self.base_url = base_url.rstrip("/") if base_url else ""

    def get(self, endpoint: str) -> EasyHttpResponse:
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the GET request to.

        Returns:
            EasyHttpResponse: The response wrapped in an EasyHttpResponse object.

        Raises:
            EasyHttpTimeoutError: If the request times out.
            EasyHttpConnectionError: If there is a connection error.
            EasyHttpRequestError: For all other request-related errors.
        """
        response = self._make_request("GET", endpoint)
        return EasyHttpResponse(response)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
    ) -> EasyHttpResponse:
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the POST request to.
            json (Optional[Dict[str, Any]]): A dictionary to be sent as JSON in the request body.
            data (Optional[Any]): Data to be sent in the request body.

        Returns:
            EasyHttpResponse: The response wrapped in an EasyHttpResponse object.

        Raises:
            EasyHttpTimeoutError: If the request times out.
            EasyHttpConnectionError: If there is a connection error.
            EasyHttpRequestError: For all other request-related errors.
        """
        response = self._make_request("POST", endpoint, json=json, data=data)
        return EasyHttpResponse(response)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> requests.models.Response:
        """
        Sends an HTTP request to the specified endpoint.

        Args:
            method (str): The HTTP method to use (e.g., "GET", "POST").
            endpoint (str): The endpoint to send the request to.
            params (Optional[Dict[str, Any]]): A dictionary of query parameters.
            data (Optional[Any]): Data to be sent in the request body.
            json (Optional[Dict[str, Any]]): A dictionary to be sent as JSON in the request body.

        Returns:
            requests.models.Response: The raw response object from the requests library.

        Raises:
            EasyHttpTimeoutError: If the request times out.
            EasyHttpConnectionError: If there is a connection error.
            EasyHttpRequestError: For all other request-related errors.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
        try:
            response = requests.request(
                method, url, params=params, data=data, json=json
            )
            return response
        except requests.Timeout as e:
            raise EasyHttpTimeoutError(
                "The request timed out", original_exception=e
            ) from e
        except requests.ConnectionError as e:
            raise EasyHttpConnectionError(
                "Failed to connect to the server", original_exception=e
            ) from e
        except requests.RequestException as e:
            raise EasyHttpRequestError(
                "HTTP request failed", original_exception=e
            ) from e
