import requests
from utils.logger import CustomLogger

logger = CustomLogger().get_logger(__file__)

class AuthClient:
    """
    Handles user registration and authentication with the mock Avi API.
    Responsible for obtaining and storing the Bearer token.
    """

    def __init__(self, base_url: str, credentials: dict):
        self.base_url = base_url
        logger.info("Initializing AuthClient with base URL: {}".format(base_url))
        self.username = credentials["credentials"]["username"]
        self.password = credentials["credentials"]["password"]
        self.token = None

    def register(self, register_endpoint: str) -> None:
        """
        Registers the user with the mock API.
        Safe to call multiple times (API may ignore duplicates).
        """
        logger.info("Registering user with username: {}".format(self.username))
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

        logger.info("Registration step completed")

    def login(self, login_endpoint: str) -> str:
        """
        Logs in using Basic Auth and retrieves a session token.

        Returns:
            str: Bearer token
        """
        logger.info("Logging in with username: {}".format(self.username))
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
        logger.info("Login successful, token acquired")

        return self.token

    def get_auth_header(self) -> dict:
        """
        Returns Authorization header for authenticated API calls.
        """
        logger.info("Getting auth header")
        if not self.token:
            raise Exception("Token not available. Please login first.")

        return {
            "Authorization": f"Bearer {self.token}"
        }
       


if __name__ == "__main__":
    import sys
    import os
    
    # Add project root to sys.path to allow imports if run directly
    # Assuming script is in src/core, so root is ../../
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    sys.path.append(project_root)

    from src.core.yaml_loader import YamlLoader

    # Load configurations
    try:
        api_config = YamlLoader.load_yaml(os.path.join(project_root, "config/api_config.yaml"))
        credentials = YamlLoader.load_yaml(os.path.join(project_root, "config/credentials.yaml"))
        
        base_url = api_config["base_url"]
        register_endpoint = api_config["endpoints"]["register"]
        login_endpoint = api_config["endpoints"]["login"]

        logger.info(f"Connecting to {base_url}...")

        auth_client = AuthClient(base_url, credentials)
        
        logger.info("Attempting registration...")
        auth_client.register(register_endpoint)
        
        logger.info("Attempting login...")
        token = auth_client.login(login_endpoint)
        
        auth_header = auth_client.get_auth_header()
        logger.info("Auth Header:", auth_header)

    except Exception as e:
        logger.error(f"An error occurred: {e}")


    
