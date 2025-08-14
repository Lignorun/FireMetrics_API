from data.cache_manager import get_cache, set_cache
from data.pydantic_models import FireDataResponse
from services.territory_search import search_territories_from_mapbiomas, fetch_external_api_data # Assumindo que a fetch_external_api_data está aqui

# URL da API externa para dados de fogo
FIRE_DATA_API_URL = "https://fogo.geodatin.com/api/statistics/time-series/"

def get_fire_data_with_cache(local_type: str, local_code: str, grouping: str) -> FireDataResponse:
    """
    Orchestrates the fetching of fire data for a territory.
    It checks the cache first, and if not found, fetches from the external API,
    caches the result, and returns the data.
    """
    # 1. Tenta obter os dados do cache
    cached_data = get_cache(local_type, local_code, grouping)
    if cached_data:
        # get_cache já retorna a instância Pydantic, então podemos retorná-la diretamente.
        return cached_data

    # 2. Constrói a URL para a API externa de dados de fogo
    api_url = f"{FIRE_DATA_API_URL}{local_type}/{local_code}/{grouping}?monthStart=1&monthEnd=12"

    # 3. Busca os dados da API externa usando sua função robusta
    data = fetch_external_api_data(api_url)

    # 4. Busca o nome do local para enriquecer os dados.
    # Esta é a parte que você pode refatorar para ser mais eficiente, se possível.
    # Por enquanto, mantemos a busca por termo para compatibilidade.
    territories = search_territories_from_mapbiomas(local_code)
    local_name = "Nome Desconhecido"
    for t in territories:
    # Acesso as chaves do dicionário 't' para encontrar o tipo
        if t['type'] == local_type:
            local_name = t['name']
            break
    
    # 5. Prepara os dados para o cache e Pydantic
    processed_data = {
        "local_name": local_name,
        "local_id": local_code,
        "local_type": local_type,
        "grouping": grouping,
        "annual": data.get("annual", []),
        "monthly": data.get("monthly", []),
    }

    # 6. Armazena os dados no cache
    # Assumindo que `set_cache` está esperando os parâmetros em ordem.
    set_cache(local_type, local_code, grouping, processed_data)

    # 7. Retorna a resposta no formato do Pydantic
    # Converte o dicionário `processed_data` para o modelo `FireDataResponse`.
    return FireDataResponse(**processed_data)