import requests
import json
from typing import Any
from fastapi import HTTPException, status
from requests.exceptions import Timeout, RequestException

# Default headers to simulate a browser request
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 "
        "Mobile Safari/537.36 Edg/138.0.0.0"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
}

def fetch_external_api_data(url: str, timeout: int = 10) -> Any:
    """
    Makes a GET request to an external API, validates the response,
    and ensures it returns a valid, non-empty JSON structure.

    Args:
        url (str): Target API endpoint URL.
        timeout (int): Maximum time (in seconds) to wait for the response.

    Returns:
        Any: Parsed JSON response (dict or list).

    Raises:
        HTTPException:
            - 504 if the request times out.
            - 502 if the API returns invalid JSON, empty JSON, or a connection error occurs.
            - Propagates the API's own status code if available.
    """
    try:
        response = requests.get(url, headers=_HEADERS, timeout=timeout)
        response.raise_for_status()

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The external API returned an invalid (non-JSON) response."
            )

        # Detect empty JSON — considered an error in this context
        if data in (None, {}, []):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The external API returned an empty JSON response, indicating an unexpected error."
            )

        return data

    except Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The external API is taking too long to respond. Please try again."
        )
    except RequestException as e:
        status_code = getattr(e.response, "status_code", status.HTTP_502_BAD_GATEWAY)
        raise HTTPException(status_code=status_code, detail=str(e))
