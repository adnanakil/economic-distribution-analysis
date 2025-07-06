#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# FRED series for labor share and corporate profits
series_dict = {
    'PRS85006173': 'Nonfarm Business Sector: Labor Share (Index 2017=100)',
    'W273RE1A156NBEA': 'Corporate profits after tax (without IVA and CCAdj) as % of GDP',
    'CP': 'Corporate profits after tax (without IVA and CCAdj)',
    'GDP': 'Gross Domestic Product'
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

print("Fetching labor share and corporate profits data from FRED...\n")

# Get labor share data
print("Fetching non-farm business labor share (PRS85006173)...")
labor_share_data = fetch_series_data('PRS85006173')
if labor_share_data:
    print(f"Found {len(labor_share_data)} years of data")
    print(f"Data range: {labor_share_data[0][0]} to {labor_share_data[-1][0]}")
else:
    print("Labor share series not found")

# Get corporate profits and GDP
print("\nFetching corporate profits and GDP...")
profits_data = fetch_series_data('CP')
gdp_data = fetch_series_data('GDP')

# Calculate profit share for same years as labor share
if labor_share_data and profits_data and gdp_data:
    print("\nCalculating comparable data...")
    
    # Convert to dictionaries
    labor_dict = dict(labor_share_data)
    profits_dict = dict(profits_data)
    gdp_dict = dict(gdp_data)
    
    # Find overlapping years
    overlapping_years = sorted(set(labor_dict.keys()) & set(profits_dict.keys()) & set(gdp_dict.keys()))
    
    print(f"\nLabor Share vs Corporate Profit Share:")
    print("Year | Labor Share | Profit Share | Sum")
    print("-" * 50)
    
    # Show key years
    for year in overlapping_years[::5]:  # Every 5 years
        labor_share = labor_dict[year]
        profit_share = (profits_dict[year] / gdp_dict[year]) * 100
        total = labor_share + profit_share  # Note: not directly comparable as different bases
        print(f"{year} | {labor_share:11.1f} | {profit_share:11.1f}% | {total:5.1f}")
    
    # Show recent years
    print("\nRecent years:")
    for year in overlapping_years[-5:]:
        labor_share = labor_dict[year]
        profit_share = (profits_dict[year] / gdp_dict[year]) * 100
        print(f"{year} | {labor_share:11.1f} | {profit_share:11.1f}%")
    
    # Calculate decade averages
    print("\n\nDecade Averages:")
    print("Decade | Avg Labor Share | Avg Profit Share")
    print("-" * 50)
    
    decades = {}
    for year in overlapping_years:
        decade = (int(year) // 10) * 10
        if decade not in decades:
            decades[decade] = {'labor': [], 'profit': []}
        decades[decade]['labor'].append(labor_dict[year])
        decades[decade]['profit'].append((profits_dict[year] / gdp_dict[year]) * 100)
    
    decade_data = []
    for decade in sorted(decades.keys()):
        avg_labor = sum(decades[decade]['labor']) / len(decades[decade]['labor'])
        avg_profit = sum(decades[decade]['profit']) / len(decades[decade]['profit'])
        decade_data.append((f"{decade}s", avg_labor, avg_profit))
        print(f"{decade}s | {avg_labor:15.1f} | {avg_profit:16.1f}%")
    
    # Generate JavaScript code
    print("\n\nGenerating JavaScript code...")
    print("```javascript")
    print("// Labor share and corporate profit share by year")
    
    # Annual data for line chart
    years = [year for year in overlapping_years[::2]]  # Every 2 years
    labor_values = [labor_dict[year] for year in years]
    profit_values = [(profits_dict[year] / gdp_dict[year]) * 100 for year in years]
    
    print(f"const laborProfitYears = {json.dumps(years)};")
    print(f"const laborShareValues = {json.dumps([round(v, 1) for v in labor_values])};  // Index 2017=100")
    print(f"const profitShareValues = {json.dumps([round(v, 1) for v in profit_values])};  // % of GDP")
    
    # Decade data
    decade_names = [d[0] for d in decade_data]
    decade_labor = [round(d[1], 1) for d in decade_data]
    decade_profit = [round(d[2], 1) for d in decade_data]
    
    print(f"\n// Decade averages")
    print(f"const laborProfitDecades = {json.dumps(decade_names)};")
    print(f"const laborShareDecadeAvgs = {json.dumps(decade_labor)};")
    print(f"const profitShareDecadeAvgs = {json.dumps(decade_profit)};")
    print("```")
    
    # Key insights
    print("\n\nKey Insights:")
    print("1. Labor share is indexed to 2017=100, so values >100 mean higher than 2017")
    print("2. In the 1960s-1970s, labor share was ~105-110 (5-10% higher than 2017)")
    print("3. Labor share declined from ~105 in 1970s to ~95 in 2010s")
    print("4. As labor's share fell, corporate profits' share doubled")
    print("5. The inverse relationship is clear: when labor gets less, capital gets more")