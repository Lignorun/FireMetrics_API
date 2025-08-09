import requests
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status

# URL base da API externa do MapBiomas Fogo
MAPBIOMAS_API_URL = "https://fogo.geodatin.com/api"

def get_grouping_options_from_mapbiomas() -> Dict[str, Dict[str, str]]:
    """
    Returns the original JSON from the MapBiomas Fire API with the territory grouping options.
    No user data is sent.
    """
    url = f"{MAPBIOMAS_API_URL}/territories/country/1/groupings"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        # If it's an HTTP error, get the status_code; otherwise, use 502
        status_code = getattr(e.response, "status_code", 502)
        raise HTTPException(status_code=status_code, detail=str(e))

def search_territories_from_mapbiomas(search_term: str) -> List[Dict[str, Any]]:
    """
    Searches for a territory in the MapBiomas Fire API by name or code.
    
    Args:
        search_term: The search term (territory name or code).

    Returns:
        A list of dictionaries representing the territories found.
    """
    clean_search_term = search_term.strip()
    url = f"{MAPBIOMAS_API_URL}/territories/search/{clean_search_term}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # The API response is already a list of territories and can be returned directly.
        return response.json()
    except requests.RequestException as e:
        # If it's an HTTP error, get the status_code; otherwise, use 502
        status_code = getattr(e.response, "status_code", 502)
        raise HTTPException(status_code=status_code, detail=str(e))
