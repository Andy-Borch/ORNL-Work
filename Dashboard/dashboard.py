import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc

#TODO: make an html version of each plot
    # create drop down menus to select the types of plots
    # make it look good

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Embedded HTML Plots"),

    html.Iframe(src="/assets/Node_vs_Diffsec_2021.html", style={"width": "100%", "height": "600px"}),
])













if __name__ =='__main__':
    app.run(debug=True, port=8051)