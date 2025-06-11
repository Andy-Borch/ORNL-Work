# #TODO:
#     # for the log plots, add a toggle to go between linear and logarithmic
#     # make it look good
#     # might be able to deploy it via github pages


import dash
from dash import html, dcc, Input, Output
from dash.dependencies import Input, Output, State

# Define which HTML files to show in each tab
GENERAL_PLOTS = [
    {"title": "Wait Time per Job ID", "file": "WaitTimevsJobID.html"},
    {"title": "Number of Jobs per Year", "file": "Num_Jobs_Over_Time.html"},
    {"title": "Jobs per user", "file": "Jobs_Submitted_per_User.html"},
    {"title": "Node Count by Year", "file": "Node_Count_by_Year.html"},
]

CLEANED_SCATTER_PLOTS = [
    {"title": "Cleaned Elapsed vs Node (2021)", "file": "Cleaned_ElapsedvsNode_2021.html"},
    {"title": "Cleaned Elapsed vs Node (2022)", "file": "Cleaned_ElapsedvsNode_2022.html"},
    {"title": "Cleaned Elapsed vs Node (2023)", "file": "Cleaned_ElapsedvsNode_2023.html"},
    {"title": "Cleaned Elapsed vs Node (2024)", "file": "Cleaned_ElapsedvsNode_2024.html"},
    {"title": "Combined Elapsed vs Node", "file": "Cleaned_ElapsedvsNode_AllYears.html"},
]

CLEANED_HEATMAP_PLOTS = [
    {"title": "Cleaned Elapsed vs Node Heatmap (2021)", "file": "Cleaned_ElapsedvsNode_Heatmap_2021.html"},
    {"title": "Cleaned Elapsed vs Node Heatmap (2022)", "file": "Cleaned_ElapsedvsNode_Heatmap_2022.html"},
    {"title": "Cleaned Elapsed vs Node Heatmap (2023)", "file": "Cleaned_ElapsedvsNode_Heatmap_2023.html"},
    {"title": "Cleaned Elapsed vs Node Heatmap (2024)", "file": "Cleaned_ElapsedvsNode_Heatmap_2024.html"},
]

TIMING_PLOTS = [
    {"title": "Node vs Diffsec (2021)", "file": "Node_vs_Diffsec_2021.html"},
    {"title": "Node vs Diffsec (2022)", "file": "Node_vs_Diffsec_2022.html"},
    {"title": "Node vs Diffsec (2023)", "file": "Node_vs_Diffsec_2023.html"},
    {"title": "Node vs Diffsec (2024)", "file": "Node_vs_Diffsec_2024.html"},
]

app = dash.Dash(__name__)
app.title = "ORNL Dashboard"

app.layout = html.Div([
    html.H1("ORNL Data Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),
    dcc.Tabs(id="tabs", value="general", children=[
        dcc.Tab(label="General", value="general"),
        dcc.Tab(label="Backfilled Job Data", value="cleaned"),
        dcc.Tab(label="Timing Data", value="timing"),
    ], style={"fontWeight": "bold"}),
    html.Div(id="cleaned-dropdown-container"),
    html.Div(id="plots-container", style={"background": "#fff", "padding": "20px", "borderRadius": "8px", "boxShadow": "0 2px 8px #ccc"}),
], style={"maxWidth": "900px", "margin": "auto", "fontFamily": "Segoe UI, Arial, sans-serif", "background": "#f7f7f7", "padding": "30px"})


@app.callback(
    Output("cleaned-dropdown-container", "children"),
    Input("tabs", "value"),
)
def show_cleaned_dropdown(tab):
    if tab == "cleaned":
        return html.Div([
            html.Label("Plot Type:", style={"marginRight": "10px"}),
            dcc.Dropdown(
                id="cleaned-plot-type",
                options=[
                    {"label": "Scatter", "value": "scatter"},
                    {"label": "Heatmap", "value": "heatmap"},
                ],
                value="scatter",
                clearable=False,
                style={"width": "200px", "display": "inline-block"}
            )
        ], style={"marginBottom": "20px"})
    return None

@app.callback(
    Output("plots-container", "children"),
    Input("tabs", "value"),
    State("cleaned-plot-type", "value"),
)
def update_plots(tab, cleaned_plot_type):
    if tab == "general":
        plots = GENERAL_PLOTS
    elif tab == "cleaned":
        # Default to scatter if dropdown not rendered yet
        if cleaned_plot_type == "heatmap":
            plots = CLEANED_HEATMAP_PLOTS
        else:
            plots = CLEANED_SCATTER_PLOTS
    elif tab == "timing":
        plots = TIMING_PLOTS
    else:
        plots = []
    children = []
    for plot in plots:
        children.append(
            html.Div([
                html.H3(plot["title"], style={"marginTop": "30px"}),
                html.Iframe(
                    src=f"/assets/{plot['file']}",
                    style={"width": "100%", "height": "600px", "border": "1px solid #ccc", "borderRadius": "6px"}
                )
            ])
        )
    return children

if __name__ == '__main__':
    app.run(debug=True, port=8051)