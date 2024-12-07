from _typeshed import Incomplete
from easy_http_requests.easy_http_response import EasyHttpResponse as EasyHttpResponse
from easy_http_requests.exceptions.easy_http_error import (
    EasyHttpConnectionError as EasyHttpConnectionError,
    EasyHttpRequestError as EasyHttpRequestError,
    EasyHttpTimeoutError as EasyHttpTimeoutError,
)
from typing import Any

class EasyHttpRequest:
    base_url: Incomplete
    def __init__(self, base_url: str | None = None) -> None: ...
    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> EasyHttpResponse: ...
    def post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> EasyHttpResponse: ...
    def put(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> EasyHttpResponse: ...
    def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> EasyHttpResponse: ...
