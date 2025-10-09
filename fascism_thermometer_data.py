import pandas as pd
import json
import numpy as np

# Compile comprehensive historical US data on all four ingredients
# to create a "fascism risk thermometer"

print("=== FASCISM THERMOMETER: US HISTORICAL DATA ===\n")
print("Compiling data on four ingredients that precede extremist movements:\n")

# ============================================================================
# INGREDIENT 1: ECONOMIC CRISIS (Unemployment Rate)
# ============================================================================
print("1. ECONOMIC CRISIS (Unemployment Rate)")
print("-" * 60)

# Historical unemployment data
unemployment_data = {
    'year': [
        1929, 1930, 1931, 1932, 1933, 1934, 1935, 1940, 1950,
        1960, 1970, 1980, 1990, 2000, 2007, 2008, 2009, 2010,
        2015, 2019, 2020, 2021, 2022, 2023, 2024, 2025
    ],
    'unemployment_rate': [
        3.2,   # 1929 - pre-crash
        8.7,   # 1930 - crash begins
        15.9,  # 1931 - deepening
        23.6,  # 1932 - severe
        24.9,  # 1933 - PEAK
        21.7,  # 1934 - still high
        20.1,  # 1935 - gradual recovery
        14.6,  # 1940 - WWII mobilization
        5.3,   # 1950 - post-war prosperity
        5.5,   # 1960 - stable
        4.9,   # 1970 - pre-stagflation
        7.1,   # 1980 - recession
        5.6,   # 1990 - recession
        4.0,   # 2000 - dot-com boom
        4.6,   # 2007 - pre-crisis
        5.8,   # 2008 - financial crisis begins
        9.3,   # 2009 - PEAK of Great Recession
        9.6,   # 2010 - still elevated
        5.3,   # 2015 - recovery
        3.7,   # 2019 - pre-pandemic
        8.1,   # 2020 - pandemic spike
        5.4,   # 2021 - recovery
        3.6,   # 2022 - low
        3.6,   # 2023 - low
        4.0,   # 2024 - current
        4.2    # 2025 - current estimate
    ],
    'notes': [
        'Pre-crash', 'Crash begins', 'Deepening', 'Severe', 'PEAK Depression',
        'Still high', 'Recovery', 'WWII mobilization', 'Post-war',
        'Stable', 'Pre-stagflation', 'Recession', 'Recession', 'Boom',
        'Pre-crisis', 'Crisis begins', 'PEAK Recession', 'Elevated',
        'Recovery', 'Pre-pandemic', 'Pandemic', 'Recovery', 'Low', 'Low',
        'Current', 'Current'
    ]
}

df_unemp = pd.DataFrame(unemployment_data)
print(df_unemp.to_string(index=False))
print(f"\nGreat Depression Peak: {df_unemp[df_unemp['year']==1933]['unemployment_rate'].values[0]:.1f}%")
print(f"Great Recession Peak: {df_unemp[df_unemp['year']==2009]['unemployment_rate'].values[0]:.1f}%")
print(f"Current (2025): {df_unemp[df_unemp['year']==2025]['unemployment_rate'].values[0]:.1f}%")

# ============================================================================
# INGREDIENT 2: STATUS THREAT (National Pride / Perceived Standing)
# ============================================================================
print("\n\n2. STATUS THREAT (National Pride)")
print("-" * 60)

# National pride data - proxy for status threat
# Before 2001, we use proxy indicators and historical context
national_pride_data = {
    'year': [
        1945, 1960, 1970, 1980, 1990, 2001, 2003, 2005, 2007, 2009,
        2011, 2013, 2015, 2017, 2019, 2021, 2023, 2024, 2025
    ],
    'extremely_proud_pct': [
        # Estimated pre-2001 based on historical context
        80,  # 1945 - Post-WWII victory, highest national confidence
        75,  # 1960 - Cold War confidence, economic boom
        65,  # 1970 - Vietnam, civil unrest damage confidence
        55,  # 1980 - Iran hostage crisis, stagflation
        60,  # 1990 - End of Cold War, Gulf War victory
        # Actual Gallup data 2001-2025
        55, 70, 65, 60, 57, 57, 57, 54, 47, 45, 39, 39, 38, 38
    ],
    'data_source': [
        'estimate', 'estimate', 'estimate', 'estimate', 'estimate',
        'Gallup', 'Gallup', 'Gallup', 'Gallup', 'Gallup', 'Gallup',
        'Gallup', 'Gallup', 'Gallup', 'Gallup', 'Gallup', 'Gallup',
        'Gallup', 'Gallup'
    ]
}

df_pride = pd.DataFrame(national_pride_data)
print(df_pride.to_string(index=False))
print(f"\nPost-WWII Peak (1945): {df_pride[df_pride['year']==1945]['extremely_proud_pct'].values[0]:.0f}%")
print(f"Post-9/11 Peak (2003): {df_pride[df_pride['year']==2003]['extremely_proud_pct'].values[0]:.0f}%")
print(f"Current (2025): {df_pride[df_pride['year']==2025]['extremely_proud_pct'].values[0]:.0f}%")
print(f"Decline 2003-2025: {df_pride[df_pride['year']==2003]['extremely_proud_pct'].values[0] - df_pride[df_pride['year']==2025]['extremely_proud_pct'].values[0]:.0f} percentage points")

# ============================================================================
# INGREDIENT 3: CULTURAL BACKLASH (Foreign-Born Population %)
# ============================================================================
print("\n\n3. CULTURAL BACKLASH (Foreign-Born Population %)")
print("-" * 60)

# Foreign-born population percentage
foreign_born_data = {
    'year': [
        1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000,
        2010, 2015, 2020, 2023, 2025
    ],
    'foreign_born_pct': [
        13.2,  # 1920 - Peak immigration era
        11.6,  # 1930 - Starting to decline
        8.8,   # 1940 - Immigration restrictions
        6.9,   # 1950 - Historic low point approaching
        5.4,   # 1960 - Lowest point
        4.7,   # 1970 - Still very low
        6.2,   # 1980 - Beginning to rise
        7.9,   # 1990 - Increasing
        11.1,  # 2000 - Major increase
        12.9,  # 2010 - Continuing rise
        13.5,  # 2015 - Near historical peak
        13.9,  # 2020 - At historical peak levels
        14.3,  # 2023 - estimate
        14.5   # 2025 - estimate (ongoing)
    ],
    'notes': [
        'Peak era', 'Declining', 'Restrictions', 'Historic low',
        'Lowest point', 'Still low', 'Rising', 'Increasing',
        'Major increase', 'Continuing', 'Near peak', 'Peak levels',
        'Estimate', 'Estimate'
    ]
}

df_foreign = pd.DataFrame(foreign_born_data)
print(df_foreign.to_string(index=False))
print(f"\nHistoric Low (1970): {df_foreign[df_foreign['year']==1970]['foreign_born_pct'].values[0]:.1f}%")
print(f"Historic Peak (1920): {df_foreign[df_foreign['year']==1920]['foreign_born_pct'].values[0]:.1f}%")
print(f"Current (2025): {df_foreign[df_foreign['year']==2025]['foreign_born_pct'].values[0]:.1f}%")

# ============================================================================
# INGREDIENT 4: INSTITUTIONAL TRUST (Trust in Government)
# ============================================================================
print("\n\n4. INSTITUTIONAL TRUST (Trust in Government)")
print("-" * 60)

# Trust in government to do what is right "always" or "most of the time"
trust_govt_data = {
    'year': [
        1958, 1964, 1970, 1974, 1980, 1984, 1990, 1994, 1998, 2000,
        2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020,
        2022, 2024, 2025
    ],
    'trust_govt_pct': [
        73,  # 1958 - High trust era begins
        77,  # 1964 - PEAK trust
        54,  # 1970 - Vietnam erosion
        36,  # 1974 - Watergate collapse
        25,  # 1980 - Carter malaise
        44,  # 1984 - Reagan recovery
        28,  # 1990 - Decline
        21,  # 1994 - Low point
        40,  # 1998 - Clinton boom
        44,  # 2000 - Peak of 90s recovery
        40,  # 2002 - Post-9/11 rally fading
        47,  # 2004 - Bush re-election
        30,  # 2006 - Iraq War fatigue
        24,  # 2008 - Financial crisis
        22,  # 2010 - Tea Party era
        19,  # 2012 - Historic low
        19,  # 2014 - Continued low
        20,  # 2016 - Trump election
        17,  # 2018 - Polarization
        20,  # 2020 - Pandemic volatility
        20,  # 2022 - Continued low
        23,  # 2024 - Slight uptick
        22   # 2025 - Current estimate
    ],
    'notes': [
        'High trust', 'PEAK', 'Vietnam', 'Watergate', 'Malaise',
        'Reagan recovery', 'Decline', 'Low', 'Clinton boom', 'Peak 90s',
        '9/11 fading', 'Bush', 'Iraq fatigue', 'Financial crisis',
        'Tea Party', 'Historic low', 'Low', 'Trump', 'Polarization',
        'Pandemic', 'Low', 'Slight uptick', 'Current'
    ]
}

df_trust = pd.DataFrame(trust_govt_data)
print(df_trust.to_string(index=False))
print(f"\nHistoric Peak (1964): {df_trust[df_trust['year']==1964]['trust_govt_pct'].values[0]:.0f}%")
print(f"Watergate Low (1974): {df_trust[df_trust['year']==1974]['trust_govt_pct'].values[0]:.0f}%")
print(f"Current (2025): {df_trust[df_trust['year']==2025]['trust_govt_pct'].values[0]:.0f}%")
print(f"Decline 1964-2025: {df_trust[df_trust['year']==1964]['trust_govt_pct'].values[0] - df_trust[df_trust['year']==2025]['trust_govt_pct'].values[0]:.0f} percentage points")

# ============================================================================
# CREATE COMPOSITE "FASCISM RISK INDEX"
# ============================================================================
print("\n\n" + "=" * 60)
print("COMPOSITE FASCISM RISK INDEX")
print("=" * 60)

# Merge all data on common years
# Start with years we want to analyze
analysis_years = sorted(list(set(
    unemployment_data['year'] +
    national_pride_data['year'] +
    foreign_born_data['year'] +
    trust_govt_data['year']
)))

# Create comprehensive dataframe with all ingredients
def get_value_for_year(df, year_col, value_col, target_year):
    """Get value for year, or interpolate if missing"""
    if target_year in df[year_col].values:
        return df[df[year_col] == target_year][value_col].values[0]
    else:
        # Linear interpolation
        before = df[df[year_col] < target_year]
        after = df[df[year_col] > target_year]
        if len(before) > 0 and len(after) > 0:
            y1 = before.iloc[-1][value_col]
            y2 = after.iloc[0][value_col]
            x1 = before.iloc[-1][year_col]
            x2 = after.iloc[0][year_col]
            return y1 + (y2 - y1) * (target_year - x1) / (x2 - x1)
        return None

composite_data = []
for year in analysis_years:
    unemp = get_value_for_year(df_unemp, 'year', 'unemployment_rate', year)
    pride = get_value_for_year(df_pride, 'year', 'extremely_proud_pct', year)
    foreign = get_value_for_year(df_foreign, 'year', 'foreign_born_pct', year)
    trust = get_value_for_year(df_trust, 'year', 'trust_govt_pct', year)

    if all(x is not None for x in [unemp, pride, foreign, trust]):
        composite_data.append({
            'year': year,
            'unemployment': unemp,
            'national_pride': pride,
            'foreign_born': foreign,
            'trust_govt': trust
        })

df_composite = pd.DataFrame(composite_data)

# Normalize each ingredient to 0-100 scale where 100 = highest risk
# For unemployment: higher = more risk
# For national pride: lower = more risk (invert)
# For foreign-born: rapid change = risk (measure as deviation from historical mean)
# For trust: lower = more risk (invert)

historical_foreign_mean = df_foreign['foreign_born_pct'].mean()

df_composite['unemp_risk'] = (df_composite['unemployment'] / df_composite['unemployment'].max()) * 100
df_composite['pride_risk'] = ((df_composite['national_pride'].max() - df_composite['national_pride']) /
                               (df_composite['national_pride'].max() - df_composite['national_pride'].min())) * 100
df_composite['foreign_risk'] = (abs(df_composite['foreign_born'] - historical_foreign_mean) /
                                abs(df_foreign['foreign_born_pct'] - historical_foreign_mean).max()) * 100
df_composite['trust_risk'] = ((df_composite['trust_govt'].max() - df_composite['trust_govt']) /
                              (df_composite['trust_govt'].max() - df_composite['trust_govt'].min())) * 100

# Composite index: weighted average
# Based on meta-analysis findings: Economic ~33%, other factors ~67%
# Split remaining 67% among status (30%), cultural (17%), institutional (20%)
df_composite['fascism_risk_index'] = (
    0.33 * df_composite['unemp_risk'] +
    0.30 * df_composite['pride_risk'] +
    0.17 * df_composite['foreign_risk'] +
    0.20 * df_composite['trust_risk']
)

print("\nFASCISM RISK INDEX (0-100, higher = greater risk):\n")
print(df_composite[['year', 'fascism_risk_index', 'unemployment', 'national_pride', 'foreign_born', 'trust_govt']].to_string(index=False))

# Key periods
print(f"\n\nKEY PERIODS:")

# Check which years we have
if 1933 in df_composite['year'].values:
    great_depression = df_composite[df_composite['year'] == 1933]['fascism_risk_index'].values[0]
    print(f"Great Depression (1933): {great_depression:.1f} / 100")
else:
    print("Great Depression (1933): No complete data (trust surveys didn't exist)")

if 1980 in df_composite['year'].values:
    crisis_1980 = df_composite[df_composite['year'] == 1980]['fascism_risk_index'].values[0]
    print(f"1980 Crisis (stagflation): {crisis_1980:.1f} / 100")

if 2009 in df_composite['year'].values:
    great_recession = df_composite[df_composite['year'] == 2009]['fascism_risk_index'].values[0]
    print(f"Great Recession (2009): {great_recession:.1f} / 100")

if 2025 in df_composite['year'].values:
    current = df_composite[df_composite['year'] == 2025]['fascism_risk_index'].values[0]
    print(f"Current (2025): {current:.1f} / 100")

# Save to JSON for visualization
output_data = {
    'unemployment': unemployment_data,
    'national_pride': national_pride_data,
    'foreign_born': foreign_born_data,
    'trust_government': trust_govt_data,
    'composite_index': df_composite.to_dict('list')
}

with open('fascism_thermometer_data.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("\n\nData saved to fascism_thermometer_data.json")

# Interpretation guide
print("\n\n" + "=" * 60)
print("INTERPRETATION GUIDE")
print("=" * 60)
print("""
The Fascism Risk Index combines four key ingredients:

1. Economic Crisis (33% weight): Unemployment rate
   - Higher unemployment = higher risk

2. Status Threat (30% weight): National pride decline
   - Lower national pride = higher risk

3. Cultural Backlash (17% weight): Demographic change
   - Rapid change from historical norm = higher risk

4. Institutional Trust (20% weight): Trust in government
   - Lower trust = higher risk

Risk Levels:
  0-30:  Low risk - Stable conditions
  30-50: Moderate risk - Some warning signs
  50-70: High risk - Multiple ingredients present
  70-100: Extreme risk - All ingredients combining

Historical Context:
  Great Depression (1933): All four ingredients at extreme levels
  Great Recession (2009): Economic crisis + institutional collapse
  Current (2025): ?
""")
