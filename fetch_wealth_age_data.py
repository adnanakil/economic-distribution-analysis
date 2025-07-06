#!/usr/bin/env python3
import requests
import json

API_KEY = 'a858d6aeb49035d915e8424430998b86'
BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# Based on Fed DFA documentation, age group series for net worth
# These are educated guesses based on DFA naming patterns
potential_series = {
    # Net worth levels by age of reference person
    'WFRBLN40024': 'Net Worth - Under 35',  
    'WFRBLN40027': 'Net Worth - 35-44',
    'WFRBLN40030': 'Net Worth - 45-54', 
    'WFRBLN40033': 'Net Worth - 55-64',
    'WFRBLN40036': 'Net Worth - 65-74',
    'WFRBLN40039': 'Net Worth - 75+',
    
    # Alternative naming pattern
    'WFRBLNA35': 'Net Worth - Under 35',
    'WFRBLNA3544': 'Net Worth - 35-44',
    'WFRBLNA4554': 'Net Worth - 45-54',
    'WFRBLNA5564': 'Net Worth - 55-64', 
    'WFRBLNA6574': 'Net Worth - 65-74',
    'WFRBLNA75': 'Net Worth - 75+',
}

def fetch_series(series_id):
    """Try to fetch a series from FRED API"""
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'limit': '1'  # Just check if it exists
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'observations' in data and len(data['observations']) > 0:
                return True
        return False
    except:
        return False

# Try to find valid series
print("Searching for wealth by age series on FRED...")
valid_series = {}

for series_id, description in potential_series.items():
    if fetch_series(series_id):
        valid_series[series_id] = description
        print(f"✓ Found: {series_id} - {description}")
    else:
        print(f"✗ Not found: {series_id}")

# Search for series with "age" in the description
print("\nSearching FRED for age-related wealth series...")
search_url = 'https://api.stlouisfed.org/fred/series/search'

# Try multiple search patterns
search_terms = [
    'net worth by age',
    'wealth age distributional financial',
    'DFA age household',
    'NWFRBLTHREF',  # Reference person age series
    'household net worth age of reference'
]

all_series = {}

for term in search_terms:
    search_params = {
        'search_text': term,
        'api_key': API_KEY,
        'file_type': 'json',
        'limit': '50'
    }
    
    response = requests.get(search_url, params=search_params)
    if response.status_code == 200:
        data = response.json()
        if 'seriess' in data:
            for series in data['seriess']:
                series_id = series['id']
                title = series['title']
                # Look for age-related wealth series
                if ('age' in title.lower() and 
                    ('wealth' in title.lower() or 'net worth' in title.lower()) and
                    series_id not in all_series):
                    all_series[series_id] = title

print(f"\nFound {len(all_series)} potential age-related wealth series:")
for series_id, title in sorted(all_series.items())[:20]:
    print(f"- {series_id}: {title}")

# Try specific DFA series patterns
print("\n\nTrying specific DFA patterns...")
dfa_patterns = [
    'NWFRBLTHREF',  # Net Worth by age of reference person
    'TNWFRBLTHREF',  # Total net worth by age ref
    'WFRBLTHREF'    # Wealth by age ref
]

for pattern in dfa_patterns:
    search_params = {
        'search_text': pattern,
        'api_key': API_KEY,
        'file_type': 'json',
        'limit': '50'
    }
    
    response = requests.get(search_url, params=search_params)
    if response.status_code == 200:
        data = response.json()
        if 'seriess' in data and len(data['seriess']) > 0:
            print(f"\nPattern '{pattern}' found {len(data['seriess'])} series:")
            for series in data['seriess'][:10]:
                print(f"- {series['id']}: {series['title']}")