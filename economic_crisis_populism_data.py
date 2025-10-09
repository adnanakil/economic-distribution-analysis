import pandas as pd
import json

# Compile historical data on economic crises and populist/fascist rise

# Case 1: Weimar Germany (1928-1933)
weimar_data = {
    'year': [1928, 1930, 1932, 1933],
    'unemployment_rate': [8.5, 15.3, 30.1, 25.9],
    'nazi_vote_share': [2.6, 18.3, 37.3, 43.9],  # July 1932 for the peak
    'country': ['Germany'] * 4
}

# Case 2: Greece (2009-2015) - Golden Dawn
greece_data = {
    'year': [2009, 2012, 2015],
    'unemployment_rate': [9.5, 24.3, 24.9],
    'golden_dawn_vote_share': [0.29, 6.97, 6.28],
    'country': ['Greece'] * 3
}

# Case 3: Hungary (2006-2014) - Jobbik
hungary_data = {
    'year': [2006, 2010, 2014],
    'unemployment_rate': [7.5, 11.2, 7.7],
    'jobbik_vote_share': [2.6, 16.7, 20.2],
    'country': ['Hungary'] * 3
}

# Case 4: Italy (1919-1924) - Fascist Party
# Limited data availability for early 1920s
italy_data = {
    'year': [1919, 1921, 1924],
    'unemployment_estimate': ['High', 'Very High', 'Moderate'],  # Qualitative due to data limitations
    'fascist_seats': [0, 35, 374],  # Parliamentary seats
    'note': 'Mussolini took power in 1922'
}

# Create comprehensive dataframe for visualization
df_weimar = pd.DataFrame(weimar_data)
df_greece = pd.DataFrame(greece_data)
df_hungary = pd.DataFrame(hungary_data)

print("=== WEIMAR GERMANY: UNEMPLOYMENT & NAZI VOTE SHARE ===")
print(df_weimar.to_string(index=False))
print(f"\nCorrelation: {df_weimar['unemployment_rate'].corr(df_weimar['nazi_vote_share']):.3f}")

print("\n=== GREECE: UNEMPLOYMENT & GOLDEN DAWN VOTE SHARE ===")
print(df_greece.to_string(index=False))
print(f"\nCorrelation: {df_greece['unemployment_rate'].corr(df_greece['golden_dawn_vote_share']):.3f}")

print("\n=== HUNGARY: UNEMPLOYMENT & JOBBIK VOTE SHARE ===")
print(df_hungary.to_string(index=False))
print(f"\nCorrelation: {df_hungary['unemployment_rate'].corr(df_hungary['jobbik_vote_share']):.3f}")

# Academic findings summary
print("\n=== ACADEMIC RESEARCH FINDINGS ===")
print("\n1. Economic Uncertainty Impact (PMC study):")
print("   - 1-point increase in World Uncertainty Index → +2.8pp populist vote")
print("   - 1-point increase in World Uncertainty Index → +1.96pp right-wing populist vote")
print("\n2. Unemployment Effect:")
print("   - 1pp increase in unemployment → +1pp populist vote (EU data)")
print("\n3. Debt Crisis (Hungary MIT study):")
print("   - 10pp increase in debt-to-income → +1.6 to 3.0pp far-right vote")
print("   - Foreign-currency debt spikes → +3pp far-right vote nationally")
print("\n4. Meta-analysis correlation:")
print("   - Partial correlation coefficient: 0.016 (after publication bias adjustment)")
print("   - Economic insecurity has positive causal effect on populism")

# Create combined dataset for visualization
combined_data = []

for _, row in df_weimar.iterrows():
    combined_data.append({
        'case': 'Weimar Germany',
        'year': int(row['year']),
        'unemployment': row['unemployment_rate'],
        'extremist_vote': row['nazi_vote_share'],
        'party': 'Nazi Party'
    })

for _, row in df_greece.iterrows():
    combined_data.append({
        'case': 'Greece',
        'year': int(row['year']),
        'unemployment': row['unemployment_rate'],
        'extremist_vote': row['golden_dawn_vote_share'],
        'party': 'Golden Dawn'
    })

for _, row in df_hungary.iterrows():
    combined_data.append({
        'case': 'Hungary',
        'year': int(row['year']),
        'unemployment': row['unemployment_rate'],
        'extremist_vote': row['jobbik_vote_share'],
        'party': 'Jobbik'
    })

df_combined = pd.DataFrame(combined_data)

# Calculate overall correlation
overall_corr = df_combined['unemployment'].corr(df_combined['extremist_vote'])
print(f"\n=== OVERALL CORRELATION ACROSS ALL CASES ===")
print(f"Unemployment vs Extremist Vote Share: {overall_corr:.3f}")

# Save to JSON for visualization
with open('economic_crisis_populism.json', 'w') as f:
    json.dump({
        'weimar': weimar_data,
        'greece': greece_data,
        'hungary': hungary_data,
        'combined': combined_data,
        'correlations': {
            'weimar': float(df_weimar['unemployment_rate'].corr(df_weimar['nazi_vote_share'])),
            'greece': float(df_greece['unemployment_rate'].corr(df_greece['golden_dawn_vote_share'])),
            'hungary': float(df_hungary['unemployment_rate'].corr(df_hungary['jobbik_vote_share'])),
            'overall': float(overall_corr)
        }
    }, f, indent=2)

print("\nData saved to economic_crisis_populism.json")

# Additional context data
print("\n=== DEMOCRACY DECLINE IN INTERWAR PERIOD ===")
print("1920: 24 fully democratic countries in Europe")
print("1939: 11 fully democratic countries in Europe")
print("Change: -54% decline in democracies")
print("\nMajor fascist takeovers:")
print("- Italy: 1922 (Mussolini)")
print("- Germany: 1933 (Hitler)")
print("- Spain: 1939 (Franco)")
print("- Multiple others in Eastern/Central Europe")
