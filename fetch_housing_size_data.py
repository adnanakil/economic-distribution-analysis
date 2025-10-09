import requests
import pandas as pd

# Try to get housing characteristics data from FRED
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

indicators = {
    'MEDAVGSQFEET': 'Median Square Feet of Floor Area in New Single-Family Houses',
    'AVGAVGSQFEET': 'Average Square Feet of Floor Area in New Single-Family Houses',
    'MSPNHSUS': 'Median Sales Price of New Houses Sold',
    'ASPNHSUS': 'Average Sales Price of New Houses Sold'
}

print("Fetching housing size/quality data from FRED...\n")

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
        print(f"  First value: {df[code].iloc[0]}")
        print(f"  Latest value: {df[code].iloc[-1]}")
        print()
    except Exception as e:
        print(f"✗ Failed to fetch {name} ({code}): {e}\n")

# Merge and analyze
if len(data_frames) > 0:
    merged_df = None
    for code, df in data_frames.items():
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='date', how='outer')

    merged_df = merged_df.sort_values('date')

    # Calculate price per square foot over time
    if 'MSPNHSUS' in merged_df.columns and 'MEDAVGSQFEET' in merged_df.columns:
        merged_df['price_per_sqft_median'] = merged_df['MSPNHSUS'] / merged_df['MEDAVGSQFEET']

    if 'ASPNHSUS' in merged_df.columns and 'AVGAVGSQFEET' in merged_df.columns:
        merged_df['price_per_sqft_avg'] = merged_df['ASPNHSUS'] / merged_df['AVGAVGSQFEET']

    merged_df.to_csv('housing_size_analysis.csv', index=False)
    print("\nData saved to housing_size_analysis.csv")

    # Summary
    print("\n=== HOUSING SIZE ANALYSIS ===")

    if 'MEDAVGSQFEET' in merged_df.columns:
        first_valid = merged_df[merged_df['MEDAVGSQFEET'].notna()].iloc[0]
        last_valid = merged_df[merged_df['MEDAVGSQFEET'].notna()].iloc[-1]

        first_sqft = first_valid['MEDAVGSQFEET']
        last_sqft = last_valid['MEDAVGSQFEET']
        sqft_growth = ((last_sqft / first_sqft - 1) * 100)

        print(f"\nMedian Home Size:")
        print(f"  {first_valid['date'].date()}: {first_sqft:,.0f} sq ft")
        print(f"  {last_valid['date'].date()}: {last_sqft:,.0f} sq ft")
        print(f"  Growth: {sqft_growth:.1f}%")

        if 'MSPNHSUS' in merged_df.columns:
            first_price = first_valid['MSPNHSUS']
            last_price = last_valid['MSPNHSUS']
            price_growth = ((last_price / first_price - 1) * 100)

            print(f"\nMedian Home Price (same period):")
            print(f"  {first_valid['date'].date()}: ${first_price:,.0f}")
            print(f"  {last_valid['date'].date()}: ${last_price:,.0f}")
            print(f"  Growth: {price_growth:.1f}%")

            print(f"\nSize-Adjusted Analysis:")
            print(f"  Raw price growth: {price_growth:.1f}%")
            print(f"  Home size growth: {sqft_growth:.1f}%")
            print(f"  Excess price growth: {(price_growth - sqft_growth):.1f} percentage points")

    if 'price_per_sqft_median' in merged_df.columns:
        price_sqft_data = merged_df[merged_df['price_per_sqft_median'].notna()]
        if len(price_sqft_data) > 0:
            first_ps = price_sqft_data.iloc[0]
            last_ps = price_sqft_data.iloc[-1]

            ps_growth = ((last_ps['price_per_sqft_median'] / first_ps['price_per_sqft_median'] - 1) * 100)

            print(f"\nPrice Per Square Foot:")
            print(f"  {first_ps['date'].date()}: ${first_ps['price_per_sqft_median']:.2f}/sq ft")
            print(f"  {last_ps['date'].date()}: ${last_ps['price_per_sqft_median']:.2f}/sq ft")
            print(f"  Growth: {ps_growth:.1f}%")
