import pandas as pd
import json

# Compile data on the three key ingredients:
# 1. Status Threat
# 2. Cultural Backlash (demographic change)
# 3. Institutional Trust

print("=== INGREDIENT 1: STATUS THREAT / NATIONAL PRIDE ===\n")

# United States National Pride Data (Gallup)
us_national_pride = {
    'year': [2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2024, 2025],
    'extremely_proud_pct': [55, 70, 65, 60, 57, 57, 57, 54, 47, 45, 39, 39, 38, 38],
    'very_proud_pct': [32, 22, 25, 27, 28, 29, 29, 29, 30, 28, 26, 22, 20, 20],
    'country': ['USA'] * 14
}

df_us_pride = pd.DataFrame(us_national_pride)
df_us_pride['total_proud_pct'] = df_us_pride['extremely_proud_pct'] + df_us_pride['very_proud_pct']

print("US National Pride (Gallup):")
print(df_us_pride[['year', 'extremely_proud_pct', 'total_proud_pct']].to_string(index=False))
print(f"\nChange 2001-2025:")
print(f"  'Extremely proud': {us_national_pride['extremely_proud_pct'][0]}% → {us_national_pride['extremely_proud_pct'][-1]}% ({us_national_pride['extremely_proud_pct'][-1] - us_national_pride['extremely_proud_pct'][0]:+d}pp)")
print(f"  Total proud: {df_us_pride['total_proud_pct'].iloc[0]:.0f}% → {df_us_pride['total_proud_pct'].iloc[-1]:.0f}% ({df_us_pride['total_proud_pct'].iloc[-1] - df_us_pride['total_proud_pct'].iloc[0]:+.0f}pp)")

print("\n=== INGREDIENT 2: CULTURAL BACKLASH / DEMOGRAPHIC CHANGE ===\n")

# Foreign-born population percentages
demographic_change = {
    'United States': {
        'years': [2000, 2010, 2020],
        'foreign_born_pct': [11.1, 12.9, 13.9],
        'note': 'Nearly 14 million immigrants entered 2000-2010'
    },
    'Greece': {
        'years': [2000, 2010, 2015, 2020],
        'foreign_born_pct': [7.0, 11.0, 10.0, 12.6],  # Estimates based on sources
        'note': 'Crisis reversed trend temporarily 2010-2015'
    },
    'Hungary': {
        'years': [2000, 2010, 2020],
        'foreign_born_pct': [2.9, 4.3, 5.8],
        'note': 'Much lower than W. Europe but rapid increase'
    },
    'Germany': {
        'years': [2000, 2010, 2020],
        'foreign_born_pct': [12.5, 13.0, 15.7],
        'note': '2015 refugee crisis major inflection point'
    }
}

print("Foreign-Born Population as % of Total Population:\n")
for country, data in demographic_change.items():
    print(f"{country}:")
    df_demo = pd.DataFrame({'year': data['years'], 'foreign_born_pct': data['foreign_born_pct']})
    print(df_demo.to_string(index=False))
    change = data['foreign_born_pct'][-1] - data['foreign_born_pct'][0]
    pct_increase = (change / data['foreign_born_pct'][0]) * 100
    print(f"  Change: {data['foreign_born_pct'][0]:.1f}% → {data['foreign_born_pct'][-1]:.1f}% (+{change:.1f}pp, +{pct_increase:.0f}% relative increase)")
    print(f"  Note: {data['note']}\n")

print("=== INGREDIENT 3: INSTITUTIONAL TRUST ===\n")

# Trust in Government (Pew Research - US)
us_trust_govt = {
    'year': [2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024],
    'trust_govt_pct': [44, 40, 47, 30, 24, 22, 19, 19, 20, 17, 20, 20, 23],
    'country': ['USA'] * 13
}

df_us_trust = pd.DataFrame(us_trust_govt)
print("US Trust in Government (Pew - trust 'always/most of the time'):")
print(df_us_trust[['year', 'trust_govt_pct']].to_string(index=False))
print(f"\nChange 2000-2024: {us_trust_govt['trust_govt_pct'][0]}% → {us_trust_govt['trust_govt_pct'][-1]}% ({us_trust_govt['trust_govt_pct'][-1] - us_trust_govt['trust_govt_pct'][0]:+d}pp)")

# European trust in political parties (ESS data approximations)
print("\n\nTrust in Political Parties - Difference from Mainstream Voters:\n")
print("(European Social Survey data - populist voters vs mainstream voters)")
print("\nRight Populist voters:")
print("  Trust in national parliament: -25 to -35 percentage points lower")
print("  Trust in political parties: -30 to -40 percentage points lower")
print("\nLeft Populist voters:")
print("  Trust in national parliament: -25 to -30 percentage points lower")
print("  Trust in political parties: -25 to -35 percentage points lower")

print("\n\nKey Finding:")
print("  People extremely distrustful of politicians are 14pp more likely")
print("  to support far-right populist parties vs those who trust politicians")

# Compile correlation data
print("\n=== CORRELATION WITH POPULIST VOTING ===\n")

correlation_summary = {
    'ingredient': [
        'Economic Crisis (unemployment)',
        'Status Threat (national pride decline)',
        'Cultural Backlash (rapid demographic change)',
        'Institutional Trust (distrust of parties)'
    ],
    'effect_size': [
        '~33% of populist surge explained',
        'Stronger predictor than economics (2016 US)',
        'Anxiety amplifies economic discontent',
        '+14pp far-right vote for extremely distrustful'
    ],
    'key_metric': [
        '1pp unemployment → 1pp populist vote',
        '2016: status threat > financial wellbeing',
        'EU: Immigration = 80% of pop. growth 2000-18',
        '-25 to -40pp trust gap for populist voters'
    ]
}

df_corr = pd.DataFrame(correlation_summary)
print(df_corr.to_string(index=False))

# Save to JSON for visualization
output_data = {
    'us_national_pride': us_national_pride,
    'us_trust_government': us_trust_govt,
    'demographic_change': demographic_change,
    'correlation_summary': correlation_summary
}

with open('ingredients_data.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("\n\nData saved to ingredients_data.json")

# Additional context
print("\n=== KEY INSIGHTS ===\n")
print("1. STATUS THREAT:")
print("   - US 'extremely proud' fell from 55% (2001) to 38% (2025) = -17pp")
print("   - Research shows perceived status loss predicts populist voting")
print("   - National humiliation narratives (Versailles, troika) create receptivity\n")

print("2. CULTURAL BACKLASH:")
print("   - US foreign-born: 11.1% → 13.9% (2000-2020) = +25% increase")
print("   - Greece: 7% → 12.6% during same period = +80% increase")
print("   - Europe: Immigration = 80% of population growth (2000-2018)")
print("   - Rapid change creates anxiety, especially when combined with economic stress\n")

print("3. INSTITUTIONAL TRUST:")
print("   - US trust in govt: 44% → 23% (2000-2024) = -21pp, fell below 25% since 2007")
print("   - Populist voters show -25 to -40pp lower trust in parliaments/parties")
print("   - Extremely distrustful voters 14pp more likely to support far-right")
print("   - Financial crises particularly damage institutional trust\n")

print("4. INTERACTION EFFECTS:")
print("   - All three ingredients AMPLIFY each other")
print("   - Economic crisis + status threat + demographic anxiety + trust collapse =")
print("     conditions for extremist surge")
print("   - Remove any ingredient and risk diminishes significantly")
print("   - Financial crises trigger ALL FOUR simultaneously (most dangerous)")
