import requests


class EasyHttpResponse:
    """
    Wrapper for an HTTP response object.

    Attributes:
        response (requests.models.Response): The original response object.
    """

    def __init__(self, response: requests.models.Response):
        """
        Initializes the EasyHttpResponse wrapper.

        Args:
            response (requests.models.Response): The original response object to wrap.
        """
        self.response = response

    @property
    def status_code(self) -> int:
        """
        The HTTP status code of the response.

        Returns:
            int: The status code of the response.
        """
        return self.response.status_code

    @property
    def headers(self) -> requests.structures.CaseInsensitiveDict:
        """
        The headers of the response.

        Returns:
            CaseInsensitiveDict[str]: A dictionary-like object containing the response headers.
        """
        return self.response.headers

    @property
    def body(self) -> dict:
        """
        The JSON body of the response.

        Returns:
            dict: The parsed JSON body of the response.

        Raises:
            ValueError: If the response does not contain valid JSON.
        """
        return self.response.json()

    @property
    def text(self) -> str:
        """
        The raw text body of the response.

        Returns:
            str: The response body as a string.
        """
        return self.response.text
