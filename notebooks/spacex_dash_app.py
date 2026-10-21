import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("../data/dataset_spacex.csv")

app = Dash(__name__)
app.title = "SpaceX Falcon 9 — Landing Prediction Dashboard"

app.layout = html.Div([
    html.H1("SpaceX Falcon 9 First-Stage Landing Dashboard"),
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": "All sites", "value": "ALL"}] +
                [{"label": s, "value": s} for s in sorted(df["LaunchSite"].unique())],
        value="ALL", clearable=False,
    ),
    dcc.Graph(id="success-pie"),
    html.P("Payload range (kg):"),
    dcc.RangeSlider(id="payload-slider",
                    min=int(df["PayloadMass"].min()), max=int(df["PayloadMass"].max()),
                    step=500, value=[int(df["PayloadMass"].min()),
                                     int(df["PayloadMass"].max())]),
    dcc.Graph(id="success-scatter"),
])

@app.callback(Output("success-pie", "figure"), Input("site-dropdown", "value"))
def update_pie(site):
    d = df if site == "ALL" else df[df["LaunchSite"] == site]
    if site == "ALL":
        g = d[d["Class"] == 1].groupby("LaunchSite").size().reset_index(name="n")
        return px.pie(g, values="n", names="LaunchSite",
                      title="Successful landings by site")
    g = d.groupby("Class").size().reset_index(name="n")
    return px.pie(g, values="n", names="Class",
                  title=f"Landing outcome — {site} (1=landed, 0=lost)")

@app.callback(Output("success-scatter", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def update_scatter(site, prange):
    d = df[(df["PayloadMass"] >= prange[0]) & (df["PayloadMass"] <= prange[1])]
    if site != "ALL":
        d = d[d["LaunchSite"] == site]
    return px.scatter(d, x="PayloadMass", y="Class", color="BoosterVersion",
                      hover_data=["LaunchSite", "Orbit"],
                      title="Payload vs. landing success")

if __name__ == "__main__":
    app.run_server(debug=False)
