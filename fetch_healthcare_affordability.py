import requests
import pandas as pd
from datetime import datetime

# FRED API key (using public data, no key needed for basic access)
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

# Healthcare cost indicators
indicators = {
    'CPIMEDSL': 'CPI: Medical Care',
    'CPIHOSNS': 'CPI: Hospital Services',
    'CUSR0000SEMD': 'CPI: Prescription Drugs',
    'CUSR0000SS47014': 'CPI: Health Insurance',
    'CUSR0000SEMF01': 'CPI: Physician Services',
    'AHETPI': 'Average Hourly Earnings (Private)',
    'MEHOINUSA672N': 'Real Median Household Income'
}

print("Fetching healthcare affordability data from FRED...\n")

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

    if not base_year.empty and 'CPIMEDSL' in merged_df.columns and 'AHETPI' in merged_df.columns:
        base_medical = base_year['CPIMEDSL'].mean()
        base_wage = base_year['AHETPI'].mean()

        if pd.notna(base_medical) and pd.notna(base_wage):
            merged_df['medical_indexed'] = (merged_df['CPIMEDSL'] / base_medical) * 100
            merged_df['wage_indexed'] = (merged_df['AHETPI'] / base_wage) * 100
            merged_df['healthcare_burden'] = merged_df['medical_indexed'] / merged_df['wage_indexed']

    # Save to CSV
    output_file = 'healthcare_affordability_data.csv'
    merged_df.to_csv(output_file, index=False)
    print(f"\nData saved to {output_file}")

    # Show summary statistics
    print("\n=== HEALTHCARE AFFORDABILITY SUMMARY ===")

    if 'CPIMEDSL' in merged_df.columns:
        recent = merged_df[merged_df['CPIMEDSL'].notna()].tail(1)
        first = merged_df[merged_df['CPIMEDSL'].notna()].head(1)

        if not recent.empty and not first.empty:
            current_cpi = recent['CPIMEDSL'].iloc[0]
            initial_cpi = first['CPIMEDSL'].iloc[0]
            print(f"\nMedical Care CPI:")
            print(f"  First recorded ({first['date'].iloc[0].date()}): {initial_cpi:.2f}")
            print(f"  Current: {current_cpi:.2f}")
            print(f"  Total increase: {((current_cpi/initial_cpi - 1) * 100):.1f}%")

    if 'healthcare_burden' in merged_df.columns:
        recent_burden = merged_df[merged_df['healthcare_burden'].notna()].tail(1)
        if not recent_burden.empty:
            burden = recent_burden['healthcare_burden'].iloc[0]
            print(f"\nHealthcare Cost vs Wages (1980 = 1.00):")
            print(f"  Current burden index: {burden:.2f}")
            print(f"  Interpretation: Healthcare costs have grown {((burden - 1) * 100):.1f}% faster than wages since 1980")
