import requests
import pandas as pd
from datetime import datetime

# FRED API key (using public data, no key needed for basic access)
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

# Food and essentials cost indicators
indicators = {
    'CPIUFDSL': 'CPI: Food',
    'CPIUFDNS': 'CPI: Food at Home',
    'CPILFENS': 'CPI: Food Away from Home',
    'CPIEALL': 'CPI: Energy',
    'CPIENGSL': 'CPI: Energy Goods and Services',
    'CUSR0000SAC': 'CPI: Commodities',
    'CPIAUCSL': 'CPI: All Items (Total Inflation)',
    'AHETPI': 'Average Hourly Earnings (Private)',
    'MEHOINUSA672N': 'Real Median Household Income'
}

print("Fetching food & essentials affordability data from FRED...\n")

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

    # Calculate affordability metrics - normalize to 1980 = 100 for comparison
    base_year = merged_df[merged_df['date'].dt.year == 1980]

    if not base_year.empty and 'CPIUFDSL' in merged_df.columns and 'AHETPI' in merged_df.columns:
        base_food = base_year['CPIUFDSL'].mean()
        base_wage = base_year['AHETPI'].mean()

        if pd.notna(base_food) and pd.notna(base_wage):
            merged_df['food_indexed'] = (merged_df['CPIUFDSL'] / base_food) * 100
            merged_df['wage_indexed'] = (merged_df['AHETPI'] / base_wage) * 100
            merged_df['food_burden'] = merged_df['food_indexed'] / merged_df['wage_indexed']

    # Save to CSV
    output_file = 'food_essentials_affordability_data.csv'
    merged_df.to_csv(output_file, index=False)
    print(f"\nData saved to {output_file}")

    # Show summary statistics
    print("\n=== FOOD & ESSENTIALS AFFORDABILITY SUMMARY ===")

    # Compare 1980 to 2024
    data_1980 = merged_df[merged_df['date'].dt.year == 1980]
    data_2024 = merged_df[merged_df['date'].dt.year == 2024]

    if not data_1980.empty and not data_2024.empty:
        # Food
        if 'CPIUFDSL' in merged_df.columns:
            food_1980 = data_1980['CPIUFDSL'].mean()
            food_2024 = data_2024['CPIUFDSL'].mean()
            wage_1980 = data_1980['AHETPI'].mean()
            wage_2024 = data_2024['AHETPI'].mean()

            food_growth = ((food_2024/food_1980 - 1) * 100)
            wage_growth = ((wage_2024/wage_1980 - 1) * 100)

            print(f"\nFood CPI (1980-2024):")
            print(f"  1980: {food_1980:.1f}")
            print(f"  2024: {food_2024:.1f}")
            print(f"  Growth: {food_growth:.1f}%")
            print(f"  vs Wage growth: {wage_growth:.1f}%")
            print(f"  Gap: {(food_growth - wage_growth):.1f} percentage points")

        # Total CPI
        if 'CPIAUCSL' in merged_df.columns:
            cpi_1980 = data_1980['CPIAUCSL'].mean()
            cpi_2024 = data_2024['CPIAUCSL'].mean()
            cpi_growth = ((cpi_2024/cpi_1980 - 1) * 100)

            print(f"\nOverall CPI (1980-2024):")
            print(f"  Growth: {cpi_growth:.1f}%")
            print(f"  vs Wage growth: {wage_growth:.1f}%")
            print(f"  Real wage change: {(wage_growth - cpi_growth):.1f} percentage points")

    # Food burden
    if 'food_burden' in merged_df.columns:
        recent_burden = merged_df[merged_df['food_burden'].notna()].tail(1)
        if not recent_burden.empty:
            burden = recent_burden['food_burden'].iloc[0]
            print(f"\nFood Cost vs Wages (1980 = 1.00):")
            print(f"  Current burden index: {burden:.2f}")
            if burden > 1:
                print(f"  Interpretation: Food costs have grown {((burden - 1) * 100):.1f}% faster than wages since 1980")
            else:
                print(f"  Interpretation: Food costs have grown {((1 - burden) * 100):.1f}% slower than wages since 1980")
