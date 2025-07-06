import json
import urllib.request

# FRED API key
api_key = "a858d6aeb49035d915e8424430998b86"

# Fetch data from FRED
def fetch_fred_data(series_id, start_date="1948-01-01", end_date="2024-12-31"):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data['observations']

# Get annual averages from quarterly data
def get_annual_averages(observations):
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

print("Fetching productivity data (OPHNFB)...")
productivity_data = fetch_fred_data("OPHNFB")
productivity_annual = get_annual_averages(productivity_data)

print("\nFetching real compensation data (COMPRNFB)...")
compensation_data = fetch_fred_data("COMPRNFB")
compensation_annual = get_annual_averages(compensation_data)

# Calculate indexed values (1948 = 100)
base_prod = productivity_annual.get('1948', 23.22)  # Use approximate value from data
base_comp = compensation_annual.get('1948', 58.53)  # Use approximate value from data

print("\nProductivity and Compensation Indexed to 1948 = 100:")
print("\nYear | Productivity | Indexed | Compensation | Indexed")
print("-" * 60)

years_to_check = ["1948", "1953", "1958", "1963", "1968", "1973", "1978", "1983", "1988", "1993", "1998", "2003", "2008", "2013", "2018", "2023"]

for year in years_to_check:
    if year in productivity_annual and year in compensation_annual:
        prod_value = productivity_annual[year]
        comp_value = compensation_annual[year]
        prod_indexed = (prod_value / base_prod) * 100
        comp_indexed = (comp_value / base_comp) * 100
        print(f"{year} | {prod_value:10.1f} | {prod_indexed:7.1f} | {comp_value:10.1f} | {comp_indexed:7.1f}")

# Get most recent values
if '2023' in productivity_annual and '2023' in compensation_annual:
    prod_2023 = productivity_annual['2023']
    comp_2023 = compensation_annual['2023']
    prod_growth = ((prod_2023 / base_prod) - 1) * 100
    comp_growth = ((comp_2023 / base_comp) - 1) * 100
    print(f"\nGrowth from 1948 to 2023:")
    print(f"Productivity: +{prod_growth:.1f}%")
    print(f"Compensation: +{comp_growth:.1f}%")
