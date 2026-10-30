import pandas as pd
import plotly.express as px

url = ("https://datahub.io/core/co2-fossil-by-nation/"
    "_r/-/data/fossil-fuel-co2-emissions-by-nation.csv")

df = pd.read_csv(url)
df = df[df["Year"] == 2020].copy()
df = df.nlargest(10, "Total")
fuels = ["Solid Fuel", "Liquid Fuel", "Gas Fuel", "Cement", "Gas Flaring"]

data = df.melt(id_vars=["Country"],value_vars=fuels, var_name="Font", value_name="Emissions")
data["Emissions"] = pd.to_numeric(data["Emissions"], errors="coerce")
data = data.dropna(subset=["Emissions"])
data = data[data["Emissions"] > 0]

fig = px.sunburst(data, path=["Country", "Font"], values="Emissions",
    title="Emissions de carboni per país i font (2020)")

fig.update_layout(height=750)
fig.show()
fig.write_html("sunburst.html")
