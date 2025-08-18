# data/pydantic_models.py
from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict
from datetime import date

# --- MODELS FOR EXTERNAL API RESPONSES ---

class Territory(BaseModel):
    """
    Model for a territory returned by the external API's search endpoint.
    This includes the unique combination of 'code' and 'type' for identification.
    """
    name: str
    code: int
    type: str
    uf: Optional[str] = None

class Translation(BaseModel):
    """
    Model for the translation object returned by the external API.
    Used within the GroupingsResponse model.
    """
    pt: str
    es: str
    en: str

class GroupingsResponse(RootModel[Dict[str, Translation]]):
    """
    Model for the groupings response from the external API.
    It's a dictionary where keys are grouping types and values are translations.
    """
    pass

# --- MODELS FOR YOUR INTERNAL API RESPONSES ---

class AnnualData(BaseModel):
    """
    Model for annual fire data, used in your API's response.
    """
    year: int
    areaHa: float

class MonthlyData(BaseModel):
    """
    Model for monthly fire data, used in your API's response.
    """
    year: int
    month: int
    areaHa: float

class RawFireData(BaseModel):
    """
    Model for the response of your API's data endpoint.
    Includes grouping information for clarity.
    """
    local_name: str
    local_id: str
    local_type: str
    grouping: str 
    annual: List[AnnualData]
    monthly: List[MonthlyData]

# Models for statistic

class Statistics (BaseModel):
    media: int

# --- MODELS FOR INTERNAL CACHE STRUCTURE ---

class CachedData(BaseModel):
    """
    Model for the structure of data stored in the internal cache.
    """
    local_name: str
    local_id: str
    local_type: str
    grouping: str 
    annual: List[AnnualData]
    monthly: List[MonthlyData]
    statistic: Optional[Statistics] = None 
    last_updated: date
