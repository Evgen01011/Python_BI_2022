import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import re
import seaborn as sns
from matplotlib.patches import ConnectionPatch
from matplotlib import patches

# Heatmap new_cases in different country per day
covid = pd.read_csv('owid-covid-data.csv')
covid["date"] = pd.to_datetime(covid["date"])    # obj to data

# Create new table
data  = pd.pivot_table(covid, values='new_cases', index=['date'],
                       columns=['location'], aggfunc=np.sum)
data = data[60:151]                              # app. first days
data_new = data[['Australia', 'Afghanistan', 'India', 'Indonesia', 'China', 'Japan','Iran', 'Thailand', 'Israel',
                 'Algeria', 'Angola', 'Ethiopia', 'Egypt', 'Kenya', 'South Africa', 'Zambia', 'Zimbabwe',
                 'Argentina', 'Brazil', 'Ecuador', 'Chile', 'Uruguay', 'Canada', 'United States', 'Mexico',
                 'United Kingdom',  'Austria', 'Belgium', 'Croatia', 'Denmark', 'France', 'Germany', 'Italy', 'Norway',
                 'Sweden', 'Russia', 'Spain']]
data_new = data_new.fillna(0)                   # not good but for graphs
data_new2 = data_new.T
# Correct label annotation
data_new2 = data_new2.rename(columns = lambda x: str(x))
data_new2.columns = data_new2.columns.str.replace(' 00:00:00', '')
# Create plot
plt.figure(figsize=(50, 30))
sns.heatmap(data_new2, cmap='coolwarm', robust=True,
            vmax=4500, fmt='.5g', linewidth=0.01, linecolor='lightgrey')
plt.xlabel('Date', fontsize=40)
plt.ylabel('Country', fontsize=40)
plt.title("New Covid Cases a Countries", fontsize=60)
plt.xticks(rotation = 45, fontsize=24)
plt.yticks(fontsize=24)
plt.savefig('Covid Heatmap.png')

# Violin plot for test distribution in Canada and USA
data  = covid.sort_values(by='date', axis=0)
covid_usa_can = data.query("location == 'United States' | location == 'Canada'")
# Select first stage of pandemic
covid_usa_can = covid_usa_can.query("date >= '2020-03-01' & date < '2020-06-01'")
# Plot
plt.figure(figsize=(8, 5), dpi=300)
sns.violinplot(data=covid_usa_can, x="location", y="new_tests",
               width=0.8, palette='husl', saturation=0.75, dodge=False)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Number of new test a day', fontsize=12)
plt.title("Distribution of New Test a Day in USA and Canada", fontsize=12)
plt.savefig('New_test_violinplot.png')


# Correlation
covid_usa = covid_usa_can.query("location == 'United States'")
covid_can = covid_usa_can.query("location == 'Canada'")
fig, axes = plt.subplots(ncols=2, figsize=(12, 5), dpi=300)
ax=axes[0]
sns.scatterplot(data=covid_usa, x='new_tests', y='new_cases', color='blue', ax=axes[0])
ax.set_xlabel('Number of new test a day', fontsize=12)
ax.set_ylabel('Number of new cases a day', fontsize=12)
ax.set_title("Dependance of New Test a Day and New Cases a Day in USA", fontsize=10)
ax=axes[1]
sns.scatterplot(data=covid_can, x='new_tests', y='new_cases', color='orange', ax=axes[1])
ax.set_xlabel('Number of new test a day', fontsize=12)
ax.set_ylabel('Number of new cases a day', fontsize=12)
ax.set_title("Dependance of New Test a Day and New Cases a Day in Canada", fontsize=10)
plt.savefig('Dependances.png')


