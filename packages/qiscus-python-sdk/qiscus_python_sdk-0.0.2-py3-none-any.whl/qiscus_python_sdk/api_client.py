import httpx
import os
from typing import Optional, Any, Dict, Union, Tuple
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()


class BaseAPIClient(ABC):
    """Base class for Qiscus API clients.

    Provides common functionality for making HTTP requests to Qiscus APIs.
    Handles authentication, URL construction, and response processing.

    This class serves as an abstract base class that defines the core interface
    and shared functionality for both synchronous and asynchronous API clients.

    Attributes:
        app_id (str): Qiscus application ID used for API authentication
        secret_key (Optional[str]): Secret key for API authentication
        authorization (Optional[str]): Authorization token for authenticated requests
        qiscus_api_base_url (str): Base URL for Qiscus multichannel API endpoints
        qiscus_sdk_base_url (str): Base URL for Qiscus SDK API endpoints
        headers (Dict[str, str]): Default headers used in all API requests

    Example:
        ```python
        class MyAPIClient(BaseAPIClient):
            def request(self, method, endpoint, **kwargs):
                # Implement request handling
                pass

        client = MyAPIClient(
            app_id="my-app-id",
            secret_key="my-secret-key",
            authorization="Bearer token"
        )
        ```
    """

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        app_id: Optional[str] = None,
        authorization: Optional[str] = None,
        secret_key: Optional[str] = None,
        qiscus_api_base_url: Optional[str] = None,
        qiscus_sdk_base_url: Optional[str] = None,
    ):
        """Initialize the API client.

        Args:
            app_id (str): Qiscus application ID for API authentication
            authorization (Optional[str]): Authorization token for authenticated requests.
                Defaults to None.
            secret_key (Optional[str]): Secret key for API authentication.
                Defaults to None.
            qiscus_api_base_url (Optional[str]): Custom base URL for multichannel API.
                If not provided, uses environment variable QISCUS_API_BASE_URL or default URL.
            qiscus_sdk_base_url (Optional[str]): Custom base URL for SDK API.
                If not provided, uses environment variable QISCUS_SDK_BASE_URL or default URL.

        Note:
            At least one of authorization or secret_key should be provided for authenticated requests.
            The app_id is required for most API operations.
        """
        if not self._initialized:
            self.app_id = app_id
            self.secret_key = secret_key
            self.authorization = authorization
            self.qiscus_api_base_url = (
                qiscus_api_base_url
                if qiscus_api_base_url
                else os.getenv(
                    "QISCUS_API_BASE_URL", "https://multichannel-api.qiscus.com"
                )
            )
            self.qiscus_sdk_base_url = (
                qiscus_sdk_base_url
                if qiscus_sdk_base_url
                else os.getenv("QISCUS_SDK_BASE_URL", "https://api.qiscus.com")
            )
            self.headers = {}
            self._get_headers()
            self._initialized = True

    def _get_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers with authentication.

        Constructs headers dictionary with required authentication credentials
        and merges with any additional headers provided.

        Args:
            headers (Optional[Dict[str, str]]): Additional headers to include in requests.
                These will be merged with the default authentication headers.

        Returns:
            Dict[str, str]: Complete headers dictionary with authentication and custom headers.

        Note:
            Default headers always include Qiscus-App-Id. Authorization and
            Qiscus-Secret-Key are added if those credentials were provided during initialization.
            Custom headers take precedence over default headers if there are conflicts.
        """
        if self.app_id:
            self.headers["Qiscus-App-Id"] = self.app_id
        if self.authorization:
            self.headers["Authorization"] = self.authorization
        if self.secret_key:
            self.headers["Qiscus-Secret-Key"] = self.secret_key
        if headers:
            headers.update(self.headers)
        else:
            headers = self.headers
        return headers

    def _get_params(self, params: Optional[Dict] = None) -> Optional[Dict]:
        """Process query parameters.

        Validates and formats query parameters for API requests.

        Args:
            params (Optional[Dict]): Query parameters to process

        Returns:
            Optional[Dict]: Processed query parameters, or None if no parameters provided

        Note:
            Currently returns parameters as-is, but can be extended to add parameter validation,
            transformation, or default values as needed.
        """
        return params

    def _get_data(self, data: Optional[Dict] = None) -> Optional[Dict]:
        """Process request body data.

        Validates and formats request body data for API requests.

        Args:
            data (Optional[Dict]): Request body data to process

        Returns:
            Optional[Dict]: Processed request body data, or None if no data provided

        Note:
            Currently returns data as-is, but can be extended to add data validation,
            transformation, or default values as needed.
        """
        return data

    def _get_base_url(self) -> str:
        """Get base URL for multichannel API.

        Returns:
            str: Base URL for multichannel API endpoints

        Note:
            Returns the configured multichannel API base URL, which can be set via
            environment variable QISCUS_API_BASE_URL or during client initialization.
        """
        return self.qiscus_api_base_url

    def _get_sdk_base_url(self) -> str:
        """Get base URL for SDK API.

        Returns:
            str: Base URL for SDK API endpoints

        Note:
            Returns the configured SDK API base URL, which can be set via
            environment variable QISCUS_SDK_BASE_URL or during client initialization.
        """
        return self.qiscus_sdk_base_url

    def _get_url(self, endpoint: str) -> str:
        """Build full URL for multichannel API endpoint.

        Args:
            endpoint (str): API endpoint path

        Returns:
            str: Complete URL including base URL and endpoint path

        Note:
            Ensures consistent URL formatting by stripping leading slashes from the endpoint
            and combining with the base URL.
        """
        return f"{self._get_base_url()}/{endpoint.lstrip('/')}"

    def _get_sdk_url(self, endpoint: str) -> str:
        """Build full URL for SDK API endpoint.

        Args:
            endpoint (str): API endpoint path

        Returns:
            str: Complete URL including SDK base URL and endpoint path

        Note:
            Ensures consistent URL formatting by stripping leading slashes from the endpoint
            and combining with the SDK base URL.
        """
        return f"{self._get_sdk_base_url()}/{endpoint.lstrip('/')}"

    def _handle_response(self, response: httpx.Response) -> Dict:
        """Process HTTP response.

        Validates the response status and converts response body to JSON.

        Args:
            response (httpx.Response): HTTP response object to process

        Returns:
            Dict: Response data as dictionary

        Raises:
            httpx.HTTPError: If response status indicates an error (4xx, 5xx)
            ValueError: If response body cannot be parsed as JSON

        Note:
            Performs basic response validation and JSON parsing. Can be extended to add
            more sophisticated error handling or response processing.
        """
        response.raise_for_status()
        return response.json()

    def _set_app_id(self, app_id: str):
        self.app_id = app_id
        self._get_headers()

    def _set_authorization(self, authorization: str):
        self.authorization = authorization
        self._get_headers()

    def _set_secret_key(self, secret_key: str):
        self.secret_key = secret_key
        self._get_headers()

    def _set_qiscus_api_base_url(self, qiscus_api_base_url: str):
        self.qiscus_api_base_url = qiscus_api_base_url
        self._get_url()

    def _set_qiscus_sdk_base_url(self, qiscus_sdk_base_url: str):
        self.qiscus_sdk_base_url = qiscus_sdk_base_url
        self._get_sdk_url()

    def _set_default_headers(self, headers: Dict[str, str]):
        self.headers = headers
        self._get_headers()

    @abstractmethod
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make HTTP request to Qiscus API.

        This is an abstract method that must be implemented by subclasses to provide
        either synchronous or asynchronous HTTP request functionality.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters to include in URL
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API instead of multichannel API

        Returns:
            Dict: Response data as dictionary

        Raises:
            NotImplementedError: If not implemented by subclass
            httpx.HTTPError: If request fails or response indicates error
            ValueError: If response cannot be parsed as JSON

        Note:
            Subclasses must implement this method to provide the actual HTTP request
            functionality, either synchronously or asynchronously.
        """
        pass


class APIClient(BaseAPIClient):
    """Synchronous Qiscus API client implementation.

    Provides synchronous HTTP request methods for interacting with Qiscus APIs.
    Implements the abstract request() method from BaseAPIClient using httpx.Client.

    Example:
        ```python
        client = APIClient(
            app_id="my-app-id",
            secret_key="my-secret-key"
        )

        # Make GET request
        response = client.get("users")

        # Make POST request with data
        response = client.post(
            "messages",
            data={"text": "Hello"},
            is_sdk=True
        )
        ```

    Note:
        This client performs blocking HTTP requests. For non-blocking requests,
        use AsyncAPIClient instead.
    """

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make synchronous HTTP request to Qiscus API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters to include in URL
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API instead of multichannel API

        Returns:
            Dict: Response data as dictionary

        Raises:
            httpx.HTTPError: If request fails or response indicates error
            ValueError: If response cannot be parsed as JSON

        Note:
            Uses httpx.Client for synchronous HTTP requests. The client is created
            and closed for each request to ensure proper resource cleanup.
        """
        url = self._get_url(endpoint) if not is_sdk else self._get_sdk_url(endpoint)
        with httpx.Client() as client:
            response = client.request(
                method,
                url,
                headers=self._get_headers(headers),
                params=self._get_params(params),
                json=self._get_data(data),
                files=files,
            )
            return self._handle_response(response)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make POST request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="post".
        """
        return self.request(
            "post", endpoint, data=data, headers=headers, files=files, is_sdk=is_sdk
        )

    def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make GET request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters
            headers (Optional[Dict[str, str]]): Additional request headers
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="get".
        """
        return self.request(
            "get", endpoint, params=params, headers=headers, is_sdk=is_sdk
        )

    def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make PUT request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="put".
        """
        return self.request(
            "put", endpoint, data=data, headers=headers, files=files, is_sdk=is_sdk
        )

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make DELETE request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters
            headers (Optional[Dict[str, str]]): Additional request headers
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="delete".
        """
        return self.request(
            "delete", endpoint, params=params, headers=headers, is_sdk=is_sdk
        )

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make PATCH request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="patch".
        """
        return self.request(
            "patch", endpoint, data=data, headers=headers, files=files, is_sdk=is_sdk
        )

    def login(self, username: str, password: str):
        """Login to Qiscus API.

        Args:
            username (str): Qiscus username
            password (str): Qiscus password
        """
        return self.post("api/v1/auth", data={"email": username, "password": password})


class AsyncAPIClient(BaseAPIClient):
    """Asynchronous Qiscus API client implementation.

    Provides asynchronous HTTP request methods for interacting with Qiscus APIs.
    Implements the abstract request() method from BaseAPIClient using httpx.AsyncClient.

    Example:
        ```python
        client = AsyncAPIClient(
            app_id="my-app-id",
            secret_key="my-secret-key"
        )

        # Make async GET request
        response = await client.get("users")

        # Make async POST request with data
        response = await client.post(
            "messages",
            data={"text": "Hello"},
            is_sdk=True
        )
        ```

    Note:
        This client performs non-blocking HTTP requests using asyncio.
        For blocking requests, use APIClient instead.
    """

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make asynchronous HTTP request to Qiscus API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters to include in URL
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API instead of multichannel API

        Returns:
            Dict: Response data as dictionary

        Raises:
            httpx.HTTPError: If request fails or response indicates error
            ValueError: If response cannot be parsed as JSON

        Note:
            Uses httpx.AsyncClient for non-blocking HTTP requests. The client is created
            and closed for each request to ensure proper resource cleanup.
        """
        url = self._get_url(endpoint) if not is_sdk else self._get_sdk_url(endpoint)
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers=self._get_headers(headers),
                params=self._get_params(params),
                json=self._get_data(data),
                files=files,
            )
            return self._handle_response(response)

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make asynchronous POST request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="post".
        """
        return await self.request(
            "post", endpoint, data=data, headers=headers, files=files, is_sdk=is_sdk
        )

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make asynchronous GET request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters
            headers (Optional[Dict[str, str]]): Additional request headers
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="get".
        """
        return await self.request(
            "get", endpoint, params=params, headers=headers, is_sdk=is_sdk
        )

    async def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make asynchronous PUT request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="put".
        """
        return await self.request(
            "put", endpoint, data=data, headers=headers, files=files, is_sdk=is_sdk
        )

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make asynchronous DELETE request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            params (Optional[Dict]): Query parameters
            headers (Optional[Dict[str, str]]): Additional request headers
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="delete".
        """
        return await self.request(
            "delete", endpoint, params=params, headers=headers, is_sdk=is_sdk
        )

    async def patch(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        is_sdk: bool = False,
    ) -> Dict:
        """Make asynchronous PATCH request to Qiscus API.

        Args:
            endpoint (str): API endpoint path
            data (Optional[Dict]): Request body data
            headers (Optional[Dict[str, str]]): Additional request headers
            files (Optional[Any]): Files to upload
            is_sdk (bool): Whether to use SDK API

        Returns:
            Dict: Response data

        Note:
            Convenience method that wraps request() with method="patch".
        """
        return await self.request(
            "patch", endpoint, data=data, headers=headers, files=files, is_sdk=is_sdk
        )
