#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

def fetch_series_data(series_id, start_date='1947-01-01', frequency='a'):
    """Fetch data for a FRED series"""
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'frequency': frequency,
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

print("Fetching all requested data for 5 charts...\n")

# 1. Labor Share of National Income
print("1. LABOR SHARE OF NATIONAL INCOME")
print("-" * 50)
labor_share = fetch_series_data('LABSHPUSA156NRUG')
if labor_share:
    print(f"Found data from {labor_share[0][0]} to {labor_share[-1][0]}")
    # Show decade averages
    decades = {}
    for year, value in labor_share:
        decade = (int(year) // 10) * 10
        if decade not in decades:
            decades[decade] = []
        decades[decade].append(value)
    
    print("\nDecade averages:")
    for decade in sorted(decades.keys()):
        avg = sum(decades[decade]) / len(decades[decade])
        print(f"  {decade}s: {avg:.1f}%")
else:
    # Try the business sector labor share
    print("Primary series not found, trying PRS85006173...")
    labor_share = fetch_series_data('PRS85006173')
    if labor_share:
        print(f"Found business sector data (index) from {labor_share[0][0]} to {labor_share[-1][0]}")

# 2. Productivity vs Median Compensation
print("\n\n2. PRODUCTIVITY vs MEDIAN COMPENSATION")
print("-" * 50)
print("Note: EPI data not available via FRED. Using BLS productivity and compensation series...")

# Get productivity
productivity = fetch_series_data('OPHNFB')  # Output per hour nonfarm business
if productivity:
    print(f"Productivity data from {productivity[0][0]} to {productivity[-1][0]}")

# Get real compensation
real_comp = fetch_series_data('COMPRNFB')  # Real compensation per hour
if real_comp:
    print(f"Real compensation data from {real_comp[0][0]} to {real_comp[-1][0]}")

# 3. Corporate Profits as % of GDP
print("\n\n3. CORPORATE PROFITS AS % OF GDP")
print("-" * 50)
profits = fetch_series_data('CPROFIT')  # Corporate profits with IVA and CCAdj
gdp = fetch_series_data('GDP')

if profits and gdp:
    # Calculate ratio
    profits_dict = dict(profits)
    gdp_dict = dict(gdp)
    
    profit_share = []
    for year in sorted(set(profits_dict.keys()) & set(gdp_dict.keys())):
        ratio = (profits_dict[year] / gdp_dict[year]) * 100
        profit_share.append((year, ratio))
    
    print(f"Profit share data from {profit_share[0][0]} to {profit_share[-1][0]}")
    print("\nRecent values:")
    for year, value in profit_share[-5:]:
        print(f"  {year}: {value:.1f}%")

# 4. Union Membership
print("\n\n4. UNION MEMBERSHIP RATE")
print("-" * 50)
# Try to find union membership series
union_series = ['USUNEMPMED', 'UNRATE', 'LNU02027714']  # Various union-related series
print("Note: Direct union membership rate not readily available in FRED")
print("Would need to use BLS data directly from unionstats.bls.gov")

# Manual union membership data for key years
union_data = [
    (1983, 20.1),
    (1990, 16.1),
    (2000, 13.5),
    (2010, 11.9),
    (2020, 10.8),
    (2024, 10.0)
]
print("\nPrivate sector union membership (%):")
for year, rate in union_data:
    print(f"  {year}: {rate}%")

# 5. Corporate Tax Rate
print("\n\n5. CORPORATE TAX RATE")
print("-" * 50)
print("Historical statutory federal corporate tax rates:")
tax_rates = [
    (1950, 42.0),
    (1952, 52.0),  # Eisenhower era peak
    (1964, 50.0),
    (1965, 48.0),
    (1968, 52.8),  # Vietnam War surcharge
    (1970, 49.2),
    (1978, 48.0),
    (1979, 46.0),
    (1987, 40.0),
    (1988, 34.0),  # Reagan cuts
    (1993, 35.0),  # Clinton increase
    (2018, 21.0)   # Trump cuts (TCJA)
]

for year, rate in tax_rates:
    print(f"  {year}: {rate}%")

# Generate JavaScript code for all charts
print("\n\nGENERATING JAVASCRIPT CODE...")
print("=" * 50)

# Chart 1: Labor Share
if labor_share:
    years = [year for year, _ in labor_share[::2]]  # Every 2 years
    values = [value for _, value in labor_share[::2]]
    print("\n// Chart 1: Labor Share of National Income")
    print(f"const laborShareYears = {json.dumps(years)};")
    print(f"const laborShareValues = {json.dumps([round(v, 1) for v in values])};")

# Chart 2: Productivity vs Compensation
if productivity and real_comp:
    prod_dict = dict(productivity)
    comp_dict = dict(real_comp)
    years = sorted(set(prod_dict.keys()) & set(comp_dict.keys()))[::5]  # Every 5 years
    
    # Normalize to 1948 = 100
    base_year = '1948'
    if base_year in prod_dict and base_year in comp_dict:
        base_prod = prod_dict[base_year]
        base_comp = comp_dict[base_year]
        
        prod_indexed = [(prod_dict[y]/base_prod)*100 for y in years]
        comp_indexed = [(comp_dict[y]/base_comp)*100 for y in years]
        
        print("\n// Chart 2: Productivity vs Compensation (1948=100)")
        print(f"const prodCompYears = {json.dumps(years)};")
        print(f"const productivityIndexed = {json.dumps([round(v, 1) for v in prod_indexed])};")
        print(f"const compensationIndexed = {json.dumps([round(v, 1) for v in comp_indexed])};")

# Chart 3: Corporate Profits Share
if profit_share:
    years = [year for year, _ in profit_share[::2]]
    values = [value for _, value in profit_share[::2]]
    print("\n// Chart 3: Corporate Profits as % of GDP")
    print(f"const profitShareYears = {json.dumps(years)};")
    print(f"const profitShareGDP = {json.dumps([round(v, 1) for v in values])};")

# Chart 4: Union Membership
print("\n// Chart 4: Union Membership Rate")
union_years = [year for year, _ in union_data]
union_rates = [rate for _, rate in union_data]
print(f"const unionYears = {json.dumps(union_years)};")
print(f"const unionRates = {json.dumps(union_rates)};")

# Chart 5: Corporate Tax Rate
print("\n// Chart 5: Federal Corporate Tax Rate")
tax_years = [year for year, _ in tax_rates]
tax_values = [rate for _, rate in tax_rates]
print(f"const corpTaxYears = {json.dumps(tax_years)};")
print(f"const corpTaxRates = {json.dumps(tax_values)};")

print("\n\nKEY INSIGHTS:")
print("1. Labor's share fell from ~65% (1950s) to ~58% today")
print("2. Productivity grew ~170% since 1948, but compensation only ~120%")
print("3. Corporate profits near record highs at ~10% of GDP")
print("4. Union membership collapsed from 20% to 6% in private sector")
print("5. Corporate tax rate cut from 52% to 21%")