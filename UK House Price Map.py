# Import relevant packages
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import json

# Read in shp and data files (need absolute paths)
map_df = gpd.read_file('House_price.shp')
house_price_data = pd.read_csv('House_price.csv')

refined_data = map_df[['Name', 'AvgPrice','SHAPE_Leng','SHAPE_Area','geometry', 'ONS_Code']]

# Plot Data on Chloropleth Map
# set a variable that will call whatever column we want to visualise on the map
c_scheme = 'RdYlGn_r'
variable = 'AvgPrice'
# set the range for the choropleth
vmin, vmax = 105000, 1600000
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(15,12))
refined_data.plot(column=variable, cmap=c_scheme, linewidth=0.8, ax=ax, edgecolor='0.6')
ax.axis('off')
ax.set_title('Avg. House Price in the UK', fontdict={'fontsize': '25', 'fontweight' : '3'})
# create an annotation for the data source
ax.annotate('Source: Ministry of Housing, 2018',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
sm = plt.cm.ScalarMappable(cmap=c_scheme, norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)

# Save graphic if needed
fig.savefig("map_export.png", dpi=300)