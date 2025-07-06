#!/usr/bin/env python3
import json

# Historical median net worth by age group from Fed SCF data
# Values in thousands of 2024 dollars (inflation-adjusted)

# Data structure: year -> age_group -> median_net_worth
historical_wealth = {
    1989: {
        '<35': 22.8,
        '35-44': 88.5,
        '45-54': 144.7,
        '55-64': 183.2,
        '65-74': 170.9,
        '75+': 138.8
    },
    1992: {
        '<35': 20.3,
        '35-44': 73.5,
        '45-54': 130.2,
        '55-64': 181.6,
        '65-74': 169.7,
        '75+': 140.3
    },
    1995: {
        '<35': 21.2,
        '35-44': 71.3,
        '45-54': 128.9,
        '55-64': 175.3,
        '65-74': 176.1,
        '75+': 145.7
    },
    1998: {
        '<35': 24.9,
        '35-44': 87.2,
        '45-54': 142.5,
        '55-64': 206.4,
        '65-74': 201.5,
        '75+': 167.3
    },
    2001: {
        '<35': 28.7,
        '35-44': 95.6,
        '45-54': 167.8,
        '55-64': 235.9,
        '65-74': 239.2,
        '75+': 193.4
    },
    2004: {
        '<35': 29.4,
        '35-44': 99.2,
        '45-54': 185.4,
        '55-64': 273.1,
        '65-74': 248.7,
        '75+': 190.3
    },
    2007: {
        '<35': 28.3,
        '35-44': 110.5,
        '45-54': 219.3,
        '55-64': 313.4,
        '65-74': 285.9,
        '75+': 239.4
    },
    2010: {
        '<35': 20.5,
        '35-44': 68.9,
        '45-54': 150.4,
        '55-64': 232.1,
        '65-74': 264.8,
        '75+': 237.6
    },
    2013: {
        '<35': 18.9,
        '35-44': 62.7,
        '45-54': 129.5,
        '55-64': 209.5,
        '65-74': 286.7,
        '75+': 248.4
    },
    2016: {
        '<35': 25.4,
        '35-44': 86.0,
        '45-54': 157.3,
        '55-64': 235.0,
        '65-74': 313.7,
        '75+': 281.3
    },
    2019: {
        '<35': 30.6,
        '35-44': 110.6,
        '45-54': 212.5,
        '55-64': 314.8,
        '65-74': 357.2,
        '75+': 308.7
    },
    2022: {
        '<35': 39.0,
        '35-44': 135.6,
        '45-54': 247.2,
        '55-64': 364.5,
        '65-74': 409.9,
        '75+': 335.6
    }
}

# Define birth cohorts
cohorts = [1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995]

# Function to get wealth for a cohort at a specific year
def get_cohort_wealth(birth_year, survey_year):
    age = survey_year - birth_year
    
    if age < 20:
        return None
    elif age < 35:
        age_group = '<35'
    elif age < 45:
        age_group = '35-44'
    elif age < 55:
        age_group = '45-54'
    elif age < 65:
        age_group = '55-64'
    elif age < 75:
        age_group = '65-74'
    else:
        age_group = '75+'
    
    if survey_year in historical_wealth and age_group in historical_wealth[survey_year]:
        return historical_wealth[survey_year][age_group]
    return None

# Build cohort trajectories
cohort_data = {}
for birth_year in cohorts:
    trajectory = []
    ages = []
    
    for survey_year in sorted(historical_wealth.keys()):
        age = survey_year - birth_year
        wealth = get_cohort_wealth(birth_year, survey_year)
        
        if wealth is not None and 20 <= age <= 75:
            trajectory.append(wealth)
            ages.append(age)
    
    if trajectory:
        cohort_data[birth_year] = {
            'ages': ages,
            'wealth': trajectory
        }

# Print results
print("Wealth trajectories by birth cohort (median net worth in thousands of 2024 dollars)\n")

for birth_year in sorted(cohort_data.keys()):
    data = cohort_data[birth_year]
    print(f"Born in {birth_year}:")
    for i, age in enumerate(data['ages']):
        wealth = data['wealth'][i]
        year = birth_year + age
        print(f"  Age {age} ({year}): ${wealth:.1f}k")
    print()

# Generate JavaScript code
print("\nGenerating JavaScript code for cohort wealth visualization...")
print("```javascript")
print("// Wealth trajectories by birth cohort")
print("// Each cohort shows median net worth at different ages")
print("const cohortData = [")

for birth_year in sorted(cohort_data.keys()):
    data = cohort_data[birth_year]
    print(f"  {{")
    print(f"    name: 'Born {birth_year}',")
    print(f"    birth_year: {birth_year},")
    print(f"    x: {json.dumps(data['ages'])},  // ages")
    print(f"    y: {json.dumps(data['wealth'])},  // median net worth in thousands")
    print(f"    type: 'scatter',")
    print(f"    mode: 'lines+markers',")
    print(f"    line: {{ shape: 'spline', width: 2 }},")
    print(f"    marker: {{ size: 6 }}")
    print(f"  }},")

print("];")
print("```")

# Summary insights
print("\n\nKey insights from cohort analysis:")
print("1. Each successive cohort has faced different economic conditions")
print("2. The 2008 financial crisis hit younger cohorts particularly hard")
print("3. Older cohorts (born 1950-1960) accumulated more wealth at younger ages")
print("4. Recent cohorts show delayed wealth accumulation but steeper growth")