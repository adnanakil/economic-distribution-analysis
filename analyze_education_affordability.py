import pandas as pd

# Read the education data
df = pd.read_csv('education_affordability_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Get data from 1993 (when education CPI starts) and 2024
data_1993 = df[df['date'].dt.year == 1993].mean()
data_2024 = df[df['date'].dt.year == 2024].mean()

print("=== EDUCATION AFFORDABILITY ANALYSIS ===\n")

# Education CPI vs Wages
if 'CUSR0000SAE1' in df.columns and 'AHETPI' in df.columns:
    edu_1993 = data_1993['CUSR0000SAE1']
    edu_2024 = data_2024['CUSR0000SAE1']
    wage_1993 = data_1993['AHETPI']
    wage_2024 = data_2024['AHETPI']

    edu_growth = ((edu_2024/edu_1993 - 1) * 100)
    wage_growth = ((wage_2024/wage_1993 - 1) * 100)

    print(f"Education CPI (1993-2024):")
    print(f"  1993: {edu_1993:.1f}")
    print(f"  2024: {edu_2024:.1f}")
    print(f"  Growth: {edu_growth:.1f}%\n")

    print(f"Average Hourly Wages (1993-2024):")
    print(f"  1993: ${wage_1993:.2f}")
    print(f"  2024: ${wage_2024:.2f}")
    print(f"  Growth: {wage_growth:.1f}%\n")

    print(f"Education has become {(edu_growth - wage_growth):.1f} percentage points")
    print(f"more expensive than wage growth would support.\n")

    # Burden index
    burden_1993 = edu_1993 / wage_1993
    burden_2024 = edu_2024 / wage_2024
    burden_increase = ((burden_2024/burden_1993 - 1) * 100)

    print(f"Education Burden Index (CPI/Wage):")
    print(f"  1993: {burden_1993:.2f}")
    print(f"  2024: {burden_2024:.2f}")
    print(f"  Increase: {burden_increase:.1f}%")
    print(f"  Interpretation: Education costs {burden_increase:.1f}% more of hourly wages in 2024 vs 1993")

# Education Services CPI
print("\n--- Education Services Specific ---")
if 'CPIEDUSL' in df.columns:
    edu_serv_1993 = data_1993['CPIEDUSL']
    edu_serv_2024 = data_2024['CPIEDUSL']

    edu_serv_growth = ((edu_serv_2024/edu_serv_1993 - 1) * 100)

    print(f"\nEducation Services CPI (1993-2024):")
    print(f"  1993: {edu_serv_1993:.1f}")
    print(f"  2024: {edu_serv_2024:.1f}")
    print(f"  Growth: {edu_serv_growth:.1f}%")
    print(f"  vs Wage growth: {(edu_serv_growth - wage_growth):.1f} pp gap")
