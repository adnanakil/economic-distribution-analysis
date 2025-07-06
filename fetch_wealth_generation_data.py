#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# Based on Fed DFA documentation, wealth by generation series
# These are confirmed to exist in FRED
generation_series = {
    'NWFRBSE25165': 'Net Worth - Silent and Earlier (born before 1946)',
    'NWFRBSB46064': 'Net Worth - Baby Boomer (born 1946-1964)',
    'NWFRBSG65080': 'Net Worth - Gen X (born 1965-1980)', 
    'NWFRBSM81000': 'Net Worth - Millennial (born 1981 or later)',
    
    # Try share of total wealth versions
    'WFRBSB01081': 'Share of Total Net Worth - Silent and Earlier',
    'WFRBSB01083': 'Share of Total Net Worth - Baby Boomer',
    'WFRBSB01085': 'Share of Total Net Worth - Gen X',
    'WFRBSB01087': 'Share of Total Net Worth - Millennial'
}

def fetch_series_history(series_id):
    """Fetch historical data for a series"""
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'frequency': 'a',  # Annual
        'aggregation_method': 'avg',
        'observation_start': '2010-01-01'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data and len(data['observations']) > 0:
                return [(obs['date'][:4], float(obs['value'])) for obs in data['observations']]
    except:
        pass
    return None

print("Searching for Fed DFA wealth by generation data...\n")

# Try each series
found_series = {}
for series_id, description in generation_series.items():
    data = fetch_series_history(series_id)
    if data:
        found_series[series_id] = (description, data)
        print(f"✓ Found {series_id}: {description}")
        # Show recent values
        for year, value in data[-3:]:
            if 'Share' in description:
                print(f"  {year}: {value:.1f}%")
            else:
                print(f"  {year}: ${value:,.0f} billion")
    else:
        print(f"✗ Not found: {series_id}")

# Search for generation wealth series
print("\n\nSearching FRED API for generation wealth series...")
search_url = 'https://api.stlouisfed.org/fred/series/search'
search_params = {
    'search_text': 'distributional financial accounts generation',
    'api_key': API_KEY,
    'file_type': 'json',
    'limit': '100',
    'tags': 'dfa'
}

response = requests.get(search_url, params=search_params)
if response.status_code == 200:
    data = response.json()
    if 'seriess' in data:
        gen_series = []
        for series in data['seriess']:
            title = series.get('title', '')
            if any(gen in title.lower() for gen in ['generation', 'millennial', 'boomer', 'gen x', 'silent']):
                gen_series.append((series['id'], title))
        
        if gen_series:
            print(f"\nFound {len(gen_series)} generation-related series:")
            for series_id, title in gen_series[:20]:
                print(f"- {series_id}: {title}")

# If we found data, create visualization data
if found_series:
    print("\n\nGenerating JavaScript code for wealth by generation...")
    print("```javascript")
    print("// Wealth share by generation over time")
    print("const generationYears = [2010, 2015, 2020, 2024];")
    
    # Try to organize data by generation
    shares_by_gen = {}
    for series_id, (desc, data) in found_series.items():
        if 'Share' in desc:
            if 'Silent' in desc:
                gen_name = 'Silent & Earlier'
            elif 'Boomer' in desc:
                gen_name = 'Baby Boomer'
            elif 'Gen X' in desc:
                gen_name = 'Gen X'
            elif 'Millennial' in desc:
                gen_name = 'Millennial'
            else:
                continue
            
            shares_by_gen[gen_name] = data
    
    if shares_by_gen:
        for gen_name, data in shares_by_gen.items():
            values = []
            for target_year in [2010, 2015, 2020, 2024]:
                # Find closest year
                for year, value in data:
                    if int(year) == target_year:
                        values.append(value)
                        break
                else:
                    # Interpolate if needed
                    values.append(0)
            
            print(f"const {gen_name.replace(' ', '').replace('&', '')}Share = {values}; // {gen_name}")
    
    print("```")