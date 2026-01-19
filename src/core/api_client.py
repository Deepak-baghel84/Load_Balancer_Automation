import requests


class ApiClient:
    """
    Generic API client for interacting with the mock Avi Controller.
    Handles GET, POST, and PUT requests with authentication headers.
    """

    def __init__(self, base_url: str, auth_header: dict):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            **auth_header
        }

    def get(self, endpoint: str) -> dict:
        """
        Perform a GET request.

        Args:
            endpoint (str): API endpoint

        Returns:
            dict: JSON response
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)

        self._validate_response(response, "GET", endpoint)
        return response.json()

    def post(self, endpoint: str, payload: dict = None) -> dict:
        """
        Perform a POST request.

        Args:
            endpoint (str): API endpoint
            payload (dict): Request body

        Returns:
            dict: JSON response
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=payload)

        self._validate_response(response, "POST", endpoint)
        return response.json()

    def put(self, endpoint: str, payload: dict) -> dict:
        """
        Perform a PUT request.

        Args:
            endpoint (str): API endpoint
            payload (dict): Request body

        Returns:
            dict: JSON response
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, json=payload)

        self._validate_response(response, "PUT", endpoint)
        return response.json()

    @staticmethod
    def _validate_response(response, method: str, endpoint: str) -> None:
        """
        Validate API response.

        Raises:
            Exception if response status code indicates failure
        """
        if not response.ok:
            raise Exception(
                f"{method} {endpoint} failed "
                f"[{response.status_code}]: {response.text}"
            )
