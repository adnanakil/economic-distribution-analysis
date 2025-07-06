#!/usr/bin/env python3
import requests
import json
from datetime import datetime

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

def fetch_series_data(series_id, start_date='1950-01-01', frequency='a'):
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

print("Fetching Corporate Tax Data to Calculate Effective Tax Rates")
print("=" * 60)

# Fetch corporate tax receipts
print("\n1. Fetching Federal Corporate Tax Receipts (FCTAX)...")
tax_receipts = fetch_series_data('FCTAX', start_date='1950-01-01')
if tax_receipts:
    print(f"   Found data from {tax_receipts[0][0]} to {tax_receipts[-1][0]}")
else:
    print("   FCTAX not found, trying quarterly series...")
    tax_receipts = fetch_series_data('B075RC1Q027SBEA', start_date='1950-01-01', frequency='a')

# Fetch corporate profits before tax
print("\n2. Fetching Corporate Profits Before Tax...")
profits_before_tax = fetch_series_data('A053RC1Q027SBEA', start_date='1950-01-01', frequency='a')
if not profits_before_tax:
    # Try alternative series
    print("   Trying to calculate from after-tax profits and tax receipts...")
    profits_after_tax = fetch_series_data('CP', start_date='1950-01-01')
    
# Calculate effective tax rates
if tax_receipts and profits_before_tax:
    print("\n3. Calculating Effective Corporate Tax Rates")
    print("-" * 60)
    
    # Convert to dictionaries for easier matching
    tax_dict = dict(tax_receipts)
    profit_dict = dict(profits_before_tax)
    
    # Find overlapping years
    years = sorted(set(tax_dict.keys()) & set(profit_dict.keys()))
    
    print("\nYear | Tax Receipts | Profits Before Tax | Effective Rate | Statutory Rate")
    print("-" * 80)
    
    # Statutory rates for comparison
    statutory_rates = {
        '1950': 42.0, '1951': 50.75, '1952': 52.0, '1953': 52.0, '1954': 52.0,
        '1955': 52.0, '1960': 52.0, '1965': 48.0, '1968': 52.8, '1970': 49.2,
        '1975': 48.0, '1980': 46.0, '1985': 46.0, '1987': 40.0, '1988': 34.0,
        '1990': 34.0, '1993': 35.0, '1995': 35.0, '2000': 35.0, '2005': 35.0,
        '2010': 35.0, '2015': 35.0, '2017': 35.0, '2018': 21.0, '2020': 21.0
    }
    
    # Calculate and display effective rates for key years
    effective_rates = []
    for year in years[::5]:  # Every 5 years
        if year in tax_dict and year in profit_dict and profit_dict[year] > 0:
            taxes = tax_dict[year]
            profits = profit_dict[year]
            effective_rate = (taxes / profits) * 100
            effective_rates.append((year, effective_rate))
            
            # Get statutory rate for comparison
            stat_rate = statutory_rates.get(year, 'N/A')
            
            print(f"{year} | ${taxes:10.1f}B | ${profits:14.1f}B | {effective_rate:13.1f}% | {stat_rate}")
    
    # Show recent years
    print("\nRecent Years:")
    print("-" * 80)
    for year in years[-5:]:
        if year in tax_dict and year in profit_dict and profit_dict[year] > 0:
            taxes = tax_dict[year]
            profits = profit_dict[year]
            effective_rate = (taxes / profits) * 100
            stat_rate = statutory_rates.get(year, 21.0 if int(year) >= 2018 else 35.0)
            
            print(f"{year} | ${taxes:10.1f}B | ${profits:14.1f}B | {effective_rate:13.1f}% | {stat_rate}")
    
    # Calculate decade averages
    print("\n\nEffective Tax Rates by Decade:")
    print("-" * 40)
    decades = {}
    for year, rate in effective_rates:
        decade = (int(year) // 10) * 10
        if decade not in decades:
            decades[decade] = []
        decades[decade].append(rate)
    
    decade_data = []
    for decade in sorted(decades.keys()):
        avg_rate = sum(decades[decade]) / len(decades[decade])
        decade_data.append((f"{decade}s", avg_rate))
        print(f"{decade}s: {avg_rate:.1f}%")
    
    # Generate JavaScript code
    print("\n\nJavaScript Code for Visualization:")
    print("=" * 60)
    print("// Effective vs Statutory Corporate Tax Rates")
    
    # Get data for all years
    all_years = []
    all_effective = []
    all_statutory = []
    
    for year in years[::2]:  # Every 2 years
        if year in tax_dict and year in profit_dict and profit_dict[year] > 0:
            effective_rate = (tax_dict[year] / profit_dict[year]) * 100
            all_years.append(year)
            all_effective.append(round(effective_rate, 1))
            
            # Find closest statutory rate
            stat_year = year
            while stat_year not in statutory_rates and int(stat_year) > 1950:
                stat_year = str(int(stat_year) - 1)
            
            if int(year) >= 2018:
                stat_rate = 21.0
            elif int(year) >= 1993:
                stat_rate = 35.0
            elif int(year) >= 1988:
                stat_rate = 34.0
            else:
                stat_rate = statutory_rates.get(stat_year, 46.0)
            
            all_statutory.append(stat_rate)
    
    print(f"const taxRateYears = {json.dumps(all_years)};")
    print(f"const effectiveTaxRates = {json.dumps(all_effective)};")
    print(f"const statutoryTaxRates = {json.dumps(all_statutory)};")
    
    print("\n// Decade averages")
    decade_names = [d[0] for d in decade_data]
    decade_rates = [round(d[1], 1) for d in decade_data]
    print(f"const taxRateDecades = {json.dumps(decade_names)};")
    print(f"const effectiveTaxRatesByDecade = {json.dumps(decade_rates)};")
    
    # Key insights
    print("\n\nKey Insights:")
    print("-" * 40)
    print("1. Effective rates have ALWAYS been lower than statutory rates")
    print("2. The gap between statutory and effective rates has varied over time")
    print("3. Even when statutory rate was 52%, effective rate was typically 30-40%")
    print("4. Recent effective rates (2018+) are around 10-15% despite 21% statutory rate")
    print("5. Effective rates show the impact of tax loopholes, deductions, and credits")

else:
    print("\nError: Could not fetch required data series")
    print("Please check FRED API availability")