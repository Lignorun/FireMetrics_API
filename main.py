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



@app.get("/territories/search", tags=["Territory Search"], response_model=List[Territory])
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


######## To be implemented ########
@app.get("/data/annual/{local}", tags=["Data Retrieval"])
def get_annual_data_endpoint(local: str):
    """
    Retrieves all annual fire data for a specific location.
    """
    data = get_fire_data(local=local, interval="annual")
    return {"message": f"Annual data for {local}", "data": data}


######## To be implemented ########
@app.get("/data/monthly/{local}", tags=["Data Retrieval"])
def get_monthly_data_endpoint(local: str):
    """
    Retrieves all monthly fire data for a specific location.
    """
    data = get_fire_data(local=local, interval="monthly")
    return {"message": f"Monthly data for {local}", "data": data}
