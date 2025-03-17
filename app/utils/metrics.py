import datetime
import math
import json

# Current date: March 16, 2025
current_date = datetime.datetime(2025, 3, 16)

# Define the funds
funds = [
    {
        "name": "ICICI Prudential Bluechip Fund",
        "investment_date": datetime.datetime(2023, 1, 10),
        "amount": 1000000,
        "isn": "INF109K016L0",
        "nav_at_investment": 100,
        "returns_since_investment": 0.125  # 12.5% total return since investment
    },
    {
        "name": "HDFC Top 100 Fund",
        "investment_date": datetime.datetime(2022, 12, 5),
        "amount": 800000,
        "isn": "INF179K01YV8",
        "nav_at_investment": 100,
        "returns_since_investment": 0.102  # 10.2% total return since investment
    },
    {
        "name": "SBI Bluechip Fund",
        "investment_date": datetime.datetime(2023, 2, 15),
        "amount": 1200000,
        "isn": "INF200K01QX4",
        "nav_at_investment": 100,
        "returns_since_investment": 0.11  # 11% total return since investment
    },
    {
        "name": "Axis Bluechip Fund",
        "investment_date": datetime.datetime(2022, 11, 20),
        "amount": 950000,
        "isn": "INF846K01DP8",
        "nav_at_investment": 100,
        "returns_since_investment": 0.098  # 9.8% total return since investment
    },
    {
        "name": "Mirae Asset Large Cap Fund",
        "investment_date": datetime.datetime(2023, 3, 1),
        "amount": 1100000,
        "isn": "INF769K01AX2",
        "nav_at_investment": 100,
        "returns_since_investment": 0.13  # 13% total return since investment
    }
]

def calculate_daily_growth_rate(fund):
    """Calculate the daily growth rate based on total return since investment."""
    total_days = (current_date - fund["investment_date"]).days
    if total_days <= 0:
        return 0
    
    # Calculate daily rate from total return: (1+r)^(1/days) - 1
    daily_rate = math.pow(1 + fund["returns_since_investment"], 1/total_days) - 1
    return daily_rate

def calculate_fund_value_at(fund, target_date):
    """
    Calculate the value of a single fund at a specific date using CAGR.
    """
    investment_date = fund["investment_date"]
    
    # If target date is before investment date, this fund wasn't invested yet
    if target_date < investment_date:
        return 0
    
    # Calculate daily growth rate
    daily_rate = calculate_daily_growth_rate(fund)
    
    # Calculate days invested at target date
    days_at_target = (target_date - investment_date).days
    
    # Apply compound growth formula: P * (1+r)^n
    value_at_target = fund["amount"] * math.pow(1 + daily_rate, days_at_target)
    
    return value_at_target

def calculate_portfolio_value_at(target_date):
    """Calculate the total portfolio value at a specific date."""
    return sum(calculate_fund_value_at(fund, target_date) for fund in funds)

def format_date(date):
    """Format date as 'D MMM YYYY'."""
    return date.strftime("%#d %b %Y")

def generate_dates(period, num_points=30):
    """Generate dates for different time periods."""
    dates = []
    
    if period == "1M":
        # Last month (30 days)
        days_range = 30
    elif period == "3M":
        # Last 3 months (90 days)
        days_range = 90
    elif period == "6M":
        # Last 6 months (180 days)
        days_range = 180
    elif period == "1Y":
        # Last year (365 days)
        days_range = 365
    elif period == "3Y":
        days_range = 1095
    elif period == "MAX":
        # Since earliest investment
        current_date= datetime.datetime(2025, 3, 16)
        earliest_date = min(fund["investment_date"] for fund in funds)
        days_range = (current_date - earliest_date).days
    
    # Generate evenly spaced dates
    for i in range(num_points):
        current_date= datetime.datetime(2025, 3, 16)
        days_back = int((days_range * (num_points - i - 1)) / num_points)
        date = current_date - datetime.timedelta(days=days_back)
        dates.append(date)
    
    return dates

def create_data_sets():
    """Create data sets for different time periods."""
    periods = ["1M", "3M", "6M", "1Y","3Y", "MAX"]
    data_sets = {}
    cdate= datetime.datetime(2025, 3, 16)
    for period in periods:
        dates = generate_dates(period)
        data_sets[period] = [
            {
                "date": format_date(date),
                "value": round(calculate_portfolio_value_at(date))
            }
            for date in dates
        ]
    
    return data_sets

# Generate the data sets
# portfolio_data_sets = create_data_sets()

# Print result in the required format
# print(json.dumps(portfolio_data_sets, indent=2))