import requests


class AuthClient:
    """
    Handles user registration and authentication with the mock Avi API.
    Responsible for obtaining and storing the Bearer token.
    """

    def __init__(self, base_url: str, credentials: dict):
        self.base_url = base_url
        self.username = credentials["credentials"]["username"]
        self.password = credentials["credentials"]["password"]
        self.token = None

    def register(self, register_endpoint: str) -> None:
        """
        Registers the user with the mock API.
        Safe to call multiple times (API may ignore duplicates).
        """
        url = f"{self.base_url}{register_endpoint}"
        payload = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(url, json=payload)

        # Registration may fail if user already exists; that is acceptable
        if response.status_code not in (200, 201, 400):
            raise Exception(
                f"Registration failed: {response.status_code} - {response.text}"
            )

        print("INFO: Registration step completed")

    def login(self, login_endpoint: str) -> str:
        """
        Logs in using Basic Auth and retrieves a session token.

        Returns:
            str: Bearer token
        """
        url = f"{self.base_url}{login_endpoint}"

        response = requests.post(
            url,
            auth=(self.username, self.password)
        )

        if response.status_code != 200:
            raise Exception(
                f"Login failed: {response.status_code} - {response.text}"
            )

        data = response.json()

        if "token" not in data:
            raise Exception("Login response does not contain token")

        self.token = data["token"]
        print("INFO: Login successful, token acquired")

        return self.token

    def get_auth_header(self) -> dict:
        """
        Returns Authorization header for authenticated API calls.
        """
        if not self.token:
            raise Exception("Token not available. Please login first.")

        return {
            "Authorization": f"Bearer {self.token}"
        }
       

# Example usage:
credentials = { "credentials": {"username": "user1", "password": "pass123"} }
auth_client = AuthClient("https://mockapi.example.com", credentials)
auth_client.register("/register")
token = auth_client.login("/login")
auth_header = auth_client.get_auth_header()
print("Auth Header:", auth_header)


    
