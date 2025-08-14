from typing import List
from .api_HTTPException import fetch_external_api_data 
from data.pydantic_models import Territory, GroupingsResponse

# external URL used to acces the MapBioma Fire info
MAPBIOMAS_API_URL = "https://fogo.geodatin.com/api"



def get_grouping_subdivisions_from_mapbiomas(local_type: str, local_code: str) -> GroupingsResponse:
    """
    Retrieves a list of subdivisions (e.g., states for a country, municipalities for a state)
    for a given territory from the MapBiomas API.
    """
    url = f"{MAPBIOMAS_API_URL}/territories/{local_type}/{local_code}/groupings"
    response_data = fetch_external_api_data(url)
    return response_data


def search_territories_from_mapbiomas(search_term: str) ->  List[Territory]:
    """
    Searches for a territory in the MapBiomas Fogo API by name or code.
    
    Args:
        search_term: The search term (territory name or code).

    Returns:
    A list of dictionaries representing the territories found.
    """
    clean_search_term = search_term.strip()
    if not search_term: clean_search_term = "Rio de Janeiro"
    url = f"{MAPBIOMAS_API_URL}/territories/search/{clean_search_term}"
    data = fetch_external_api_data(url)

    # The API response is already a list of territories and can be returned directly.
    return data