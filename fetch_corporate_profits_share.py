#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# FRED series for corporate profits share of GDP
series_dict = {
    'W273RE1A156NBEA': 'Corporate profits after tax (without IVA and CCAdj) as % of GDP',
    'A053RC1Q027SBEA': 'Corporate profits before tax (without IVA and CCAdj)',
    'GDP': 'Gross Domestic Product',
    'CP': 'Corporate profits after tax (without IVA and CCAdj)',
    'CPROFIT': 'Corporate Profits with Inventory Valuation Adjustment (IVA) and Capital Consumption Adjustment (CCAdj)'
}

def fetch_series_data(series_id, start_date='1947-01-01', frequency='a'):
    """Fetch data for a FRED series"""
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'frequency': frequency,  # Annual
        'aggregation_method': 'avg'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data and len(data['observations']) > 0:
                return [(obs['date'][:4], float(obs['value'])) for obs in data['observations'] if obs['value'] != '.']
    except Exception as e:
        print(f"Error fetching {series_id}: {e}")
    return None

print("Fetching corporate profits share of GDP data from FRED...\n")

# Try to get the direct ratio series first
print("Searching for direct corporate profits/GDP ratio series...")
ratio_series = fetch_series_data('W273RE1A156NBEA')
if ratio_series:
    print(f"Found direct ratio series with {len(ratio_series)} years of data")
else:
    print("Direct ratio series not found, will calculate manually")

# Get corporate profits and GDP separately
print("\nFetching corporate profits after tax...")
profits_data = fetch_series_data('CP')
print(f"Found {len(profits_data) if profits_data else 0} years of data")

print("\nFetching GDP...")
gdp_data = fetch_series_data('GDP')
print(f"Found {len(gdp_data) if gdp_data else 0} years of data")

# Calculate the ratio
if profits_data and gdp_data:
    print("\nCalculating corporate profits as % of GDP:")
    
    # Convert to dictionaries for easier lookup
    profits_dict = dict(profits_data)
    gdp_dict = dict(gdp_data)
    
    # Calculate ratios for matching years
    ratios = []
    for year in sorted(set(profits_dict.keys()) & set(gdp_dict.keys())):
        ratio = (profits_dict[year] / gdp_dict[year]) * 100
        ratios.append((year, ratio))
    
    # Show data by decade
    print("\nCorporate Profits as % of GDP by Decade:")
    decades = {}
    for year, ratio in ratios:
        decade = (int(year) // 10) * 10
        if decade not in decades:
            decades[decade] = []
        decades[decade].append(ratio)
    
    for decade in sorted(decades.keys()):
        avg_ratio = sum(decades[decade]) / len(decades[decade])
        print(f"  {decade}s: {avg_ratio:.1f}%")
    
    # Show recent years
    print("\nRecent Years:")
    for year, ratio in ratios[-10:]:
        print(f"  {year}: {ratio:.1f}%")
    
    # Generate JavaScript code
    print("\n\nGenerating JavaScript code...")
    print("```javascript")
    print("// Corporate profits after tax as percentage of GDP")
    years = [year for year, _ in ratios[::5]]  # Every 5 years
    values = [ratio for _, ratio in ratios[::5]]
    print(f"const profitShareYears = {json.dumps(years)};")
    print(f"const profitShareValues = {json.dumps([round(v, 1) for v in values])};")
    
    # Decade averages
    decade_years = list(sorted(decades.keys()))
    decade_avgs = [sum(decades[d])/len(decades[d]) for d in decade_years]
    print(f"\n// Decade averages")
    print(f"const profitShareDecades = {json.dumps([f'{d}s' for d in decade_years])};")
    print(f"const profitShareDecadeAvgs = {json.dumps([round(v, 1) for v in decade_avgs])};")
    print("```")

# Historical context from research
print("\n\nHistorical Context (from economic research):")
print("- 1950s: Corporate profits averaged ~13-14% of GDP (high corporate tax era)")
print("- 1960s-1970s: Declined to ~8-10% of GDP")
print("- Early 1980s: Hit low of ~7% during recession")
print("- 1990s-2000s: Rose back to ~10-12%")
print("- 2010s-2020s: Reached post-war highs of ~11-14%")
print("\nNote: Pre-1947 data exists but uses different methodology and is less reliable")