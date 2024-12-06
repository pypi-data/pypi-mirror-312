import requests

from .exceptions import FaultsAPIError

ALL_FAULTS_URL = (
    "https://citypower.mobi/forcelink/za4/rest/calltakemanager/getAllCustomerCalls"
)
LOG_FAULT_URL = (
    "https://citypower.mobi/forcelink/za4/rest/calltakemanager/logCallMyAddress"
)


def get_all_faults(cookie: str) -> list[dict]:
    """
    Fetch all logged faults from the API.
    """
    headers = {"Content-Type": "application/json", "Cookie": cookie}

    try:
        response = requests.get(ALL_FAULTS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise FaultsAPIError(f"Failed to fetch faults: {str(e)}") from e
    except ValueError as e:
        raise FaultsAPIError(f"Invalid JSON response: {str(e)}") from e


def log_fault(cookie: str, fault_data: dict) -> dict:
    """
    Log a fault to the API.
    """
    headers = {
        "Accept": "*/*",
        "Referer": "https://citypower.mobi/logFaultMyAddress",
        "Content-Type": "application/problem+json",
        "Origin": "https://citypower.mobi",
        "Connection": "keep-alive",
        "Cookie": cookie,
    }

    try:
        response = requests.post(
            LOG_FAULT_URL, headers=headers, json=fault_data, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise FaultsAPIError(f"Failed to log fault: {str(e)}") from e
    except ValueError as e:
        raise FaultsAPIError(f"Invalid JSON response: {str(e)}") from e
