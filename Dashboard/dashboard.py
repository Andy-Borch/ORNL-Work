import dash
from dash import html, dcc, Input, Output
from dash.dependencies import Input, Output, State

# Define which HTML files to show in each tab
GENERAL_PLOTS = [
    {"title": "Job Wait Time Distribution", "file": "WaitTimevsJobID.html"},
    {"title": "Jobs Submitted Over Time", "file": "Num_Jobs_Over_Time.html"},
    {"title": "Jobs Submitted per User", "file": "Jobs_Submitted_per_User.html"},
    {"title": "Node Count by Year", "file": "Node_Count_by_Year.html"},
    {"title": "Elapsed Time Distribution by Year", "file": "Elapsed_Time_Distribution_by_Year.html"},
]

CLEANED_SCATTER_PLOTS = [
    {"title": "Elapsed Time vs Node Count (All Years)", "file": "Cleaned_ElapsedvsNode_AllYears.html"},
    {"title": "Elapsed Time vs Node Count (2021)", "file": "Cleaned_ElapsedvsNode_2021.html"},
    {"title": "Elapsed Time vs Node Count (2022)", "file": "Cleaned_ElapsedvsNode_2022.html"},
    {"title": "Elapsed Time vs Node Count (2023)", "file": "Cleaned_ElapsedvsNode_2023.html"},
    {"title": "Elapsed Time vs Node Count (2024)", "file": "Cleaned_ElapsedvsNode_2024.html"},
]

CLEANED_HEATMAP_PLOTS = [
    {"title": "Elapsed Time vs Node Count Heatmap (2021)", "file": "Cleaned_ElapsedvsNode_Heatmap_2021.html"},
    {"title": "Elapsed Time vs Node Count Heatmap (2022)", "file": "Cleaned_ElapsedvsNode_Heatmap_2022.html"},
    {"title": "Elapsed Time vs Node Count Heatmap (2023)", "file": "Cleaned_ElapsedvsNode_Heatmap_2023.html"},
    {"title": "Elapsed Time vs Node Count Heatmap (2024)", "file": "Cleaned_ElapsedvsNode_Heatmap_2024.html"},
]

TIMING_PLOTS = [
    {"title": "Node Count vs Difference in Seconds (2021)", "file": "Node_vs_Diffsec_2021.html"},
    {"title": "Node Count vs Difference in Seconds (2022)", "file": "Node_vs_Diffsec_2022.html"},
    {"title": "Node Count vs Difference in Seconds (2023)", "file": "Node_vs_Diffsec_2023.html"},
    {"title": "Node Count vs Difference in Seconds (2024)", "file": "Node_vs_Diffsec_2024.html"},
]

# Define ORNL color palette
ORNL_GREEN = "#006341"
ORNL_DARK_GREEN = "#004d33" # A darker shade for accents
ORNL_LIGHT_GREEN = "#e6f2ed"
ORNL_GREY = "#f0f2f5" # Light grey for background
ORNL_DARK_GREY = "#4a4a4a" # For text

app = dash.Dash(__name__)
app.title = "ORNL Data Dashboard"

app.layout = html.Div([
    # Main container with a subtle background and consistent font
    html.Div(
        style={
            "fontFamily": "Inter, 'Segoe UI', Arial, sans-serif", # Prioritize Inter for modern look
            "backgroundColor": ORNL_GREY,
            "minHeight": "100vh", # Ensure background covers full height
            "padding": "30px 20px"
        },
        children=[
            # Header section
            html.H1(
                "ORNL Data Dashboard",
                style={
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "color": ORNL_DARK_GREEN,
                    "fontWeight": "800", # Bolder font weight
                    "letterSpacing": "1.5px",
                    "fontSize": "2.8em", # Larger font size
                    "paddingBottom": "10px",
                    "borderBottom": f"3px solid {ORNL_GREEN}" # Underline effect
                }
            ),

            # Tabs container
            dcc.Tabs(
                id="tabs",
                value="general",
                children=[
                    dcc.Tab(
                        label="General Metrics",
                        value="general",
                        style={
                            "padding": "15px 25px",
                            "fontWeight": "600",
                            "color": ORNL_DARK_GREY,
                            "borderTopLeftRadius": "8px",
                            "borderTopRightRadius": "8px",
                            "border": "1px solid #d4d4d4",
                            "borderBottom": "none",
                            "marginRight": "5px",
                            "backgroundColor": "#ffffff"
                        },
                        selected_style={
                            "padding": "15px 25px",
                            "fontWeight": "700",
                            "color": "white",
                            "backgroundColor": ORNL_GREEN,
                            "borderTopLeftRadius": "8px",
                            "borderTopRightRadius": "8px",
                            "border": f"1px solid {ORNL_GREEN}",
                            "borderBottom": "none"
                        }
                    ),
                    dcc.Tab(
                        label="Backfilled Job Data Analysis",
                        value="cleaned",
                        style={
                            "padding": "15px 25px",
                            "fontWeight": "600",
                            "color": ORNL_DARK_GREY,
                            "borderTopLeftRadius": "8px",
                            "borderTopRightRadius": "8px",
                            "border": "1px solid #d4d4d4",
                            "borderBottom": "none",
                            "marginRight": "5px",
                            "backgroundColor": "#ffffff"
                        },
                        selected_style={
                            "padding": "15px 25px",
                            "fontWeight": "700",
                            "color": "white",
                            "backgroundColor": ORNL_GREEN,
                            "borderTopLeftRadius": "8px",
                            "borderTopRightRadius": "8px",
                            "border": f"1px solid {ORNL_GREEN}",
                            "borderBottom": "none"
                        }
                    ),
                    dcc.Tab(
                        label="Timing Data Insights",
                        value="timing",
                        style={
                            "padding": "15px 25px",
                            "fontWeight": "600",
                            "color": ORNL_DARK_GREY,
                            "borderTopLeftRadius": "8px",
                            "borderTopRightRadius": "8px",
                            "border": "1px solid #d4d4d4",
                            "borderBottom": "none",
                            "backgroundColor": "#ffffff"
                        },
                        selected_style={
                            "padding": "15px 25px",
                            "fontWeight": "700",
                            "color": "white",
                            "backgroundColor": ORNL_GREEN,
                            "borderTopLeftRadius": "8px",
                            "borderTopRightRadius": "8px",
                            "border": f"1px solid {ORNL_GREEN}",
                            "borderBottom": "none"
                        }
                    ),
                ],
                # General tab styling
                style={
                    "backgroundColor": ORNL_LIGHT_GREEN,
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 15px rgba(0,0,0,0.1)",
                    "border": f"1px solid {ORNL_GREEN}",
                    "overflow": "hidden"
                },
                # Styling for the container that holds the tabs
                colors={
                    "border": ORNL_GREEN,
                    "primary": ORNL_GREEN,
                    "background": ORNL_LIGHT_GREEN,
                }
            ),

            # Dropdown for cleaned plots, hidden by default
            html.Div(
                id="cleaned-dropdown-container",
                children=[
                    html.Label(
                        "Select Plot Type:",
                        style={
                            "marginRight": "15px",
                            "fontWeight": "600",
                            "color": ORNL_DARK_GREY
                        }
                    ),
                    dcc.Dropdown(
                        id="cleaned-plot-type",
                        options=[
                            {"label": "Scatter Plots", "value": "scatter"},
                            {"label": "Heatmap Plots", "value": "heatmap"},
                        ],
                        value="scatter",
                        clearable=False,
                        style={
                            "width": "250px",
                            "display": "inline-block",
                            "verticalAlign": "middle",
                            "borderRadius": "5px",
                            "boxShadow": "0 2px 5px rgba(0,0,0,0.05)",
                            "border": f"1px solid {ORNL_GREEN}"
                        },
                        className="custom-dropdown" # Add a class for potential external CSS
                    )
                ],
                style={
                    "marginTop": "25px",
                    "marginBottom": "25px",
                    "display": "none", # Hidden by default, controlled by callback
                    "backgroundColor": "#ffffff",
                    "padding": "15px 25px",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
                    "border": f"1px solid {ORNL_LIGHT_GREEN}"
                }
            ),

            # Container for plots, wrapped with a loading component
            dcc.Loading(
                id="loading-plots",
                type="cube", # Or "graph", "dot", "default"
                color=ORNL_GREEN,
                children=[
                    html.Div(
                        id="plots-container",
                        style={
                            "backgroundColor": "#ffffff",
                            "padding": "30px",
                            "borderRadius": "10px",
                            "boxShadow": "0 4px 20px rgba(0,0,0,0.15)",
                            "marginTop": "20px",
                            "border": f"2px solid {ORNL_LIGHT_GREEN}"
                        }
                    )
                ]
            ),
        ]
    )
])

# Callback to control visibility of the cleaned plot type dropdown
@app.callback(
    Output("cleaned-dropdown-container", "style"),
    Input("tabs", "value"),
)
def toggle_dropdown_visibility(tab):
    if tab == "cleaned":
        # Make it visible with some margin
        return {
            "marginTop": "25px",
            "marginBottom": "25px",
            "display": "flex", # Use flex for alignment
            "alignItems": "center",
            "justifyContent": "flex-start", # Align to the left
            "backgroundColor": "#ffffff",
            "padding": "15px 25px",
            "borderRadius": "8px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
            "border": f"1px solid {ORNL_LIGHT_GREEN}"
        }
    return {"display": "none"} # Hide it

# Callback to update the plots displayed based on tab and dropdown selection
@app.callback(
    Output("plots-container", "children"),
    Input("tabs", "value"),
    Input("cleaned-plot-type", "value"),
)
def update_plots(tab, cleaned_plot_type):
    # Base style for plot containers within the grid
    plot_card_style = {
        "backgroundColor": "#f8f9fa",
        "padding": "20px",
        "borderRadius": "8px",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.05)",
        "border": f"1px solid {ORNL_LIGHT_GREEN}",
        "marginBottom": "25px" # Consistent margin bottom for all cards
    }

    # Style for plot titles
    plot_title_style = {
        "marginTop": "10px",
        "marginBottom": "20px",
        "fontSize": "1.4em", # Slightly larger title
        "color": ORNL_DARK_GREEN,
        "fontWeight": "600",
        "textAlign": "center"
    }

    # Style for Iframes
    iframe_style = {
        "width": "100%",
        "minHeight": "450px", # Minimum height to prevent collapse
        "height": "auto", # Allow height to adjust
        "border": "none", # Remove default iframe border
        "borderRadius": "6px",
        "boxShadow": "inset 0 0 5px rgba(0,0,0,0.05)" # Subtle inner shadow
    }

    if tab == "general":
        plots = GENERAL_PLOTS
        grid = []
        row_items = []
        for idx, plot in enumerate(plots):
            row_items.append(
                html.Div([
                    html.H3(plot["title"], style=plot_title_style),
                    html.Iframe(
                        src=f"/assets/{plot['file']}",
                        style={**iframe_style, "height": "600px"} # Specific height for general plots
                    )
                ], style={**plot_card_style, "flex": "1 1 calc(50% - 20px)", "margin": "10px"}) # Flex item with margin
            )
            # If two items are collected or it's the last plot
            if len(row_items) == 2 or idx == len(plots) - 1:
                grid.append(
                    html.Div(
                        row_items,
                        style={"display": "flex", "justifyContent": "space-around", "width": "100%", "marginBottom": "10px"} # Add margin to rows
                    )
                )
                row_items = [] # Reset row for next pair
        return html.Div(grid) # Return the full grid of rows

    elif tab == "cleaned":
        if cleaned_plot_type == "heatmap":
            plots = CLEANED_HEATMAP_PLOTS
            return html.Div([
                html.Div([
                    html.H3(plot["title"], style=plot_title_style),
                    html.Iframe(
                        src=f"/assets/{plot['file']}",
                        style={**iframe_style, "height": "700px"} # Specific height for heatmaps
                    )
                ], style={**plot_card_style, "width": "100%"})
                for plot in plots
            ], style={"display": "flex", "flexDirection": "column", "alignItems": "center"})
        else: # cleaned_plot_type == "scatter"
            combined_plot = CLEANED_SCATTER_PLOTS[0]
            year_plots = CLEANED_SCATTER_PLOTS[1:]

            combined_section = html.Div(
                [
                    html.H3(combined_plot["title"], style=plot_title_style),
                    html.Iframe(
                        src=f"/assets/{combined_plot['file']}",
                        style={**iframe_style, "height": "600px"} # Specific height for combined scatter
                    )
                ],
                style={**plot_card_style, "width": "100%"} # Full width for combined plot
            )

            grid = []
            row = []
            for idx, plot in enumerate(year_plots):
                row.append(
                    html.Div([
                        html.H3(plot["title"], style=plot_title_style),
                        html.Iframe(
                            src=f"/assets/{plot['file']}",
                            style={**iframe_style, "height": "600px"} # Specific height for year scatter plots
                        )
                    ], style={**plot_card_style, "flex": "1 1 calc(50% - 20px)", "margin": "10px"}) # Flex item for 2x2 grid
                )
                # If two items are collected or it's the last plot
                if len(row) == 2 or idx == len(year_plots) - 1:
                    grid.append(html.Div(row, style={"display": "flex", "justifyContent": "space-around"}))
                    row = []
            return [combined_section] + grid

    elif tab == "timing":
        plots = TIMING_PLOTS
        return html.Div([
            html.Div([
                html.H3(plot["title"], style=plot_title_style),
                html.Iframe(
                    src=f"/assets/{plot['file']}",
                    style={**iframe_style, "height": "1100px"} # Specific height for timing plots
                )
            ], style={**plot_card_style, "width": "100%"})
            for plot in plots
        ], style={"display": "flex", "flexDirection": "column", "alignItems": "center"})


if __name__ == '__main__':
    app.run(debug=True, port=8051)
