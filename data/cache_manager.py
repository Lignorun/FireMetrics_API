# data/cache_manager.py
from datetime import date, timedelta
from typing import Optional

# Import the cache data model from the pydantic_models file
from data.pydantic_models import CachedData, RawFireData

# A dictionary to store the cached data
_cache_store: dict[str, CachedData] = {}

def set_raw_data_to_cache(local_type: str, local_id: str, grouping: str, data: dict):
    """
    Stores data in the cache using a compound key of type, ID, and grouping.
    The data is stored as a Pydantic model for validation and consistency.
    """
    cache_key = f"{local_type}-{local_id}-{grouping}"
    _cache_store[cache_key] = CachedData(
        local_name=data.get("local_name"),
        local_id=local_id,
        local_type=local_type,
        grouping=grouping,
        annual=data.get("annual", []),
        monthly=data.get("monthly", []),
        last_updated=date.today()
    )

def get_raw_data_from_cache(local_type: str, local_id: str, grouping: str) -> Optional[RawFireData]:
    """
    Retrieves data from the cache using a compound key.
    Returns the data if it's valid and not expired (30 days), otherwise returns None.
    """
    cache_key = f"{local_type}-{local_id}-{grouping}"
    cached_data = _cache_store.get(cache_key)
    
    # Check if data exists and is not older than 30 days
    if cached_data and (date.today() - cached_data.last_updated) < timedelta(days=30):
        return cached_data
    
    return None


def show_all_data(local_type: str, local_id: str, grouping: str) -> Optional[CachedData]:
    """
    Return the full content of a cache item as a Pydantic model,
    using the same arguments as get_raw_data_from_cache.
    """
    cache_key = f"{local_type}-{local_id}-{grouping}"
    cached_data = _cache_store.get(cache_key)

    if not cached_data:
        return None

    return cached_data

