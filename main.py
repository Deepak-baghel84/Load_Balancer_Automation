import os
from src.core.yaml_loader import YamlLoader
from src.core.auth import AuthClient
from src.core.api_client import ApiClient
from src.workflows.vs_disable_workflow import VSDisableWorkflow
from utils.logger import CustomLogger


def main():
    logger = CustomLogger().get_logger(__file__)
    logger.info("Starting Avi Test Automation Framework")

    # -------------------------
    # Load YAML configurations
    # -------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Base Directory:", base_dir)
    pth=os.path.join(base_dir, "config", "api_config.yaml")
    print("YAML Path:", pth)

    api_config = YamlLoader.load_yaml(
        os.path.join("config", "api_config.yaml")
    )
    credentials = YamlLoader.load_yaml(
        os.path.join("config", "credentials.yaml")
    )
    test_case = YamlLoader.load_yaml(
        os.path.join("config", "test_case.yaml")
    )

    base_url = api_config["base_url"]
    endpoints = api_config["endpoints"]

    # -------------------------
    # Authentication
    # -------------------------
    auth_client = AuthClient(base_url, credentials)

    auth_client.register(endpoints["register"])
    auth_client.login(endpoints["login"])

    auth_header = auth_client.get_auth_header()

    # -------------------------
    # API Client Initialization
    # -------------------------
    api_client = ApiClient(base_url, auth_header)

    # -------------------------
    # Execute Workflow
    # -------------------------
    workflow = VSDisableWorkflow(api_client, test_case)
    workflow.run(endpoints)

    logger.info("Automation completed successfully")


if __name__ == "__main__":
    print("starting main working")
    main()
