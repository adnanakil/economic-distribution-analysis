#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# FRED series for labor compensation and GDP
series_dict = {
    'LABSHPUSA156NRUG': 'Share of Labour Compensation in GDP at Current National Prices for United States',
    'W270RE1A156NBEA': 'Compensation of employees/Gross domestic income',
    'A576RC1': 'Compensation of employees',
    'GDP': 'Gross Domestic Product',
    'GDI': 'Gross Domestic Income',
    'GDICOMP': 'Gross domestic income: Compensation of employees, paid',
    'A4102C1Q027SBEA': 'Compensation of employees as a percentage of gross value added'
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

print("Searching for actual labor compensation share of GDP...\n")

# Try different series that might have the actual percentage
for series_id, description in series_dict.items():
    print(f"\nTrying {series_id}: {description}")
    data = fetch_series_data(series_id)
    if data:
        print(f"✓ Found data from {data[0][0]} to {data[-1][0]}")
        # Show recent values to see if it's a percentage
        print("Recent values:")
        for year, value in data[-5:]:
            print(f"  {year}: {value:.1f}")
    else:
        print("✗ No data found")

# Also try calculating it manually from components
print("\n\nCalculating labor share manually from compensation/GDP...")
comp_data = fetch_series_data('A576RC1')  # Compensation of employees (billions)
gdp_data = fetch_series_data('GDP')       # GDP (billions)

if comp_data and gdp_data:
    # Convert to dictionaries
    comp_dict = dict(comp_data)
    gdp_dict = dict(gdp_data)
    
    # Calculate labor share for overlapping years
    overlapping_years = sorted(set(comp_dict.keys()) & set(gdp_dict.keys()))
    
    print(f"\nLabor Compensation as % of GDP:")
    print("Year | Compensation | GDP     | Labor Share")
    print("-" * 50)
    
    # Show every 5 years
    labor_share_data = []
    for year in overlapping_years[::5]:
        comp = comp_dict[year]
        gdp = gdp_dict[year]
        share = (comp / gdp) * 100
        labor_share_data.append((year, share))
        print(f"{year} | ${comp:10.1f}B | ${gdp:10.1f}B | {share:5.1f}%")
    
    # Show recent years
    print("\nRecent years:")
    recent_shares = []
    for year in overlapping_years[-5:]:
        comp = comp_dict[year]
        gdp = gdp_dict[year]
        share = (comp / gdp) * 100
        recent_shares.append((year, share))
        print(f"{year} | ${comp:10.1f}B | ${gdp:10.1f}B | {share:5.1f}%")
    
    # Calculate decade averages
    print("\n\nLabor Share by Decade:")
    decades = {}
    for year in overlapping_years:
        decade = (int(year) // 10) * 10
        if decade not in decades:
            decades[decade] = []
        share = (comp_dict[year] / gdp_dict[year]) * 100
        decades[decade].append(share)
    
    print("Decade | Average Labor Share")
    print("-" * 30)
    decade_avgs = []
    for decade in sorted(decades.keys()):
        avg = sum(decades[decade]) / len(decades[decade])
        decade_avgs.append((f"{decade}s", avg))
        print(f"{decade}s | {avg:18.1f}%")
    
    # Generate JavaScript
    print("\n\nGenerating JavaScript code...")
    print("```javascript")
    print("// Actual labor compensation as percentage of GDP")
    years = [year for year, _ in labor_share_data]
    values = [share for _, share in labor_share_data]
    print(f"const actualLaborShareYears = {json.dumps(years)};")
    print(f"const actualLaborShareValues = {json.dumps([round(v, 1) for v in values])};")
    
    # Decade averages
    decade_names = [name for name, _ in decade_avgs]
    decade_values = [avg for _, avg in decade_avgs]
    print(f"\n// Decade averages of labor share")
    print(f"const laborShareDecades = {json.dumps(decade_names)};")
    print(f"const laborShareDecadeAvgs = {json.dumps([round(v, 1) for v in decade_values])};")
    print("```")

print("\n\nKey Insights:")
print("- Labor compensation includes wages, salaries, and employer contributions to benefits")
print("- This is the most direct measure of 'labor's share' of the economy")
print("- Different from 'labor share index' which is productivity-adjusted")
print("- Shows actual percentage of GDP going to workers")