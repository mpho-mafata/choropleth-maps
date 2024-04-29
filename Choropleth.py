## set directory to the desired folder
import os
os.chdir("/Users/mphomafata/Documents/GitHub/choropleth-maps")

# Import necessary libraries
import psycopg # to connect to postgresql
import matplotlib.pyplot as plt
import plotly.express as px # to plot the map
import pandas as pd # to manipulate data
import geopandas


# Fetch required data
biblio_data = pd.read_csv("/Users/mphomafata/Documents/GitHub/choropleth-maps/ctry_bins.csv", header=0)

# CHANGE COUNTRY NAMES IN OUR DATASET TO MATCH GEOPANDA LIST
biblio_data['region'] = biblio_data['region'].replace(['USA', 'U Arab Emirates', 'Czech Republic', 'England', 'Wales', 'Scotland', 'North Ireland', 'Peoples R China'], # our data's country names
                                                    ['United States of America', 'United Arab Emirates', 'Czechia', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'China']) # Geopanda country names

# Now there is inconsistency in the united kingdom data so let's fix that
biblio_data = biblio_data.groupby("region").aggregate(func="sum").reset_index()

biblio_data.to_excel("biblio.xlsx")
# plot an interactive map using plotly
biblio_map = px.choropleth(biblio_data,
                           locationmode = 'country names',
                           locations="region",
                           scope="world",
                           hover_name="region",
                           color="total_count",
                           color_continuous_scale="Viridis")
# save my interactive plot
biblio_map.write_html("/Users/mphomafata/Documents/GitHub/choropleth-maps/choropleth_example_python.html")

# plot static maps
# read the polygon countries data from the Geopandas reference data
world = geopandas.read_file("/Users/mphomafata/Documents/GitHub/choropleth-maps/geopanda reference data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.dbf")

# Merge with our data
mapdata=pd.merge(world, biblio_data, how = "outer", left_on="SOVEREIGNT", right_on='region')

# Plot world map
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16,10))
ax.axis('off') # remove axis lines to have a  blank background
mapplot = mapdata.plot(column='total_count',
                       scheme='naturalbreaks',
                       k=10,
                       ax=ax,
                       legend=True,
                       edgecolor='black',
                       linewidth=0.5,
                       missing_kwds={"color": "lightgrey"},
                       legend_kwds={"title": 'Number of publications',
                                    'bbox_to_anchor':(0.22, 0.62),
                                    'title_fontsize':12,
                                    'fontsize':10}
                       )
# save my map
plt.savefig(fname = 'choropleth_example_python.svg',dpi = 600,
            bbox_inches="tight", pad_inches=0.0,
            transparent=True, format = "svg")
plt.show()