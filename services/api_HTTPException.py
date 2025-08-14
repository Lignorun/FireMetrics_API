import requests
import json
from typing import Any
from fastapi import HTTPException, status
from requests.exceptions import Timeout, RequestException

# Default headers to simulate a browser request.
# Useful to avoid being blocked by some external APIs.
_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36 Edg/138.0.0.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Connection': 'keep-alive'
}

def fetch_external_api_data(url: str, timeout: int = 10) -> Any:
    """
    Makes a GET request to an external API and handles common errors gracefully.

    This function is designed to be a robust wrapper for fetching data,
    ensuring the response is a valid JSON and providing user-friendly
    error messages through FastAPI's HTTPException.

    Args:
        url (str): The URL of the external API endpoint.
        timeout (int, optional): Maximum time in seconds to wait for the response.
                                 Defaults to 10.

    Returns:
        Any: The JSON object (dictionary, list, etc.) returned by the API.

    Raises:
        HTTPException:
            - 504 Gateway Timeout: If the external API takes too long to respond.
            - 502 Bad Gateway: If there's a connection issue or the API returns
              invalid JSON data.
            - Other HTTP error codes (e.g., 404, 500): If the API returns a status
              code indicating an error.
    """
    try:
        response = requests.get(url, headers=_HEADERS, timeout=timeout)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        return response.json()
    
    except Timeout:
        # The external service is not responding within the timeout period.
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The external service is taking too long to respond. Please try again in a moment."
        )

    except json.JSONDecodeError:
        # The external service returned data that is not valid JSON.
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The external service returned data in an unexpected format."
        )
        
    except RequestException as e:
        # Catches all other requests-related exceptions (e.g., connection errors,
        # DNS failures, and HTTP errors caught by raise_for_status).
        status_code = getattr(e.response, "status_code", status.HTTP_502_BAD_GATEWAY)
        detail = "Unable to connect to the external service at the moment."
        
        # If there's a specific HTTP error from the external service, provide a more specific detail.
        if e.response is not None:
            detail = f"The external service returned an error: {e.response.status_code} {e.response.reason}"
        
        raise HTTPException(status_code=status_code, detail=detail)