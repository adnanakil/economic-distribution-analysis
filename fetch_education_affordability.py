import requests
import pandas as pd
from datetime import datetime

# FRED API key (using public data, no key needed for basic access)
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

# Education cost indicators
indicators = {
    'CUSR0000SAE1': 'CPI: Education',
    'CUUR0000SEEB01': 'CPI: College Tuition and Fees',
    'CUSR0000SAE2': 'CPI: Tuition, Other School Fees, and Childcare',
    'CPIEDUSL': 'CPI: Education Services',
    'AHETPI': 'Average Hourly Earnings (Private)',
    'MEHOINUSA672N': 'Real Median Household Income'
}

print("Fetching education affordability data from FRED...\n")

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

    # Calculate affordability metrics - normalize to 1985 = 100 for comparison
    base_year = merged_df[merged_df['date'].dt.year == 1985]

    if not base_year.empty and 'CUUR0000SEEB01' in merged_df.columns and 'AHETPI' in merged_df.columns:
        base_tuition = base_year['CUUR0000SEEB01'].mean()
        base_wage = base_year['AHETPI'].mean()

        if pd.notna(base_tuition) and pd.notna(base_wage):
            merged_df['tuition_indexed'] = (merged_df['CUUR0000SEEB01'] / base_tuition) * 100
            merged_df['wage_indexed'] = (merged_df['AHETPI'] / base_wage) * 100
            merged_df['education_burden'] = merged_df['tuition_indexed'] / merged_df['wage_indexed']

    # Save to CSV
    output_file = 'education_affordability_data.csv'
    merged_df.to_csv(output_file, index=False)
    print(f"\nData saved to {output_file}")

    # Show summary statistics
    print("\n=== EDUCATION AFFORDABILITY SUMMARY ===")

    if 'CUUR0000SEEB01' in merged_df.columns:
        recent = merged_df[merged_df['CUUR0000SEEB01'].notna()].tail(1)
        first = merged_df[merged_df['CUUR0000SEEB01'].notna()].head(1)

        if not recent.empty and not first.empty:
            current_cpi = recent['CUUR0000SEEB01'].iloc[0]
            initial_cpi = first['CUUR0000SEEB01'].iloc[0]
            print(f"\nCollege Tuition CPI:")
            print(f"  First recorded ({first['date'].iloc[0].date()}): {initial_cpi:.2f}")
            print(f"  Current: {current_cpi:.2f}")
            print(f"  Total increase: {((current_cpi/initial_cpi - 1) * 100):.1f}%")

    if 'education_burden' in merged_df.columns:
        recent_burden = merged_df[merged_df['education_burden'].notna()].tail(1)
        if not recent_burden.empty:
            burden = recent_burden['education_burden'].iloc[0]
            print(f"\nEducation Cost vs Wages (1985 = 1.00):")
            print(f"  Current burden index: {burden:.2f}")
            print(f"  Interpretation: College tuition has grown {((burden - 1) * 100):.1f}% faster than wages since 1985")

    # Calculate wage growth vs tuition growth
    if 'CUUR0000SEEB01' in merged_df.columns and 'AHETPI' in merged_df.columns:
        data_1985 = merged_df[merged_df['date'].dt.year == 1985]
        data_recent = merged_df[merged_df['date'].dt.year == 2024]

        if not data_1985.empty and not data_recent.empty:
            tuition_1985 = data_1985['CUUR0000SEEB01'].mean()
            tuition_2024 = data_recent['CUUR0000SEEB01'].mean()
            wage_1985 = data_1985['AHETPI'].mean()
            wage_2024 = data_recent['AHETPI'].mean()

            if all(pd.notna([tuition_1985, tuition_2024, wage_1985, wage_2024])):
                tuition_growth = ((tuition_2024/tuition_1985 - 1) * 100)
                wage_growth = ((wage_2024/wage_1985 - 1) * 100)
                print(f"\nGrowth Comparison (1985-2024):")
                print(f"  College tuition growth: {tuition_growth:.1f}%")
                print(f"  Wage growth: {wage_growth:.1f}%")
                print(f"  Gap: {(tuition_growth - wage_growth):.1f} percentage points")
