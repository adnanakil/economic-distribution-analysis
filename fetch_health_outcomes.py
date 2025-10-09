import requests
import pandas as pd
from datetime import datetime

# FRED API for health outcome metrics
base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

indicators = {
    'SPDYNLE00INUSA': 'Life Expectancy at Birth (Total)',
    'SPDYNIM01INUSA': 'Infant Mortality Rate',
}

print("Fetching health outcome data from FRED...\n")

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

# Merge all data
if data_frames:
    merged_df = None
    for code, df in data_frames.items():
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='date', how='outer')

    merged_df = merged_df.sort_values('date')
    merged_df.to_csv('health_outcomes_data.csv', index=False)
    print(f"\nData saved to health_outcomes_data.csv")

# Now load our healthcare cost data and merge
healthcare_df = pd.read_csv('healthcare_affordability_data.csv')
healthcare_df['date'] = pd.to_datetime(healthcare_df['date'])

# Merge with health outcomes
combined = pd.merge(merged_df, healthcare_df, on='date', how='inner')

# Calculate cost per year of life expectancy
if 'SPDYNLE00INUSA' in combined.columns and 'CPIMEDSL' in combined.columns:
    # Get 1980 baseline
    baseline_1980 = combined[combined['date'].dt.year == 1980].iloc[0] if len(combined[combined['date'].dt.year == 1980]) > 0 else None

    if baseline_1980 is not None:
        life_exp_1980 = baseline_1980['SPDYNLE00INUSA']
        medical_cpi_1980 = baseline_1980['CPIMEDSL']

        combined['life_exp_gained'] = combined['SPDYNLE00INUSA'] - life_exp_1980
        combined['medical_cost_increase'] = (combined['CPIMEDSL'] / medical_cpi_1980 - 1) * 100

        # Cost increase per year of life gained
        combined['cost_per_life_year'] = combined['medical_cost_increase'] / combined['life_exp_gained']

        print("\n=== HEALTHCARE COST VS LIFE EXPECTANCY ===")
        print(f"\n1980 Baseline:")
        print(f"  Life expectancy: {life_exp_1980:.1f} years")
        print(f"  Medical CPI: {medical_cpi_1980:.1f}")

        # Get most recent data
        recent = combined[combined['date'].dt.year >= 2020].iloc[-1] if len(combined[combined['date'].dt.year >= 2020]) > 0 else combined.iloc[-1]

        print(f"\n{recent['date'].year} Current:")
        print(f"  Life expectancy: {recent['SPDYNLE00INUSA']:.1f} years")
        print(f"  Gain: +{recent['life_exp_gained']:.1f} years since 1980")
        print(f"  Medical cost increase: +{recent['medical_cost_increase']:.0f}% since 1980")
        print(f"  Cost increase per year of life gained: {recent['cost_per_life_year']:.0f}%")

        print(f"\nInterpretation:")
        print(f"  Americans live {recent['life_exp_gained']:.1f} years longer than in 1980")
        print(f"  Healthcare costs increased {recent['medical_cost_increase']:.0f}%")
        print(f"  That's {recent['cost_per_life_year']:.0f}% cost increase per additional year of life")

# Infant mortality analysis
if 'SPDYNIM01INUSA' in combined.columns:
    baseline_1980_im = combined[combined['date'].dt.year == 1980].iloc[0] if len(combined[combined['date'].dt.year == 1980]) > 0 else None

    if baseline_1980_im is not None:
        im_1980 = baseline_1980_im['SPDYNIM01INUSA']
        recent_im = combined[combined['date'].dt.year >= 2020].iloc[-1] if len(combined[combined['date'].dt.year >= 2020]) > 0 else combined.iloc[-1]

        im_reduction = ((im_1980 - recent_im['SPDYNIM01INUSA']) / im_1980) * 100

        print(f"\n=== INFANT MORTALITY ===")
        print(f"  1980: {im_1980:.1f} deaths per 1,000 live births")
        print(f"  {recent_im['date'].year}: {recent_im['SPDYNIM01INUSA']:.1f} deaths per 1,000 live births")
        print(f"  Reduction: {im_reduction:.0f}%")

combined.to_csv('healthcare_outcomes_normalized.csv', index=False)
print(f"\nCombined data saved to healthcare_outcomes_normalized.csv")
