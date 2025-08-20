# statistics.py
from concurrent.futures import ProcessPoolExecutor
from math.basic_data import basic_stats
from math.descriptive_stats import (
    calculate_coefficient_of_variation,
    detect_anomalies,
    calculate_concentration_index,
    calculate_large_event_proportion,
    count_events_by_size_bin)
from math.time_series_analysis import (
    calculate_yearly_growth_rate,
    calculate_linear_trend,
    calculate_seasonal_index,
    calculate_rolling_mean,
    compare_to_historical_average)

def run_statistics(local_type: str, local_code: str, grouping: str, mode: str):
    # Step 1. Run the main function to generate basic data
    basic_stats(local_type, local_code, grouping, mode)

    # Step 2. List of additional functions (expandable over time)
    functions = [
        calculate_yearly_growth_rate,
        calculate_linear_trend,
        detect_anomalies,
        calculate_seasonal_index,
        calculate_rolling_mean,
        calculate_concentration_index,
        calculate_large_event_proportion,
        count_events_by_size_bin,
        calculate_coefficient_of_variation,
        compare_to_historical_average
    ]

    # Step 3. Run additional functions in parallel using multiple processes
    with ProcessPoolExecutor(max_workers=4) as executor:
        for func in functions:
            executor.submit(func, local_type, local_code, grouping, mode)


'''
Lista de Funções para Análise de Queimadas

* **Taxa de Crescimento Anual** (`calculate_yearly_growth_rate(data)`)
    * Mede o aumento ou a diminuição percentual da área queimada de um ano para o outro.

* **Tendência Linear** (`calculate_linear_trend(data)`)
    * Indica se a área queimada tem uma tendência geral de aumento ou diminuição ao longo do tempo.

* **Detecção de Anomalias** (`detect_anomalies(data)`)
    * Identifica períodos com valores de área queimada que são significativamente maiores ou menores que o padrão.

* **Sazonalidade** (`calculate_seasonal_index(data)`)
    * Revela quais meses do ano são historicamente mais propensos a queimadas.

* **Média Móvel** (`calculate_rolling_mean(data, window_size)`)
    * Suaviza as flutuações mensais ou anuais para mostrar a tendência de longo prazo de forma mais clara.

* **Índice de Concentração** (`calculate_concentration_index(data)`)
    * Determina se a área total queimada está concentrada em poucos eventos de grande escala.

* **Proporção de Eventos de Grande Escala** (`calculate_large_event_proportion(data)`)
    * Calcula a porcentagem de eventos que representam uma grande porção do total.

* **Contagem de Eventos por Faixa de Tamanho** (`count_events_by_size_bin(data, bins)`)
    * Conta quantos eventos se encaixam em categorias de tamanho predefinidas (pequeno, médio, grande, etc.).

* **Coeficiente de Variação** (`calculate_coefficient_of_variation(data)`)
    * Mede a variabilidade ou a instabilidade da área queimada em relação à média, útil para comparar períodos diferentes.

* **Comparação com a Média Histórica** (`compare_to_historical_average(data)`)
    * Compara a área queimada de um ano específico com a média de todo o período, indicando se o ano foi "acima do normal" ou "abaixo do normal".
'''