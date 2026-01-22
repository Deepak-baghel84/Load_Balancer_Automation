import yaml
import os
from utils.logger import CustomLogger

logger = CustomLogger().get_logger(__file__)

class YamlLoader:
    """
    Centralized YAML loader for configuration-driven automation.
    Responsible for reading and validating YAML files.
    """

    @staticmethod
    def load_yaml(file_path: str) -> dict:
        """
        Load a YAML file and return its contents as a dictionary.

        Args:
            file_path (str): Path to the YAML file

        Returns:
            dict: Parsed YAML content

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If YAML is empty or invalid
        """
        if not os.path.exists(file_path):
            logger.error(f"YAML file not found: {file_path}")
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                logger.error(f"Error parsing YAML file {file_path}: {exc}")
                raise ValueError(f"Error parsing YAML file {file_path}: {exc}")

        if not data:
            logger.error(f"YAML file is empty or invalid: {file_path}")
            raise ValueError(f"YAML file is empty or invalid: {file_path}")

        return data

# Example usage:
if __name__ == "__main__":
    confg = YamlLoader.load_yaml("config/api_config.yaml")
    logger.info(confg)