# Import necessary libraries
import psycopg # to connect to postgresql
import matplotlib.pyplot as plt
import plotly.express as px # to plot the map
import pandas as pd # to manipulate data
import geopandas

# get my postgresql credentials
credentials = pd.read_excel("~/my_credentials.xlsx")
crest_port = 5432
db_name = credentials.dbname[0]
host_name = credentials.host[0]
user_name = credentials.user_name[0]
user_password = credentials.user_password[0]
# connect to postgresql
connec = psycopg.connect(
    port=5432,
    host=host_name,
    dbname=db_name,
    user=user_name,
    password=user_password)
# Retrieve data tables
cursor = connec.cursor()
table1 = 'ctry_bins_maps'
schema1 = 'my_schema'
cursor.execute(f'SELECT * from {schema1}.{table1}')
# Fetch required data
biblio_data = cursor.fetchall()
# Closing the connection
connec.close()

# mutate data and add column names
biblio_data = pd.DataFrame(biblio_data)
biblio_data.columns = ["country","total_count","tw1", "tw2"]
# CHANGE COUNTRY NAMES TO MATCH GEOPANDA LIST
biblio_data['country'] = biblio_data['country'].replace(['USA', 'UK', 'Czech Republic'],
                                                    ['United States of America', 'United Kingdom', 'Czechia'])
print(biblio_data) # inspect the data

# plot an interactive map using plotly
biblio_map = px.choropleth(biblio_data,
                           locationmode = 'country names',
                           locations="country",
                           scope="world",
                           hover_name="country",
                           color="total_count",
                           color_continuous_scale="Viridis")
# save my interactive plot
biblio_map.write_html("~/choropleth_example_python.html")

# plot static maps
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world.columns=['pop_est', 'continent2', 'country', 'Country Code', 'gdp_md_est', 'geometry']

# Merge with our data
mapdata=pd.merge(world,biblio_data, how = "outer", on='country')
mapdata.to_excel("mapdata.xlsx")

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