import requests


API_URL = "http://127.0.0.1:8000/predict"
HEALTH_URL = "http://127.0.0.1:8000/health/"


def check_backend_health() -> bool:
    """Return whether the FastAPI backend health endpoint is reachable."""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        response.raise_for_status()
        return response.json().get("status") == "Running"
    except Exception:
        return False


def predict_customer(data: dict) -> dict:
    """
    Send prediction request to FastAPI.

    Parameters
    ----------
    data : dict
        Customer information.

    Returns
    -------
    dict
        Prediction response.
    """

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        raise ConnectionError(
            "Unable to connect to the prediction API."
        )

    except requests.exceptions.Timeout:

        raise TimeoutError(
            "The prediction request timed out."
        )

    except requests.exceptions.HTTPError as e:

        try:
            detail = response.json()["detail"]
        except Exception:
            detail = str(e)

        raise RuntimeError(detail)

    except Exception as e:

        raise RuntimeError(str(e))