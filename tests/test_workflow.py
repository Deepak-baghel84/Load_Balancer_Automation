from src.core.yaml_loader import YamlLoader


api_config = YamlLoader.load_yaml("config/api_config.yaml")
print("API Configuration:", api_config)
credentials = YamlLoader.load_yaml("config/credentials.yaml")
print("Credentials:", credentials)
test_case = YamlLoader.load_yaml("config/test_case.yaml")
print("Test Case:", test_case)