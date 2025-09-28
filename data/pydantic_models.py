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


# --- MODELS FOR STATISTICS --- #

class BasicSummaryStats(BaseModel):
    """
    Basic descriptive statistics about burned area data.
    All names are descriptive and unambiguous.
    """
    sample_size: int                                # Number of observations (n)
    total_area_burned: float                        # Sum of burned area
    average_area_burned: float                      # Mean
    median_area_burned: float                       # Median
    minimum_area_burned: Optional[float] = None    # Minimum
    maximum_area_burned: Optional[float] = None    # Maximum
    range_area_burned: Optional[float] = None      # Max - Min
    variance_area_burned: Optional[float] = None   # Variance
    standard_deviation_area_burned: Optional[float] = None  # Std deviation
    coefficient_of_variation: Optional[float] = None        # Std / Mean
    first_quartile_area_burned: Optional[float] = None      # 25th percentile
    third_quartile_area_burned: Optional[float] = None      # 75th percentile
    sum_cumulative_area_burned: Optional[float] = None      # Running total
    number_of_zero_burned_periods: Optional[int] = None     # Count of zeros
    proportion_of_nonzero_burned_periods: Optional[float] = None  # Fraction > 0


class DescriptiveStats(BaseModel):
    """
    Descriptive statistics about burned area data.
    This model groups all general calculations that are not related to time series.
    """
    coefficient_of_variation: Optional[float] = None
    anomalies_count: Optional[int] = None
    concentration_index: Optional[float] = None
    large_event_proportion: Optional[float] = None
    event_counts_by_bin: Optional[Dict[str, int]] = None

class TimeSeriesStats(BaseModel):
    """
    Time series analysis statistics for burned area data.
    This model groups all calculations that analyze trends and temporal patterns.
    """
    yearly_growth_rate: Optional[List[float]] = None
    linear_trend_slope: Optional[float] = None
    seasonal_index: Optional[Dict[str, float]] = None
    rolling_mean: Optional[List[float]] = None
    historical_comparison: Optional[List[float]] = None

## --- MODELS FOR STATISTICS --- ##


class AnnualStatistics(BaseModel):
    """
    Estatísticas calculadas a partir dos dados anuais.
    """
    basic: Optional[BasicSummaryStats] = None
    descriptive: Optional[DescriptiveStats] = None
    time_series: Optional[TimeSeriesStats] = None


class MonthlyStatistics(BaseModel):
    """
    Estatísticas calculadas a partir dos dados mensais.
    """
    basic: Optional[BasicSummaryStats] = None
    descriptive: Optional[DescriptiveStats] = None
    time_series: Optional[TimeSeriesStats] = None


class Statistics(BaseModel):
    """
    Estrutura geral de estatísticas, separadas em anual e mensal.
    """
    annual: Optional[AnnualStatistics] = None
    monthly: Optional[MonthlyStatistics] = None


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


''' diagram
+-------------------------------------------------------------+
| data/pydantic_models.py                                     |
+-------------------------------------------------------------+

EXTERNAL API MODELS
┌───────────────────────┐
│ Territory             │
│ ─ name: str           │
│ ─ code: int           │
│ ─ type: str           │
│ ─ uf: Optional[str]   │
└───────────────────────┘
┌───────────────────────┐              ┌──────────────────────────────┐
│ Translation           │              │ GroupingsResponse            │
│ ─ pt: str             │◄────────────►│ RootModel[Dict[str,          │
│ ─ es: str             │              │              Translation]]   │
│ ─ en: str             │              └──────────────────────────────┘
└───────────────────────┘


INTERNAL API RESPONSES (RAW DATA)
┌───────────────────────┐     ┌───────────────────────────┐
│ AnnualData            │     │ MonthlyData                │
│ ─ year: int           │     │ ─ year: int               │
│ ─ areaHa: float       │     │ ─ month: int              │
└───────────────────────┘     │ ─ areaHa: float           │
                               └───────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│ RawFireData                                               │
│ ─ local_name: str                                         │
│ ─ local_id: str                                           │
│ ─ local_type: str                                         │
│ ─ grouping: str                                           │
│ ─ annual: List[AnnualData]                                │
│ ─ monthly: List[MonthlyData]                              │
└───────────────────────────────────────────────────────────┘


STATISTICS
                      (shared)
                   ┌───────────────────────┐
                   │ BasicSummaryStats     │
                   │ ─ sample_size: int    │
                   │ ─ average_value: float│
                   │ ─ median_value: float │
                   │ ─ standard_deviation? │
                   │ ─ min_value?          │
                   │ ─ max_value?          │
                   │ ─ first_quartile?     │
                   │ ─ third_quartile?     │
                   └───────────────────────┘
                         ▲            ▲
                         │            │
        ┌────────────────┘            └────────────────┐
        │                                             │
┌───────────────────────────┐               ┌───────────────────────────┐
│ AnnualStatistics          │               │ MonthlyStatistics         │
│ ─ basic?: BasicSummaryStats│              │ ─ basic?: BasicSummaryStats│
│  # (space for trend)      │              │  # (space for trend)       │
└───────────────────────────┘               └───────────────────────────┘

┌───────────────────────────────────────────┐
│ Statistics                                │
│ ─ annual?: AnnualStatistics               │
│ ─ monthly?: MonthlyStatistics             │
└───────────────────────────────────────────┘


CACHE
┌───────────────────────────────────────────────────────────┐
│ CachedData                                                │
│ ─ local_name: str                                         │
│ ─ local_id: str                                           │
│ ─ local_type: str                                         │
│ ─ grouping: str                                           │
│ ─ annual: List[AnnualData]                                │
│ ─ monthly: List[MonthlyData]                              │
│ ─ statistic?: Statistics                                  │
│ ─ last_updated: date                                      │
└───────────────────────────────────────────────────────────┘

RELATIONSHIPS
RawFireData ──(raw data)──────► CachedData
Statistics  ──(statistics)────► CachedData
AnnualData/MonthlyData used by RawFireData and CachedData
BasicSummaryStats is a component of AnnualStatistics and MonthlyStatistics
'''
