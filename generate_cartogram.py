import pandas as pd
import geopandas as gpd
import plotly.express as px
import cartogram
import requests
from pathlib import Path

year = 2020
population_url = "https://datahub.io/core/population/_r/-/data/population.csv"
geo_url = (
    "https://raw.githubusercontent.com/nvkelso/"
    "natural-earth-vector/master/geojson/"
    "ne_110m_admin_0_countries.geojson")

population = pd.read_csv(population_url)
population = population[population["Year"] == year].copy()
population = population.rename(columns={"Country Code": "iso_a3", "Value": "population"})

response = requests.get(geo_url, timeout=30)
Path("countries.geojson").write_bytes(response.content)
world = gpd.read_file("countries.geojson")



europe = world[
    (world["CONTINENT"] == "Europe") &
    (world["ADM0_A3"] != "RUS")
].merge(
    population[["iso_a3", "population"]],
    left_on="ADM0_A3",
    right_on="iso_a3"
)

europe = europe[europe["population"] > 0].copy()
europe = europe.to_crs("EPSG:3035")


intensity = 0.65

area = europe.geometry.area
area_population = area / area.sum() * europe["population"].sum()

europe["cartogram_value"] = (
    intensity * europe["population"]
    + (1 - intensity) * area_population
)

print(f"Generant cartograma amb intensitat {intensity}...")
result = cartogram.Cartogram(
    europe, "cartogram_value", max_iterations=10
)


result = result.to_crs("EPSG:4326")
result = result.reset_index(drop=True)
result["id"] = result.index.astype(str)

geojson = result.__geo_interface__

fig = px.choropleth(
    result,
    geojson=result.__geo_interface__,
    locations="id",
    featureidkey="properties.id",
    color="population",
    hover_name="ADMIN",
    color_continuous_scale=[
        [0.0, "#dbeafe"],
        [0.25, "#93c5fd"],
        [0.5, "#3b82f6"],
        [0.75, "#1d4ed8"],
        [1.0, "#172554"]
    ],
    title=f"Cartograma de població europea ({year})"
)

fig.update_geos(fitbounds="locations",visible=False)
fig.update_layout(height=700, coloraxis_colorbar_title="Habitants")
fig.show()
fig.write_html("cartogram.html")