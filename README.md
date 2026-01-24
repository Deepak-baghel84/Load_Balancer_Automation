# Load Balancer Automation Framework

This project is a modular automation framework designed for interacting with Load Balancers (specifically Avi/VMware NSX ALB). It provides a structured approach to authentication, API interaction, and workflow execution.

## Features

- **Modular Design**: Separates authentication, API client, workflows, and configuration.
- **YAML Configuration**: Uses YAML files for API endpoints, credentials, and test cases/workflow definitions.
- **Robust Logging**: utilizes `structlog` for detailed logging of automation steps.
- **Workflow Engine**: Supports defined workflows with pre-fetch, pre-validation, action, and post-validation stages.
- **Extensible**: Easy to add new workflows and API interactions.

## Project Structure

```
Load_Balancer_Automation/
├── config/                 # Configuration files
│   ├── api_config.yaml     # API Base URL and endpoints
│   ├── credentials.yaml    # User credentials
│   └── test_case.yaml      # Workflow and test case definitions
├── lb_env/                 # Virtual environment (optional)
├── logs/                   # Log files directory
├── src/                    # Source code
│   ├── core/               # Core modules (Auth, API Client, YAML Loader)
│   ├── workflows/          # Workflow implementations (e.g., VSDisableWorkflow)
│   ├── validators/         # Validation logic
│   └── mocks/              # Mock objects for testing
├── utils/                  # Utility scripts (Logger)
├── tests/                  # Unit and integration tests
├── main.py                 # Entry point of the application
├── setup.py                # Package setup file
├── requirements.txt        # Python dependencies
└── README.md               # This documentation
```

## Prerequisites

- Python 3.x
- pip package manager

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd Load_Balancer_Automation
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv lb_env
   # Windows
   lb_env\Scripts\activate
   # Linux/Mac
   source lb_env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The framework uses three main configuration files located in the `config/` directory:

1.  **`api_config.yaml`**: Defines the base URL and API endpoints.
    ```yaml
    base_url: "https://<controller_ip>"
    endpoints:
      login: "/login"
      virtual_services: "/api/virtualservice"
      # ... other endpoints
    ```

2.  **`credentials.yaml`**: Stores authentication details.
    ```yaml
    username: "<username>"
    password: "<password>"
    ```

3.  **`test_case.yaml`**: Defines the specific test case and workflow parameters.
    ```yaml
    test_case:
      target:
        vs_name: "my-virtual-service"
      workflow:
        pre_fetch:
          enabled: true
          resources: ["tenants", "virtual_services"]
        action:
          payload:
             enabled: false
    ```

## Usage

To run the automation framework, execute the `main.py` script:

```bash
python main.py
```

### Execution Flow

1.  **Initialization**: Loads configurations and sets up the logger.
2.  **Authentication**: Authenticates with the Load Balancer using credentials.
3.  **API Setup**: Initializes the API client with the authentication token.
4.  **Workflow Execution**: Runs the specified workflow (e.g., `VSDisableWorkflow`).
    *   **Pre-Fetch**: Fetches necessary resources (Tenants, VS lists, etc.).
    *   **Pre-Validation**: Verifies the state before action (e.g., checks if VS is enabled).
    *   **Action**: Performs the operation (e.g., disables the VS).
    *   **Post-Validation**: Verifies the state after action (e.g., checks if VS is disabled).

## Logging

Logs are generated in the `logs/` directory. The framework uses `structlog` to provide structured and readable logs for debugging and tracking the execution flow.

## Extending the Framework

- **New Workflows**: Create a new class in `src/workflows/` inheriting the structure of `VSDisableWorkflow`.
- **New API Endpoints**: Add them to `config/api_config.yaml`.
- **New Utilities**: Add helper functions to `utils/`.
