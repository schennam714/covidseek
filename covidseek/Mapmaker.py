import gmaps
import pandas as pd 
from ipywidgets.embed import embed_minimal_html

f = open("apikey.txt", "r")
key = f.readline()

gmaps.configure(api_key=key)
corona_df = pd.read_csv("/Users/shreyas/Desktop/Web Dev/COVIDTrack/final_data.csv")
coords = (38.9085, -77.2405)
fig = gmaps.figure(center=coords, zoom_level=12)
heatmap_layer = gmaps.heatmap_layer(corona_df[['Lat', 'Long']], weights=corona_df['cases'], max_intensity=30, point_radius=3.0)

figure_layout = {
    'width': '100%',
    'height': '100%',
    'border': '1px solid black',
    'padding': '2px'
}
fig.add_layer(heatmap_layer)