import json
import urllib.request

# FRED API key
api_key = "a858d6aeb49035d915e8424430998b86"

# Fetch data from FRED
def fetch_fred_data(series_id, start_date="1947-01-01", end_date="2024-12-31"):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data['observations']

print("Fetching corporate profits (CPROFIT)...")
profits_data = fetch_fred_data("CPROFIT")

print("\nFetching GDP data...")
gdp_data = fetch_fred_data("GDP")

# Convert to annual data
def get_annual_data(observations):
    annual_data = {}
    for obs in observations:
        year = obs['date'][:4]
        value = float(obs['value'])
        if year not in annual_data:
            annual_data[year] = []
        annual_data[year].append(value)
    
    # Calculate averages
    annual_averages = {}
    for year, values in annual_data.items():
        annual_averages[year] = sum(values) / len(values)
    
    return annual_averages

profits_annual = get_annual_data(profits_data)
gdp_annual = get_annual_data(gdp_data)

print("\nCorporate Profits as % of GDP:")
print("\nYear | Corp Profits | GDP       | % of GDP")
print("-" * 50)

years_to_check = ["1947", "1950", "1955", "1960", "1965", "1970", "1975", "1980", "1985", "1990", "1995", "2000", "2005", "2010", "2015", "2020", "2024"]

for year in years_to_check:
    if year in profits_annual and year in gdp_annual:
        profits = profits_annual[year]
        gdp = gdp_annual[year]
        pct_of_gdp = (profits / gdp) * 100
        print(f"{year} | ${profits:8.1f}B | ${gdp:9.1f}B | {pct_of_gdp:5.1f}%")

# Recent years
print("\nRecent years:")
for year in ["2020", "2021", "2022", "2023", "2024"]:
    if year in profits_annual and year in gdp_annual:
        profits = profits_annual[year]
        gdp = gdp_annual[year]
        pct_of_gdp = (profits / gdp) * 100
        print(f"{year} | ${profits:8.1f}B | ${gdp:9.1f}B | {pct_of_gdp:5.1f}%")
