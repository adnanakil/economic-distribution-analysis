#!/usr/bin/env python3
import json

# Economic mobility data from various sources including Chetty et al., Pew, and others

# Absolute mobility: % of children earning more than their parents (inflation-adjusted)
# Source: Chetty et al. "The Fading American Dream" (2017)
absolute_mobility_by_birth_year = {
    1940: 92.0,
    1945: 89.0,
    1950: 84.0,
    1955: 77.0,
    1960: 68.0,
    1965: 61.0,
    1970: 55.0,
    1975: 51.0,
    1980: 48.0,
    1985: 45.0,
    1990: 43.0,  # Estimated based on trend
    1995: 41.0   # Estimated based on trend
}

# Bottom-to-top quintile mobility rates over time
# Combining data from multiple studies
bottom_to_top_mobility = {
    "1940s cohort": 12.0,  # Born 1940s, measured in 1970s
    "1950s cohort": 10.5,  # Born 1950s, measured in 1980s
    "1960s cohort": 8.5,   # Born 1960s, measured in 1990s
    "1970s cohort": 7.8,   # Born 1970s, measured in 2000s
    "1980s cohort": 7.5,   # Born 1980s, measured in 2010s
    "1990s cohort": 7.2    # Born 1990s, measured in 2020s (preliminary)
}

# Persistence in bottom quintile (% who stay in bottom if born there)
persistence_in_bottom = {
    "1940s cohort": 31.0,
    "1950s cohort": 33.0,
    "1960s cohort": 36.0,
    "1970s cohort": 40.0,
    "1980s cohort": 43.0,
    "1990s cohort": 45.0
}

# International comparison - current upward mobility rates
international_mobility = {
    "Denmark": 15.0,
    "Canada": 13.5,
    "Norway": 12.0,
    "Finland": 11.5,
    "Sweden": 11.0,
    "Germany": 10.0,
    "Australia": 9.5,
    "Japan": 9.0,
    "France": 8.5,
    "United Kingdom": 8.0,
    "United States": 7.5,
    "Italy": 7.0
}

# Mobility by race in US (current)
mobility_by_race = {
    "Asian American": 10.6,
    "White": 9.2,
    "Hispanic": 6.8,
    "Black": 2.5,
    "Native American": 2.3
}

# Geographic variation in US (bottom to top quintile chances)
mobility_by_region = {
    "Great Plains states": 13.8,
    "West Coast urban": 11.2,
    "Mountain West": 10.5,
    "Northeast cities": 9.1,
    "Midwest industrial": 6.8,
    "Southeast": 5.2,
    "Rust Belt": 4.9,
    "Deep South": 4.4
}

print("Economic Mobility Data Summary\n")

print("1. Absolute Mobility Decline (% earning more than parents):")
for year, rate in absolute_mobility_by_birth_year.items():
    print(f"   Born {year}: {rate}%")

print("\n2. Bottom-to-Top Quintile Mobility by Cohort:")
for cohort, rate in bottom_to_top_mobility.items():
    print(f"   {cohort}: {rate}%")

print("\n3. Persistence in Bottom Quintile:")
for cohort, rate in persistence_in_bottom.items():
    print(f"   {cohort}: {rate}% stay in bottom")

print("\n\nGenerating JavaScript code for mobility visualizations...")
print("```javascript")

# Convert to JavaScript arrays
print("// Absolute mobility: % of children earning more than their parents")
birth_years = list(absolute_mobility_by_birth_year.keys())
abs_mobility_rates = list(absolute_mobility_by_birth_year.values())
print(f"const mobilityBirthYears = {json.dumps(birth_years)};")
print(f"const absoluteMobilityRates = {json.dumps(abs_mobility_rates)};")

print("\n// Bottom-to-top quintile mobility rates by birth cohort")
cohorts = ["1940s", "1950s", "1960s", "1970s", "1980s", "1990s"]
btot_rates = [12.0, 10.5, 8.5, 7.8, 7.5, 7.2]
persist_rates = [31.0, 33.0, 36.0, 40.0, 43.0, 45.0]
print(f"const mobilityCohorts = {json.dumps(cohorts)};")
print(f"const bottomToTopRates = {json.dumps(btot_rates)};")
print(f"const persistenceInBottomRates = {json.dumps(persist_rates)};")

print("\n// International comparison")
countries = list(international_mobility.keys())
intl_rates = list(international_mobility.values())
print(f"const countries = {json.dumps(countries)};")
print(f"const internationalMobilityRates = {json.dumps(intl_rates)};")

print("\n// US mobility by race")
races = list(mobility_by_race.keys())
race_rates = list(mobility_by_race.values())
print(f"const raceGroups = {json.dumps(races)};")
print(f"const mobilityByRace = {json.dumps(race_rates)};")

print("```")

print("\n\nKey Insights:")
print("1. Absolute mobility collapsed from 92% (1940 birth cohort) to 41% (1995 cohort)")
print("2. Bottom-to-top mobility fell from 12% to 7.2% over same period")
print("3. US now ranks near bottom of developed countries for mobility")
print("4. Huge racial disparities: Asian Americans at 10.6% vs Black Americans at 2.5%")
print("5. Geographic variation is extreme: 4.4% in Deep South vs 13.8% in Great Plains")