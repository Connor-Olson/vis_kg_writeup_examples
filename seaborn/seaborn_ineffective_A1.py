# A less effective visualization in Seaborn (Figure 2, relative to Figure 1, `seaborn_effective_A/py`), which
# groups subplots by location instead of date, leading to lower data density (~4000 encoded numbers)

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
# 4. Replace precipitation values with a value of 0.0 with 0.01 to
#    prepare for using a logarithmic scale on the precipitation
# 5. Collect a subset of 20 locations from the set
df['Date.Full'] = df['Date.Full'].astype(str).str.strip()
df = df.dropna(subset=['Date.Full', 'Data.Temperature.Max Temp', 'Data.Temperature.Min Temp', 'Data.Precipitation'])
df['Data.Temperature.Max Temp'] = pd.to_numeric(df['Data.Temperature.Max Temp'], errors='coerce')
df['Data.Temperature.Min Temp'] = pd.to_numeric(df['Data.Temperature.Min Temp'], errors='coerce')
df['Data.Precipitation'] = pd.to_numeric(df['Data.Precipitation'], errors='coerce')
df = df.dropna(subset=['Data.Temperature.Max Temp', 'Data.Temperature.Min Temp', 'Data.Precipitation'])
df['precip_for_color'] = df['Data.Precipitation'].replace(0, 0.01)
unique_stations = df['Station.Code'].unique()
selected_stations = unique_stations[:20]
df_subset = df[df['Station.Code'].isin(selected_stations)]

# Seaborn does not directly support logarithmic color scaling in its 
# figure level API, so we need to do it ourselves using matplotlib. 
# This option is actually pointed out as an aside in the documentation: 
# https://seaborn.pydata.org/generated/seaborn.scatterplot.html  
cmap = mcolors.LinearSegmentedColormap.from_list("log_precip_cmap", ["black", "blue"])
norm = LogNorm(vmin=0.01, vmax=4.0)

# Create the grid for the small multiples plot and fill each subplot with a scatterplot.
# https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
# https://seaborn.pydata.org/generated/seaborn.scatterplot.html
g = sns.FacetGrid(df_subset, col="Station.Code", col_wrap=5, height=3.5, aspect=1, sharex=True, sharey=True)
g.map_dataframe(sns.scatterplot,
  x='Data.Temperature.Min Temp',
  y='Data.Temperature.Max Temp',
  hue='precip_for_color',
  palette=cmap,
  hue_norm=norm,
  legend=False,
  s=8,
  edgecolor='k',
  linewidth=0.3,
  ax=plt.gca()
)

plt.show()
