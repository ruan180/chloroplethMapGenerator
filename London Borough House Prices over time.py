import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Import data in local user folder
house_price_data = pd.read_csv('House_price.csv')
london_borough = gpd.read_file('London_Borough_Excluding_MHW.shp')
# Transform and merge data
house_data = house_price_data.rename(columns={'ONS_Code': 'GSS_CODE'})
london_prices_over_time_temp = pd.read_csv('land-registry-house-prices-borough.csv')
q = london_prices_over_time_temp.rename(columns={'Code': 'GSS_CODE'})
london_prices_over_time = london_borough.merge(q, on= 'GSS_CODE', how='left')
refined_price_ot = london_prices_over_time.loc[london_prices_over_time['Measure'] == 'Mean']
london_data_ot = refined_price_ot.rename(columns={'Name': 'Area', 'Value':'Price', 'Year': 'Survey Date', 'Code': 'GSS_CODE'})
london_data_ot[['x', 'y', 'z', 'Year']] = london_data_ot['Survey Date'].str.split(' ', 3, expand=True)
# i = london_ot_mean_price['Year'].str.split().str[3]
loop_data = london_data_ot[['GSS_CODE', 'Year']]
london_data_ot_final = london_data_ot[['GSS_CODE', 'Price', 'Year']]

# List of years that correlate to data supplied, these years will be plotted on one map each
list_of_years = ['1996', '1997']

a = london_data_ot_final.loc[loop_data['Year'] == '1996']
b = a.rename(columns={'Price': '1996'})
c = london_data_ot_final.loc[loop_data['Year'] == '1997']
d = c.rename(columns={'Price': '1997'})
merged = b.merge(d, on='GSS_CODE', how='left')
final = merged.drop(columns=['Year_x', 'Year_y'])
# Slight error in order of defined variables in for loop to be resolved.
for i in list_of_years:
    a = london_data_ot_final.loc[loop_data['Year'] == i]
    b = a.rename(columns={'Price': i})
    merged = merge_temp.merge(b, on='GSS_CODE', how='left')
    merge_temp = merged.drop(columns=['Year'])
    final = merge_temp.drop_duplicates(subset=['GSS_CODE'])

london_prices_df = london_borough.merge(house_data, on='GSS_CODE', how='left')
london_prices_df_95 = london_prices_df.merge(final, on= 'GSS_CODE', how='left')
london_prices_df_95 = london_prices_df_95.replace(',','', regex=True)
for i in list_of_years:
    london_prices_df_95[i] = london_prices_df_95[i].apply(pd.to_numeric,errors='coerce')

# save all the maps in the charts folder
output_path = 'charts/maps'
# counter for the for loop
i = 0
vmin, vmax = 50000, 1500000
# start the for loop to create one map per year
for year in list_of_years:
    # create map, UDPATE: added plt.Normalize to keep the legend range the same for all maps
    fig = london_prices_df_95.plot(column=year, cmap='gnuplot_r', figsize=(10, 10), linewidth=0.8, edgecolor='0.8',
                                   vmin=vmin, vmax=vmax,
                                   legend=True, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # remove axis of chart
    fig.axis('off')
    # add a title
    fig.set_title('Avg. London House Price (£)', fontdict={'fontsize': '25',
                            'fontweight': '3'})
    # create an annotation for the year by grabbing the first 4 digits
    only_year = year[:4]
    # position the annotation to the bottom left
    fig.annotate(only_year,
                 xy=(0.1, .225), xycoords='figure fraction',
                 horizontalalignment='left', verticalalignment='top',
                 fontsize=35)
    # this will save the figure as a high-res png in the output path. you can also save as svg if you prefer.
    filepath = os.path.join(output_path, year + '_avg_house_price_chloropleth.jpg')
    chart = fig.get_figure()
    chart.savefig(filepath, dpi=300)