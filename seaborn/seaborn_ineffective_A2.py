# A less effective visualization in Seaborn (Figure 3, as compared to Figure 1 `seaborn_effective_A.py`), which
# does not encode precipitation, leading to a 33% reduction in data density.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm

# Load the weather data set
df = pd.read_csv("weather.csv")

# Prepare data:
# 1. Clean fields that might have stray spaces
# 2. Remove rows with missing data
# 3. Convert string data to numeric data where necessary
# 4. Collect a subset of 20 dates from the set
df['Date.Full'] = df['Date.Full'].astype(str).str.strip()
df = df.dropna(subset=['Date.Full', 'Data.Temperature.Max Temp', 'Data.Temperature.Min Temp'])
df['Data.Temperature.Max Temp'] = pd.to_numeric(df['Data.Temperature.Max Temp'], errors='coerce')
df['Data.Temperature.Min Temp'] = pd.to_numeric(df['Data.Temperature.Min Temp'], errors='coerce')
df = df.dropna(subset=['Data.Temperature.Max Temp', 'Data.Temperature.Min Temp'])
unique_dates = df['Date.Full'].unique()
selected_dates = unique_dates[:20]
df_subset = df[df['Date.Full'].isin(selected_dates)]

# Create the grid for the small multiples plot and fill each subplot with a scatterplot.
# https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
# https://seaborn.pydata.org/generated/seaborn.scatterplot.html
g = sns.FacetGrid(df_subset, col="Date.Full", col_wrap=5, height=3.5, aspect=1, sharex=True, sharey=True)
g.map_dataframe(sns.scatterplot,
  x='Data.Temperature.Min Temp',
  y='Data.Temperature.Max Temp',
  legend=False,
  s=8,
  edgecolor='k',
  linewidth=0.3,
  ax=plt.gca()
)

plt.show()
