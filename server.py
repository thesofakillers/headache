"""Dash server index point"""
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


DAYLIO_PATH = os.getenv("DAYLIO_PATH")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

FIELDS = ["full_date", "Headache", "Exercise", "Ibuprofen", "Paracetamol", "Coffee"]
daylio_df = pd.read_csv(
    DAYLIO_PATH,
    usecols=FIELDS,
    index_col="full_date",
    parse_dates=True,
)
daylio_df = daylio_df.resample("1D").first()


TOTAL_FIELDS = len(FIELDS)

fig = make_subplots(
    rows=TOTAL_FIELDS - 1, cols=1, shared_xaxes=True, vertical_spacing=0.02
)

for i, field in enumerate(FIELDS[1:], 1):
    fig.add_trace(
        go.Scatter(x=daylio_df.index, y=daylio_df[field], line_shape="hv", name=field),
        row=i,
        col=1,
    )

app.layout = html.Div(
    children=[
        html.H1("Headache data visualization"),
        dcc.Graph(id="daylio", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
