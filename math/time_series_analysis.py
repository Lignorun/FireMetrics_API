# math/time_series_analysis.py

def calculate_yearly_growth_rate(local_code: str, grouping: str, mode: str):
    """
    Measures the percentage growth of the burned area from one year to the next.
    """
    if mode != "annual":
        return

def calculate_linear_trend(local_code: str, grouping: str, mode: str):
    """
    Indicates whether the burned area has a general trend of increase or decrease over time.
    """
    pass

def calculate_seasonal_index(local_code: str, grouping: str, mode: str):
    """
    Reveals which months of the year are historically more prone to fires.
    """
    if mode != "monthly":
        return

def calculate_rolling_mean(local_code: str, grouping: str, mode: str):
    """
    Smooths monthly or annual fluctuations to more clearly show the long-term trend.
    """
    pass

def compare_to_historical_average(local_code: str, grouping: str, mode: str):
    """
    Compares the burned area of a period to the average for the entire period, indicating if the year was above or below 'normal'.
    """
    pass