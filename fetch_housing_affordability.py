import requests
import pandas as pd
from datetime import datetime

# FRED API key (using public data, no key needed for basic access)
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

# Housing affordability indicators
indicators = {
    'CSUSHPISA': 'S&P/Case-Shiller U.S. National Home Price Index',
    'MSPUS': 'Median Sales Price of Houses Sold',
    'MEHOINUSA672N': 'Real Median Household Income',
    'CPIHOSSL': 'CPI: Housing',
    'CUSR0000SEHA': 'CPI: Rent of Primary Residence',
    'MORTGAGE30US': '30-Year Fixed Rate Mortgage Average',
    'LES1252881600Q': 'Homeownership Rate'
}

print("Fetching housing affordability data from FRED...\n")

data_frames = {}

for code, name in indicators.items():
    try:
        url = f"{base_url}?id={code}"
        df = pd.read_csv(url)
        df.columns = ['date', code]
        df['date'] = pd.to_datetime(df['date'])
        data_frames[code] = df
        print(f"✓ {name} ({code})")
        print(f"  Range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"  Latest value: {df[code].iloc[-1]}")
        print()
    except Exception as e:
        print(f"✗ Failed to fetch {name} ({code}): {e}\n")

# Merge all data on date
if data_frames:
    merged_df = None
    for code, df in data_frames.items():
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='date', how='outer')

    merged_df = merged_df.sort_values('date')

    # Calculate affordability metrics
    if 'MSPUS' in merged_df.columns and 'MEHOINUSA672N' in merged_df.columns:
        merged_df['price_to_income_ratio'] = merged_df['MSPUS'] / merged_df['MEHOINUSA672N']

    # Save to CSV
    output_file = 'housing_affordability_data.csv'
    merged_df.to_csv(output_file, index=False)
    print(f"\nData saved to {output_file}")

    # Show summary statistics
    print("\n=== HOUSING AFFORDABILITY SUMMARY ===")
    if 'price_to_income_ratio' in merged_df.columns:
        recent_data = merged_df.dropna(subset=['price_to_income_ratio']).tail(1)
        historical_data = merged_df.dropna(subset=['price_to_income_ratio'])

        if not recent_data.empty and not historical_data.empty:
            current_ratio = recent_data['price_to_income_ratio'].iloc[0]
            avg_ratio = historical_data['price_to_income_ratio'].mean()
            print(f"\nHome Price to Income Ratio:")
            print(f"  Current: {current_ratio:.2f}")
            print(f"  Historical average: {avg_ratio:.2f}")
            print(f"  Change: {((current_ratio/avg_ratio - 1) * 100):.1f}% vs historical average")
