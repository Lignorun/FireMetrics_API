# territory_search.py
from typing import List
from .api_HTTPException import fetch_external_api_data
from data.pydantic_models import Territory, GroupingsResponse

# external URL used to access the MapBiomas Fire info
MAPBIOMAS_API_URL = "https://plataforma.monitorfogo.mapbiomas.org/api"


def get_grouping_subdivisions_from_mapbiomas(local_type: str, local_code: str) -> GroupingsResponse:
    """
    Retrieves a list of subdivisions (e.g., states for a country, municipalities for a state)
    for a given territory from the MapBiomas API.
    
    Args:
        local_type: Type of the territory (e.g., "country", "state").
        local_code: Code of the territory.
    
    Returns:
        GroupingsResponse model containing subdivisions.
    """
    url = f"{MAPBIOMAS_API_URL}/territories/{local_type}/{local_code}/groupings"
    response_data = fetch_external_api_data(url)
    return GroupingsResponse(**response_data)


def search_territories_from_mapbiomas(search_term: str) -> List[Territory]:
    """
    Searches for a territory in the MapBiomas Fogo API by name or code.
    
    Args:
        search_term: The search term (territory name or code).
    
    Returns:
        A list of Territory models representing the territories found.
    """
    clean_search_term = search_term.strip() if search_term and search_term.strip() else "Rio de Janeiro"
    url = f"{MAPBIOMAS_API_URL}/territories/search/{clean_search_term}"
    print(url)
    data = fetch_external_api_data(url)

    # Convert each dict to a Territory model
    return [Territory(**item) for item in data]
