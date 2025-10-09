import pandas as pd
import json

# Load all the data
housing_df = pd.read_csv('housing_affordability_data.csv')
healthcare_df = pd.read_csv('healthcare_affordability_data.csv')
education_df = pd.read_csv('education_affordability_data.csv')
food_df = pd.read_csv('food_essentials_affordability_data.csv')

# Filter to reduce size - take every 12th month (annual data) starting from 1980
housing_df['date'] = pd.to_datetime(housing_df['date'])
housing_df['year'] = housing_df['date'].dt.year
housing_annual = housing_df[housing_df['year'] >= 1980].groupby('year').first().reset_index()

healthcare_df['date'] = pd.to_datetime(healthcare_df['date'])
healthcare_df['year'] = healthcare_df['date'].dt.year
healthcare_annual = healthcare_df[healthcare_df['year'] >= 1980].groupby('year').first().reset_index()

education_df['date'] = pd.to_datetime(education_df['date'])
education_df['year'] = education_df['date'].dt.year
education_annual = education_df[education_df['year'] >= 1993].groupby('year').first().reset_index()

food_df['date'] = pd.to_datetime(food_df['date'])
food_df['year'] = food_df['date'].dt.year
food_annual = food_df[food_df['year'] >= 1980].groupby('year').first().reset_index()

# Calculate key metrics
housing_annual['price_to_income'] = housing_annual['MSPUS'] / housing_annual['MEHOINUSA672N']

# Healthcare indexed to 1980
base_1980_health = healthcare_annual[healthcare_annual['year'] == 1980].iloc[0]
healthcare_annual['medical_indexed'] = (healthcare_annual['CPIMEDSL'] / base_1980_health['CPIMEDSL']) * 100
healthcare_annual['wage_indexed'] = (healthcare_annual['AHETPI'] / base_1980_health['AHETPI']) * 100

# Education indexed to 1993
base_1993_edu = education_annual[education_annual['year'] == 1993].iloc[0]
education_annual['education_indexed'] = (education_annual['CUSR0000SAE1'] / base_1993_edu['CUSR0000SAE1']) * 100
education_annual['edu_wage_indexed'] = (education_annual['AHETPI'] / base_1993_edu['AHETPI']) * 100

# Food indexed to 1980
base_1980_food = food_annual[food_annual['year'] == 1980].iloc[0]
food_annual['food_indexed'] = (food_annual['CPIUFDSL'] / base_1980_food['CPIUFDSL']) * 100
food_annual['food_wage_indexed'] = (food_annual['AHETPI'] / base_1980_food['AHETPI']) * 100

# Create simple output
output = {
    'housing': {
        'years': housing_annual['year'].tolist(),
        'price_to_income': housing_annual['price_to_income'].where(pd.notna(housing_annual['price_to_income']), None).tolist()
    },
    'healthcare': {
        'years': healthcare_annual['year'].tolist(),
        'medical_indexed': healthcare_annual['medical_indexed'].where(pd.notna(healthcare_annual['medical_indexed']), None).tolist(),
        'wage_indexed': healthcare_annual['wage_indexed'].where(pd.notna(healthcare_annual['wage_indexed']), None).tolist()
    },
    'education': {
        'years': education_annual['year'].tolist(),
        'education_indexed': education_annual['education_indexed'].where(pd.notna(education_annual['education_indexed']), None).tolist(),
        'wage_indexed': education_annual['edu_wage_indexed'].where(pd.notna(education_annual['edu_wage_indexed']), None).tolist()
    },
    'food': {
        'years': food_annual['year'].tolist(),
        'food_indexed': food_annual['food_indexed'].where(pd.notna(food_annual['food_indexed']), None).tolist(),
        'wage_indexed': food_annual['food_wage_indexed'].where(pd.notna(food_annual['food_wage_indexed']), None).tolist()
    },
    'comparison': {
        'categories': ['Housing', 'Healthcare', 'Education', 'Food'],
        'growth_vs_wages': [73, 70, 109, -15]
    }
}

with open('affordability_data_simple.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Simple data file created")
print(f"Housing years: {len(output['housing']['years'])}")
print(f"Healthcare years: {len(output['healthcare']['years'])}")
print(f"Education years: {len(output['education']['years'])}")
print(f"Food years: {len(output['food']['years'])}")
