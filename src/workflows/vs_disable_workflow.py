class VSDisableWorkflow:
    """
    Workflow to disable a Virtual Service using the Avi API.
    Implements:
      - Pre-fetch
      - Pre-validation
      - Disable action
      - Post-validation
    """

    def __init__(self, api_client, test_case: dict):
        self.api_client = api_client
        self.test_case = test_case
        self.target_vs_name = test_case["test_case"]["target"]["vs_name"]

    # -------------------------
    # Stage 1: Pre-Fetch
    # -------------------------
    def pre_fetch(self, endpoints: dict) -> None:
        print("INFO: Starting pre-fetch stage")

        resources = self.test_case["test_case"]["workflow"]["pre_fetch"]["resources"]

        if "tenants" in resources:
            tenants = self.api_client.get(endpoints["tenants"])
            print(f"INFO: Tenants fetched: {len(tenants.get('results', []))}")

        if "virtual_services" in resources:
            vs_list = self.api_client.get(endpoints["virtual_services"])
            print(f"INFO: Virtual Services fetched: {len(vs_list.get('results', []))}")

        if "service_engines" in resources:
            se_list = self.api_client.get(endpoints["service_engines"])
            print(f"INFO: Service Engines fetched: {len(se_list.get('results', []))}")

    # -------------------------
    # Utility: Find VS
    # -------------------------
    def _find_virtual_service(self, vs_endpoint: str) -> dict:
        response = self.api_client.get(vs_endpoint)

        for vs in response.get("results", []):
            if vs.get("name") == self.target_vs_name:
                return vs

        raise Exception(f"Virtual Service not found: {self.target_vs_name}")

    # -------------------------
    # Stage 2: Pre-Validation
    # -------------------------
    def pre_validation(self, vs_endpoint: str) -> dict:
        print("INFO: Starting pre-validation stage")

        vs = self._find_virtual_service(vs_endpoint)

        if not vs.get("enabled", False):
            raise Exception(
                f"Pre-validation failed: Virtual Service '{self.target_vs_name}' "
                f"is already disabled"
            )

        print("INFO: Pre-validation successful (VS is enabled)")
        return vs

    # -------------------------
    # Stage 3: Disable VS
    # -------------------------
    def disable_virtual_service(self, vs: dict, vs_endpoint: str) -> None:
        print("INFO: Disabling virtual service")

        vs_uuid = vs.get("uuid")
        if not vs_uuid:
            raise Exception("Virtual Service UUID not found")

        disable_endpoint = f"{vs_endpoint}/{vs_uuid}"

        payload = self.test_case["test_case"]["workflow"]["action"]["payload"]

        self.api_client.put(disable_endpoint, payload)
        print(f"INFO: Virtual Service '{self.target_vs_name}' disabled")

    # -------------------------
    # Stage 4: Post-Validation
    # -------------------------
    def post_validation(self, vs_endpoint: str) -> None:
        print("INFO: Starting post-validation stage")

        vs = self._find_virtual_service(vs_endpoint)

        if vs.get("enabled", True):
            raise Exception(
                f"Post-validation failed: Virtual Service '{self.target_vs_name}' "
                f"is still enabled"
            )

        print("INFO: Post-validation successful (VS is disabled)")

    # -------------------------
    # Workflow Runner
    # -------------------------
    def run(self, endpoints: dict) -> None:
        print("INFO: Executing VS Disable Workflow")

        workflow_cfg = self.test_case["test_case"]["workflow"]

        if workflow_cfg["pre_fetch"]["enabled"]:
            self.pre_fetch(endpoints)

        vs = self.pre_validation(endpoints["virtual_services"])
        self.disable_virtual_service(vs, endpoints["virtual_services"])

        if workflow_cfg["post_validation"]["enabled"]:
            self.post_validation(endpoints["virtual_services"])

        print("INFO: Workflow execution completed successfully")

if __name__ == "__main__":
    api_client = APIClient()
    test_case = {
        "test_case": {
            "target": {
                "vs_name": "test-vs"
            },
            "workflow": {
                "pre_fetch": {
                    "enabled": True,
                    "resources": ["tenants", "virtual_services", "service_engines"]
                },
                "pre_validation": {
                    "enabled": True
                },
                "action": {
                    "enabled": True,
                    "payload": {
                        "enabled": False
                    }
                },
                "post_validation": {
                    "enabled": True
                }
            }
        }
    }

    workflow = VSDisableWorkflow(test_case)
    workflow.run()