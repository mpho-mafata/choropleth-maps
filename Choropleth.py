## set directory to the desired folder
import os
os.chdir("/Users/mphomafata/Documents/GitHub/choropleth-maps")

# Import necessary libraries
import psycopg # to connect to postgresql
import matplotlib.pyplot as plt
import plotly.express as px # to plot the map
import pandas as pd # to manipulate data
import geopandas
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes # for zoomed-in subplots
from mpl_toolkits.axes_grid1.inset_locator import mark_inset # for zoomed-in subplots

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
mapdata = pd.merge(world, biblio_data, how = "outer", left_on="SOVEREIGNT", right_on='region')

# Plot world map
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16,10))
ax.axis('off') # remove axis lines to have a  blank background
mapplot = mapdata.plot(column='total_count',
                       scheme='naturalbreaks',
                       k=10,
                       ax=ax,
                       legend=True,
                       edgecolor='black',
                       cmap="tab10", # tab10, tab20, Accent, Dark2, Paired, Pastel1, Set1, Set2
                       linewidth=0.5,
                       missing_kwds={"color": "lightgrey"},
                       legend_kwds={"title": 'Number of publications',
                                    'bbox_to_anchor':(0.22, 0.62),
                                    'title_fontsize':12,
                                    'fontsize':10}
                       )
# Add a EUROPE zoom plot
axins = zoomed_inset_axes(ax,
                          zoom=1.75, # size of the zoomed section
                          bbox_to_anchor=(860,285)
                          )
axins.set_xlim(-10,40)
axins.set_ylim(30,60)
plt.xticks(visible=False)
plt.yticks(visible=False)
mark_inset(ax, axins, loc1=2, loc2=1, fc="none", ec="0.5")

mapdata.plot(column='total_count',
             scheme='naturalbreaks',
             k=10,
             ax = axins,
             legend=False,
             edgecolor='black',
             cmap="tab10",
             linewidth=0.5,
             missing_kwds={"color": "lightgrey"}
             )

# save my map
plt.savefig(fname = 'choropleth_example_python.svg',dpi = 600,
            bbox_inches="tight", pad_inches=0.0,
            transparent=True, format = "svg")
plt.show()