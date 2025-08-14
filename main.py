from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import List,  Optional
# Import models
from data.pydantic_models import (
    Territory,
    GroupingsResponse,
    FireDataResponse,
)
#import functions
from services.territory_search import (
    search_territories_from_mapbiomas, 
    get_grouping_subdivisions_from_mapbiomas)
from services.fire_data import get_fire_data_with_cache

app = FastAPI(
    title="FireMetrics_API",
    description="API for statistical analysis of fire data in Brazil, using data from MapBiomas Fogo.",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
def read_root():
    """
    Main API route that serves the homepage.
    """
    return FileResponse("homepage.html")


@app.get("/territories/{search_term}", tags=["Territory Search"], response_model=List[Territory])
def search_territories(search_term: Optional[str] = None):
    """
    Searches for a territory by name or code.
    Returns a list of territories matching the search term.
    """
    return search_territories_from_mapbiomas(search_term)

# This specific endpoint must come before the generic endpoint with `{search_term}`
@app.get("/territories/ibge/groupings/{local_type}/{local_code}", tags=["Territory Search"], response_model=GroupingsResponse)
def get_grouping_options(local_type: str, local_code: str):
    """
    Retrieves the list of possible territory grouping types.
    This function returns the original JSON from the external MapBiomas API,
    containing all translations ('pt', 'es', 'en').
    """
    data_from_service = get_grouping_subdivisions_from_mapbiomas(local_type, local_code)
    return data_from_service


@app.get("/data/raw/{local_type}/{local_code}/{grouping}", tags=["Data Retrieval"], response_model=FireDataResponse)
def fetch_and_cache_data(local_type: str, local_code: str, grouping: str):
    """
    Fetches and caches the raw fire data for a specific territory based on type, code, and grouping.
    All data fetching, caching, and error handling are managed by a dedicated service function.
    """
    return get_fire_data_with_cache(local_type, local_code, grouping)