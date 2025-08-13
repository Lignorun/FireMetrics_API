from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, RootModel
from typing import List, Union, Optional, Dict
from services.territory_search import search_territories_from_mapbiomas, get_grouping_options_from_mapbiomas
from services.fire_data import get_fire_data
from datetime import date, timedelta

# Model for the /territories/search endpoint
class Territory(BaseModel):
    """
    Model to represent a territory returned by the search.
    """
    name: str
    code: Union[int, str]
    type: str
    uf: Optional[str] = None

# --- MODELS FOR THE GROUPINGS ENDPOINT ---
class Translation(BaseModel):
    pt: str
    es: str
    en: str

class GroupingsResponse(RootModel[Dict[str, Translation]]):
    pass
# --------------------------------------------------------

# Model for the fire area data
class AnnualData(BaseModel):
    year: int
    areaHa: float

class MonthlyData(BaseModel):
    year: int
    month: int
    areaHa: float

class FireDataResponse(BaseModel):
    local_name: str
    local_id: str
    annual: List[AnnualData]
    monthly: List[MonthlyData]

# Store all fire data by annual and monthly, for a single local ID
_cache_store = {}

def set_cache(local: str, data: dict):
    _cache_store[local] = {
        "local_name": data.get("local_name"),
        "local_id": local,
        "annual": data.get("annual", []),
        "monthly": data.get("monthly", []),
        "last_updated": date.today()  # Apenas data
    }

def get_cache(local: str, max_age_days=30):
    cached = _cache_store.get(local)
    if cached and cached.get("local_id") == local:
        last_updated = cached["last_updated"]
        if isinstance(last_updated, date) and (date.today() - last_updated) < timedelta(days=max_age_days):
            return cached
    return None

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

# This specific endpoint must come before the generic endpoint with `{search_term}`
@app.get("/territories/ibge/groupings", tags=["Territory Search"], response_model=GroupingsResponse)
def get_grouping_options():
    """
    Retrieves the list of possible territory grouping types.

    This function returns the original JSON from the external MapBiomas API,
    containing all translations ('pt', 'es', 'en').
    """
    data_from_service = get_grouping_options_from_mapbiomas()
    return data_from_service

@app.get("/territories/{search_term}", tags=["Territory Search"], response_model=List[Territory])
def search_territories(search_term: Optional[str] = None):
    """
    Searches for a territory by name or code.
    Returns a list of territories matching the search term.
    """
    return search_territories_from_mapbiomas(search_term)


@app.get("/data/raw/{local}", tags=["Data Retrieval"], response_model=FireDataResponse)
def fetch_and_cache_data(local: str):
    """
    Fetches and caches the raw fire data for a specific territory.
    Returns the processed data.
    """
    cached_data = get_cache(local)
    if cached_data:
        return cached_data

    data = get_fire_data(local)  # Fetch data for this location
    territories = search_territories_from_mapbiomas(local)
    local_name = territories[0].name if territories else "Unknown"
    
    cached_data = {
        "local_name": local_name,
        "local_id": local,
        "annual": data.get("annual", []),
        "monthly": data.get("monthly", []),
    }
    set_cache(local, cached_data)
    return cached_data
