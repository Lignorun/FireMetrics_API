from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Union, Optional, Dict
from services.territory_search import search_territories_from_mapbiomas, get_grouping_options_from_mapbiomas
from services.fire_data import get_fire_data

# model for the endpoint /territories/search
class Territory(BaseModel):
    """
    Model to represent a territory returned by the search.
    """
    name: str
    code: Union[int, str]
    type: str
    uf: Optional[str] = None

## model for the endpoint /territories/groupings
class Translation(BaseModel):
    pt: str
    es: str
    en: str

class GroupingsResponse(BaseModel):
    __root__: Dict[str, Translation]


# model for the area data of fire 
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


# store all teh fire data by annual and monthly, for only one local id
_cache_store = {}  # Simple dictionary to store cache in memory

def set_cache(local: str, data: dict):
    _cache_store[local] = {
        "local_name": data.get("local_name"),
        "local_id": local,
        "annual": data.get("annual", []),
        "monthly": data.get("monthly", [])
    }

def get_cache(local: str):
    cached = _cache_store.get(local)
    if cached and cached.get("local_id") == local:
        # Here you can implement cache validity checks if you want
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



@app.get("/territories/{search_term}", tags=["Territory Search"], response_model=List[Territory])
def search_territories(search_term: Optional[str] = None):
    """
    Searches for a territory by name or code.
    Returns a list of territories matching the search term.
    """
    return search_territories_from_mapbiomas(search_term)


@app.get("/territories/groupings", tags=["Territory Search"], response_model=GroupingsResponse)
def get_grouping_options():
    """
    Retrieves the list of possible territory grouping types.

    This function returns the original JSON from the external MapBiomas API,
    containing all translations ('pt', 'es', 'en').
    """
    return get_grouping_options_from_mapbiomas()




@app.get("/data/raw/{local}", tags=["Data Retrieval"], response_model=FireDataResponse)
def fetch_and_cache_data(local: str):
    # local já recebido via URL
    data = get_fire_data(local) # Busca os dados para esse local
    territories = search_territories_from_mapbiomas(local) 
    local_name = territories[0].name if territories else "Unknown"
    # FIM DA ALTERAÇÃO
 
    cached_data = {
        "local_name": local_name,
        "local_id": local,
        "annual": data.get("annual", []),
        "monthly": data.get("monthly", [])
    }
    set_cache(local, cached_data)
    return cached_data
