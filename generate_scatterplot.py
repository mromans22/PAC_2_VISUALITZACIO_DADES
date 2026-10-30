import pandas as pd
import plotly.graph_objects as go

gdp_url = "https://datahub.io/core/gdp/_r/-/data/gdp.csv"
inflation_url = "https://datahub.io/core/inflation/_r/-/data/inflation-consumer.csv"

gdp = pd.read_csv(gdp_url)
inflation = pd.read_csv(inflation_url)

gdp = gdp[gdp["Country Code"] == "ESP"]
inflation = inflation[inflation["Country Code"] == "ESP"]

data = pd.merge(gdp[["Year", "Value"]], inflation[["Year", "Inflation"]], on="Year", how="inner")
data = data.rename(columns={"Value": "PIB"})

data = data[(data["Year"] >= 2000) & (data["Year"] <= 2024)].copy()
data = data.dropna().sort_values("Year")
data["PIB"] = data["PIB"] / 1e12

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data["PIB"],
    y=data["Inflation"],
    mode="lines+markers+text",
    text=data["Year"],
    textposition="top center",
    customdata=data[["Year"]],
    hovertemplate=(
        "Any: %{customdata[0]}<br>"
        "PIB: %{x:.2f} bilions USD<br>"
        "Inflació: %{y:.2f}%<extra></extra>"
    ),
    line=dict(width=2),
    marker=dict(size=9)
))

fig.update_layout(
    title="Evolució del PIB i la inflació a Espanya",
    xaxis_title="PIB (bilions USD corrents)",
    yaxis_title="Inflació anual (%)",
    height=650
)
fig.show()
fig.write_html("connected_scatterplot.html")
