import pandas as pd
import numpy as np
import random

# loading data and sorting by patient_id and visit_date
data = pd.read_csv("ms_data.csv")
data['visit_date'] = pd.to_datetime(data['visit_date'])
data.sort_values(by=['patient_id', 'visit_date'], inplace=True)

# load insurance types and assigning to pts
with open("insurance.lst", "r") as file:
    insurance_types = [line.strip() for line in file if line.strip()]

# mapping unique patient ids with random insurance type
unique_pt = data['patient_id'].unique()
insurance_mapping = {patient_id: np.random.choice(insurance_types) for patient_id in unique_pt}
data['insurance_type'] = data['patient_id'].map(insurance_mapping)

# visit cost based on insurance type
insurance_cost = {'Basic': 75, 'Premium': 100, 'Platinum': 150}
data['visit_cost'] = data['insurance_type'].map(insurance_cost) + np.random.normal(0, 10, size=len(data))

# calculating summary statistics
# mean walking speed by education level
mean_speed_educ = data.groupby('education_level')['walking_speed'].mean() 
print("\nMean walking speed by education level:\n", mean_speed_educ)

# mean costs by insurance type
mean_cost_ins = data.groupby('insurance_type')['visit_cost'].mean() 
print("\nMean costs by insurance type:\n", mean_cost_ins)

# Age effects on walking speed
age_bins = pd.cut(data['age'], bins=[0, 18, 35, 50, 65, 100], labels=['<18', '18-35', '36-50', '51-65', '>65'])
mean_speed_age = data.groupby(age_bins)['walking_speed'].mean()
age_effect = data[["age", "walking_speed"]].corr().iloc[0,1]
print("\nMean walking speed by age group:\n", mean_speed_age)
print("Correlation between walking speed and age:", age_effect)

# save analyzed data to new file
data.to_csv("processed_ms_data.csv", index=False)
