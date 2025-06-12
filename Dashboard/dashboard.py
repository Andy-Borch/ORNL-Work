# #TODO:
#     # update all titles, axis titles, descriptions, and legends
#     # make it look good
#     # might be able to deploy it via github pages
#     # Fix plots not rendering until you click the tab
#     # Fix the error messages that don't do anything


import dash
from dash import html, dcc, Input, Output
from dash.dependencies import Input, Output, State

# Define which HTML files to show in each tab
GENERAL_PLOTS = [
    {"title": "Wait Time per Job ID", "file": "WaitTimevsJobID.html"},
    {"title": "Number of Jobs per Year", "file": "Num_Jobs_Over_Time.html"},
    {"title": "Jobs per user", "file": "Jobs_Submitted_per_User.html"},
    {"title": "Node Count by Year", "file": "Node_Count_by_Year.html"},
    {"title": "Elapsed Time Distribution by Year", "file": "Elapsed_Time_Distribution_by_Year.html"},
]

CLEANED_SCATTER_PLOTS = [
    {"title": "Combined Elapsed vs Node", "file": "Cleaned_ElapsedvsNode_AllYears.html"},
    {"title": "Cleaned Elapsed vs Node (2021)", "file": "Cleaned_ElapsedvsNode_2021.html"},
    {"title": "Cleaned Elapsed vs Node (2022)", "file": "Cleaned_ElapsedvsNode_2022.html"},
    {"title": "Cleaned Elapsed vs Node (2023)", "file": "Cleaned_ElapsedvsNode_2023.html"},
    {"title": "Cleaned Elapsed vs Node (2024)", "file": "Cleaned_ElapsedvsNode_2024.html"},
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
    # Combined one is not needed
    #{"title": "Node vs Diffsec (All Years)", "file": "Combined_Node_vs_Diffsec_AllYears.html"},
]

ORNL_GREEN = "#006341"
ORNL_LIGHT = "#e6f2ed"

app = dash.Dash(__name__)
app.title = "ORNL Dashboard"

app.layout = html.Div([
    html.H1(
        "ORNL Data Dashboard",
        style={
            "textAlign": "center",
            "marginBottom": "20px",
            "color": ORNL_GREEN,
            "fontWeight": "bold",
            "letterSpacing": "2px",
            "fontFamily": "Segoe UI, Arial, sans-serif"
        }
    ),dcc.Tabs(id="tabs", value="general", children=[
        dcc.Tab(label="General", value="general"),
        dcc.Tab(label="Backfilled Job Data", value="cleaned"),
        dcc.Tab(label="Timing Data", value="timing"),
    ],  style={
            "background": ORNL_GREEN,
            "color": ORNL_GREEN,
            "borderRadius": "8px",
            "fontFamily": "Segoe UI, Arial, sans-serif",
        },
        colors={
            "border": ORNL_GREEN,
            "primary": ORNL_GREEN,
            "background": ORNL_LIGHT,
        }),
        html.Div(
            id="cleaned-dropdown-container",
            children=[
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
            ],
            style={"marginBottom": "20px", "display": "none"}  # Hidden by default
        ),

        html.Div(
            id="plots-container",
            style={
                "background": "#fff",
                "padding": "30px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 12px #b7b7b7",
                "marginTop": "20px",
                "border": f"2px solid {ORNL_GREEN}"
            }
        ),
    ], style={
        "maxWidth": "1800px",
        "margin": "auto",
        "fontFamily": "Segoe UI, Arial, sans-serif",
        "padding": "30px"
    })

@app.callback(
    Output("cleaned-dropdown-container", "style"),
    Input("tabs", "value"),
)

def toggle_dropdown_visibility(tab):
    if tab == "cleaned":
        return {"marginBottom": "20px", "display": "block"}
    return {"display": "none"}

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
    Input("cleaned-plot-type", "value"),
)
def update_plots(tab, cleaned_plot_type):
    if tab == "general":
        plots = GENERAL_PLOTS
        grid = []
        row = []
        for idx, plot in enumerate(plots):
            row.append(
                html.Div([
                    html.H3(plot["title"], style={"marginTop": "10px", "fontSize": "1.1em"}),
                    html.Iframe(
                        src=f"/assets/{plot['file']}",
                        style={"width": "100%", "height": "600px", "border": "1px solid #ccc", "borderRadius": "6px"}
                    )
                ], style={"width": "55%", "display": "inline-block", "verticalAlign": "top", "margin": "1%"})
            )
            if len(row) == 2 or idx == len(plots) - 1:
                grid.append(html.Div(row, style={"display": "flex", "justifyContent": "space-between"}))
                row = []
        return grid
    elif tab == "cleaned":
        if cleaned_plot_type == "heatmap":
            plots = CLEANED_HEATMAP_PLOTS
            return [
                html.Div([
                    html.H3(plot["title"], style={"marginTop": "30px", "fontSize": "1.1em"}),
                    html.Iframe(
                        src=f"/assets/{plot['file']}",
                        style={"width": "100%", "height": "700px", "border": "1px solid #ccc", "borderRadius": "6px"}
                    )
                ], style={"width": "100%", "marginBottom": "30px"})
                for plot in plots
            ]
        else:
            # Special layout for scatter: combined on top (2x1), then 2x2 grid with the rest
            combined_plot = CLEANED_SCATTER_PLOTS[0]
            year_plots = CLEANED_SCATTER_PLOTS[1:]

            combined_section = html.Div([
                html.H3(combined_plot["title"], style={"marginTop": "10px", "fontSize": "1.1em"}),
                html.Iframe(
                    src=f"/assets/{combined_plot['file']}",
                    style={"width": "100%", "height": "600px", "border": "1px solid #ccc", "borderRadius": "6px"}
                )
            ], style={"width": "100%", "marginBottom": "30px"})

            grid = []
            row = []
            for idx, plot in enumerate(year_plots):
                row.append(
                    html.Div([
                        html.H3(plot["title"], style={"marginTop": "10px", "fontSize": "1.1em"}),
                        html.Iframe(
                            src=f"/assets/{plot['file']}",
                            style={"width": "100%", "height": "600px", "border": "1px solid #ccc", "borderRadius": "6px"}
                        )
                    ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top", "margin": "1%"})
                )
                if len(row) == 2 or idx == len(year_plots) - 1:
                    grid.append(html.Div(row, style={"display": "flex", "justifyContent": "space-between"}))
                    row = []
            return [combined_section] + grid
    elif tab == "timing":
        plots = TIMING_PLOTS
        return [
            html.Div([
                html.H3(plot["title"], style={"marginTop": "30px", "fontSize": "1.1em"}),
                html.Iframe(
                    src=f"/assets/{plot['file']}",
                    style={"width": "100%", "height": "1100px", "border": "1px solid #ccc", "borderRadius": "6px"}
                )
            ], style={"width": "100%", "marginBottom": "30px"})
            for plot in plots
        ]

if __name__ == '__main__':
    app.run(debug=True, port=8051)