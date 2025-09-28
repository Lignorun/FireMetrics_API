# services/fire_data.py

from data.cache_manager import (
    get_raw_data_from_cache,
    set_raw_data_to_cache,
    show_all_data,
)
from data.pydantic_models import RawFireData, CachedData
from services.territory_search import search_territories_from_mapbiomas
from services.api_HTTPException import fetch_external_api_data  # import corrigido

# External API base URL for fire data
FIRE_DATA_API_URL = "https://plataforma.monitorfogo.mapbiomas.org/api/statistics/time-series/"


def get_raw_fire_data_of_cache(local_type: str, local_code: str, grouping: str) -> RawFireData:
    """
    Fetches fire data for a territory, using cache when available.

    Steps:
    1. Tries to load from cache.
    2. If not cached, fetches from the external API.
    3. Retrieves the local name for enrichment.
    4. Caches the processed data.
    5. Returns the result as a validated Pydantic model.

    Args:
        local_type: Type of the territory (e.g., "state", "municipality").
        local_code: Unique code of the territory.
        grouping: Grouping option for aggregation (e.g., "biome").

    Returns:
        RawFireData: Validated fire data for the requested territory.
    """
    # 1. Try cache
    cached_data = get_raw_data_from_cache(local_type, local_code, grouping)
    if cached_data:
        return cached_data

    # 2. Fetch from API
    api_url = f"{FIRE_DATA_API_URL}{local_type}/{local_code}/{grouping}?monthStart=1&monthEnd=12"
    data = fetch_external_api_data(api_url)

    # 3. Enrich with local name
    territories = search_territories_from_mapbiomas(local_code)
    local_name = next((t.name for t in territories if t.type == local_type), "unknoing")

    # 4. Prepare processed data
    processed_data = {
        "local_name": local_name,
        "local_id": local_code,
        "local_type": local_type,
        "grouping": grouping,
        "annual": data.get("annual", []),
        "monthly": data.get("monthly", []),
    }

    # 5. Cache the data
    set_raw_data_to_cache(local_type, local_code, grouping, processed_data)

    # 6. Return as Pydantic model
    return RawFireData(**processed_data)


def get_all_fire_data_from_cache(local_type: str, local_code: str, grouping: str) -> CachedData:
    """
    Returns all fire data stored in the cache, including raw data and statistics.

    Args:
        local_type: Type of the territory.
        local_code: Code of the territory.
        grouping: Grouping option.

    Returns:
        CachedData: The cached data object.
    """

    cached_data = show_all_data(local_type, local_code, grouping)
    if cached_data:
        return cached_data
    return None
