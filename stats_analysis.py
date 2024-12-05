import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
import matplotlib.pyplot as plt

data = pd.read_csv("processed_ms_data.csv")

# 1. Analyzing walking speed
# multiple regression model with education and age
data['education_level'] = data['education_level'].astype('category')
model = smf.ols("walking_speed ~ education_level + age", data= data).fit()
print("\nMultiple Regression: Walking Speed\n")
print(model.summary())

# mixed-effects model to account for repeated measures
mixed_model = smf.mixedlm("walking_speed ~ education_level + age", data, groups = data['patient_id'])
mixed_model_fit = mixed_model.fit()
print("\nMixed-Effects Model: Walking Speed\n")
print(mixed_model_fit.summary())

# correlation of age and walking speed
corr, p_value = stats.pearsonr(data['age'], data['walking_speed'])
print(f"\nCorrelation Between Age and Walking Speed\nCorrelation: {corr:.3f}, p-value: {p_value:.3f}")

# 2. analyze costs
# Summary statistics for visit_cost by insurance_type
summary_stats = data.groupby('insurance_type')['visit_cost'].describe()
print(f"\nSummary statistics: Visit Costs by Insurance Type\n", summary_stats)

# ANOVA analysis for insurance type effect
anova_results = stats.f_oneway(
    data.loc[data['insurance_type'] == 'Basic', 'visit_cost'],
    data.loc[data['insurance_type'] == 'Premium', 'visit_cost'],
    data.loc[data['insurance_type'] == 'Platinum', 'visit_cost']
)
print(f"\nANOVA: Costs by Insurance Type\nF-statistic: {anova_results.statistic:.3f}, p-value: {anova_results.pvalue:.3f}")

# boxplot: visit cost by insurance type
plt.figure()
data.boxplot(column='visit_cost', by='insurance_type')
plt.title('Visit Costs by Insurance Type')
plt.ylabel('Cost of Visit')
plt.xlabel('Insurance Type')
plt.savefig('boxplot_question3.png')
# plt.show()

# 3. Advanced analysis
# Education-Age interaction on walking speed
print("\nInteraction Effect: Education * Age on Walking Speed\n")
interaction_model = smf.ols("walking_speed ~ education_level * age", data=data).fit()
print(interaction_model.summary())


# controlling for potential confounders - commented out to avoid long output
# print("\nControlled Model: Walking Speed")
# controlled_model = smf.ols("walking_speed ~ education_level * age + insurance_type + visit_date", data=data).fit()
# print(controlled_model.summary())