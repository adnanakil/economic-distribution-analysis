#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# Known FRED series IDs for household net worth by age of reference person
# These are from the Fed's Distributional Financial Accounts
age_series = {
    'NWFRBLT0134': 'Net Worth, Less than 35 years',
    'NWFRBLA3544': 'Net Worth, 35-44 years', 
    'NWFRBLA4554': 'Net Worth, 45-54 years',
    'NWFRBLA5564': 'Net Worth, 55-64 years',
    'NWFRBLA6574': 'Net Worth, 65-74 years',
    'NWFRBLA75UP': 'Net Worth, 75 years and over'
}

# Alternative series IDs (mean values)
mean_series = {
    'NWFRBMA0134': 'Mean Net Worth, Less than 35',
    'NWFRBMA3544': 'Mean Net Worth, 35-44',
    'NWFRBMA4554': 'Mean Net Worth, 45-54', 
    'NWFRBMA5564': 'Mean Net Worth, 55-64',
    'NWFRBMA6574': 'Mean Net Worth, 65-74',
    'NWFRBMA75UP': 'Mean Net Worth, 75+'
}

def fetch_series_data(series_id):
    """Fetch the latest observation for a series"""
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': '1'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data and len(data['observations']) > 0:
                return float(data['observations'][0]['value'])
    except:
        pass
    return None

print("Searching for Fed DFA wealth by age data...\n")

# Try the level series first
print("Trying aggregate net worth by age series...")
found_data = {}
for series_id, description in age_series.items():
    value = fetch_series_data(series_id)
    if value is not None:
        found_data[description] = value
        print(f"✓ Found {series_id}: {description} = ${value:,.0f}")
    else:
        print(f"✗ Not found: {series_id}")

# If level series don't work, try mean series
if not found_data:
    print("\nTrying mean net worth by age series...")
    for series_id, description in mean_series.items():
        value = fetch_series_data(series_id)
        if value is not None:
            found_data[description] = value
            print(f"✓ Found {series_id}: {description} = ${value:,.0f}")
        else:
            print(f"✗ Not found: {series_id}")

# Search for series using the API search endpoint
print("\n\nSearching FRED API for 'age of reference person'...")
search_url = 'https://api.stlouisfed.org/fred/series/search'
search_params = {
    'search_text': 'age of reference person net worth',
    'api_key': API_KEY,
    'file_type': 'json',
    'limit': '100'
}

response = requests.get(search_url, params=search_params)
if response.status_code == 200:
    data = response.json()
    if 'seriess' in data:
        age_series_found = []
        for series in data['seriess']:
            title = series.get('title', '')
            if 'age' in title.lower() and ('net worth' in title.lower() or 'wealth' in title.lower()):
                age_series_found.append((series['id'], title))
        
        if age_series_found:
            print(f"\nFound {len(age_series_found)} series with 'age' and 'net worth' in title:")
            for series_id, title in age_series_found[:15]:
                print(f"- {series_id}: {title}")
                
            # Try to fetch data for the first few
            print("\nFetching data for found series...")
            for series_id, title in age_series_found[:5]:
                value = fetch_series_data(series_id)
                if value is not None:
                    print(f"✓ {series_id}: {title} = ${value:,.0f}")

# If we found data, create the JavaScript arrays
if found_data:
    print("\n\nGenerating JavaScript code for the data...")
    print("```javascript")
    print("// Net worth by age group (in thousands)")
    print("const ageGroups = ['<35', '35-44', '45-54', '55-64', '65-74', '75+'];")
    print("const netWorthByAge = [")
    for age_group in ['Less than 35', '35-44', '45-54', '55-64', '65-74', '75+']:
        for key, value in found_data.items():
            if age_group in key:
                print(f"  {value/1000:.1f},  // {key}")
                break
    print("];")
    print("```")