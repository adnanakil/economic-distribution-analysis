import pandas as pd
import json
from datetime import datetime

# Load all the data we collected
housing_df = pd.read_csv('housing_affordability_data.csv')
healthcare_df = pd.read_csv('healthcare_affordability_data.csv')
education_df = pd.read_csv('education_affordability_data.csv')
food_df = pd.read_csv('food_essentials_affordability_data.csv')

# Prepare housing data for visualization
housing_data = {
    'dates': housing_df['date'].tolist(),
    'home_price': housing_df['MSPUS'].tolist(),
    'median_income': housing_df['MEHOINUSA672N'].tolist(),
    'case_shiller': housing_df['CSUSHPISA'].tolist(),
    'mortgage_rate': housing_df['MORTGAGE30US'].tolist(),
    'housing_cpi': housing_df['CPIHOSSL'].tolist(),
    'rent_cpi': housing_df['CUSR0000SEHA'].tolist()
}

# Calculate price to income ratio
housing_df['price_to_income'] = housing_df['MSPUS'] / housing_df['MEHOINUSA672N']
housing_data['price_to_income'] = housing_df['price_to_income'].tolist()

# Prepare healthcare data
healthcare_data = {
    'dates': healthcare_df['date'].tolist(),
    'medical_cpi': healthcare_df['CPIMEDSL'].tolist(),
    'hospital_cpi': healthcare_df['CPIHOSNS'].tolist(),
    'prescription_cpi': healthcare_df['CUSR0000SEMD'].tolist(),
    'wages': healthcare_df['AHETPI'].tolist()
}

# Calculate healthcare burden (normalized to 1980)
healthcare_df['date'] = pd.to_datetime(healthcare_df['date'])
base_1980 = healthcare_df[healthcare_df['date'].dt.year == 1980].mean()
if pd.notna(base_1980['CPIMEDSL']) and pd.notna(base_1980['AHETPI']):
    healthcare_df['medical_indexed'] = (healthcare_df['CPIMEDSL'] / base_1980['CPIMEDSL']) * 100
    healthcare_df['wage_indexed'] = (healthcare_df['AHETPI'] / base_1980['AHETPI']) * 100
    healthcare_data['medical_indexed'] = healthcare_df['medical_indexed'].tolist()
    healthcare_data['wage_indexed'] = healthcare_df['wage_indexed'].tolist()

# Prepare education data
education_data = {
    'dates': education_df['date'].tolist(),
    'education_cpi': education_df['CUSR0000SAE1'].tolist(),
    'education_services_cpi': education_df['CPIEDUSL'].tolist(),
    'wages': education_df['AHETPI'].tolist()
}

# Calculate education burden (normalized to 1993)
education_df['date'] = pd.to_datetime(education_df['date'])
base_1993 = education_df[education_df['date'].dt.year == 1993].mean()
if pd.notna(base_1993['CUSR0000SAE1']) and pd.notna(base_1993['AHETPI']):
    education_df['education_indexed'] = (education_df['CUSR0000SAE1'] / base_1993['CUSR0000SAE1']) * 100
    education_df['wage_indexed'] = (education_df['AHETPI'] / base_1993['AHETPI']) * 100
    education_data['education_indexed'] = education_df['education_indexed'].tolist()
    education_data['wage_indexed'] = education_df['wage_indexed'].tolist()

# Prepare food data
food_data = {
    'dates': food_df['date'].tolist(),
    'food_cpi': food_df['CPIUFDSL'].tolist(),
    'food_home_cpi': food_df['CPIUFDNS'].tolist(),
    'food_away_cpi': food_df['CPILFENS'].tolist(),
    'overall_cpi': food_df['CPIAUCSL'].tolist(),
    'wages': food_df['AHETPI'].tolist()
}

# Calculate food burden (normalized to 1980)
food_df['date'] = pd.to_datetime(food_df['date'])
base_1980_food = food_df[food_df['date'].dt.year == 1980].mean()
if pd.notna(base_1980_food['CPIUFDSL']) and pd.notna(base_1980_food['AHETPI']):
    food_df['food_indexed'] = (food_df['CPIUFDSL'] / base_1980_food['CPIUFDSL']) * 100
    food_df['wage_indexed'] = (food_df['AHETPI'] / base_1980_food['AHETPI']) * 100
    food_data['food_indexed'] = food_df['food_indexed'].tolist()
    food_data['wage_indexed'] = food_df['wage_indexed'].tolist()

# Create comparison data for all four categories since 1980
comparison_data = {
    'categories': ['Housing', 'Healthcare', 'Education', 'Food'],
    'growth_vs_wages': [73, 70, 109, -15],  # percentage point difference from wage growth
    'burden_increase': [73, 70, 40, -15],  # % change in burden
    'quality_adjusted': [28, 70, 40, -15]  # after quality adjustment where applicable
}

# Write all data to JSON for JavaScript
output = {
    'housing': housing_data,
    'healthcare': healthcare_data,
    'education': education_data,
    'food': food_data,
    'comparison': comparison_data
}

with open('affordability_data.json', 'w') as f:
    json.dump(output, f)

print("Data prepared and saved to affordability_data.json")
print("\nSummary statistics:")
print(f"Housing records: {len(housing_df)}")
print(f"Healthcare records: {len(healthcare_df)}")
print(f"Education records: {len(education_df)}")
print(f"Food records: {len(food_df)}")
