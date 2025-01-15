import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import json


st.set_page_config(
    page_title="SRI LANKA'S JOURNEY: A comparative study with germany",
    page_icon="🇱🇰",
    layout='centered', # or wide
    initial_sidebar_state="collapsed")


COLORS = {'good': '#34C759',
          'bad': '#FF3737',
          'neutral': '#808080',
          'inflation': '#FF7043',
          'GDP': '#4DB6AC',
          'happiness': '#81C784',
          'tourism': '#7986CB',
          'Germany': '#4DB6AC',
          'Sri Lanka': '#FF7043'}


def plot_panel1(data: dict[str, dict[str, pd.DataFrame]], sl_events: dict[int, dict[str, int | str]]) -> None:

    # here (as function call?)
    st.write("""
    Here by moving through specific years using the timeline, 
    we can see how events happened in these years affected inflation rates, GDP, tourism industry, and happiness of its citizens.
    """)

    st.title("Sri Lanka Indicators")

    # TODO: fancy tooltips
    # TODO: optimize ticks
    # TODO: make modular/functions

    # Define specific years for the slider
    year_options = [2000, 2004, 2009, 2018, 2019, 2021, 2022, 2024]
    selected_year = st.select_slider(
        "Select Year Range",
        options=year_options,
        value=2000, # == starting value
        format_func=lambda x: str(int(x))
    )
    assert type(selected_year) == int # typ checking fix


    # Display the selected event name and description
    try:
        with st.container(border=True, height=150):
            # st.write(f"**Year:** {selected_year}")
            st.page_link(
                # page=f"pages/PLACEHOLDER.py{'#'+sl_events[selected_year]["Event"] if False else ""}", # TODO: unfinished!
                label=f"**{sl_events[selected_year]['Event']}**" + " (THIS IS A BUTTON)")
            st.write(f"{sl_events[selected_year]['Description']}")

    except Exception as e:
        st.write("Error loading event descriptions!")
        st.write(e)


    # Filter data while handling missing values
    all_years = np.arange(2000, 2025)
    visible_years = all_years[all_years <= selected_year]

    inflation_filtered = data['inflation']['sl']['Inflation Value (%)'].reindex(visible_years)
    gdp_filtered = data['GDP']['sl']['GDP per capita (current US$)'].reindex(visible_years)
    happiness_filtered = data['happiness']['sl']['Happiness score'].reindex(visible_years)
    tourism_filtered = data['tourism']['sl']['tourists arrived'].reindex(visible_years)


    g, b, n = COLORS["good"], COLORS["bad"], COLORS["neutral"]

    color_highlights = {
        "inflation": [
            (2000, n),
            (2004, n),
            (2005, b),
            (2006, n),
            (2008, b),
            (2009, g),
            (2021, n),
            (2022, b),
            (2025, n)
        ],
        "GDP": [
            (2000, n),
            (2009, n),
            (2011, g),
            (2021, n),
            (2022, b),
            (2025, n),
        ],
        "happiness": [
            (2000, n),
            (2015, n),
            (2018, g),
            (2023, n),
            (2025, b),
        ],
        "tourism": [
            (2000, n),
            (2009, n),
            (2018, g),
            (2021, b),
            (2025, n),
        ],
    }

    common_traces = dict(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6),#, color=n),
        hoverinfo="none", # TODO: would be nice to see the year (y-value without the line color inside the tooltip)
    )

    # plot data
    fig = go.Figure()

    for i, (filtered_data, metric) in enumerate([
        (inflation_filtered, 'inflation'),
        (gdp_filtered, 'GDP'),
        (happiness_filtered, 'happiness'),
        (tourism_filtered, 'tourism')
    ], start=1):
        for (start_year, _), (end_year, color) in zip(color_highlights[metric], color_highlights[metric][1:]):
            selection=filtered_data[(filtered_data.index >= start_year) & (filtered_data.index <= end_year)]

            fig.add_trace(
                go.Scatter(
                    x=selection,
                    y=selection.index,
                    xaxis=f"x{i}",      # Use different x-axis for each metric
                    line_color=color,   # if color != n else COLORS[metric],
                    # only highlight markers inside sections >= 2 years
                    marker_color=[n] + [color]*(len(selection) - 2) + [color if len(selection) > 1 else n],
                    **common_traces,
                )
            )


    # don't touch domain or side
    fig.update_layout(
        xaxis1=dict(
            domain=[0, 0.25],
            range=[0, 55],
            title="Inflation (%)",
            side="top"
        ),
        xaxis2=dict(
            domain=[0.25, 0.5],
            range=[0, 5100],
            title="GDP per capita",
            side="top"
        ),
        xaxis3=dict(
            domain=[0.5, 0.75],
            range=[0, 9],
            title="Happiness Score",
            side="top"
        ),
        xaxis4=dict(
            domain=[0.75, 1],
            range=[0, 2.5e6],
            title="Yearly Tourist Arrivals",
            side="top"
        ),

        # Reverse range and styling
        yaxis=dict(range=[2025.1, 1999.8]),

        showlegend=False,
        hovermode="y unified",
        height=600
    )

    # Add vertical lines between subplots
    for x in [0.25, 0.5, 0.75]:
        fig.add_vline(
            x=x,
            xref="paper",
            line_dash="dot",
            line_color="gray",
            line_width=0.25
        )

    # render in streamlit
    st.plotly_chart(fig, use_container_width=True)


def plot_inflation_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        # "Year: %{x}<br>"
        "Inflation: <b>%{y:.1f}%</b><br>"
        "Reason: %{customdata[2]}<br>"
        "<extra></extra>"
    )

    # different order because sri lanka's line is above germany
    # different order affects the tooltip order
    # high inflation = bad whereas high gdp/happiness/tourism = good
    for country, df in [('Sri Lanka', data['sl']), ('Germany', data['de'])]:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                # y=df['Inflation'],
                y=df['Inflation Value (%)'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                    df['Reason']
                )),
                hovertemplate=hovertemplate
            )
        )

    fig.update_layout(
        title_text="Inflation",
        yaxis=dict(range=[0, 51]),
        hovermode='x unified'
    )

    return fig


def plot_GDP_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        # "Year: %{x}<br>"
        "GDP per capita: <b>%{customdata[2]:,.0f}</b> US$<br>"
        "GDP: <b>%{customdata[3]:,.1f}</b> billion US$<br>"
        "Gov. debt: <b>%{customdata[4]:.1f}%</b> of GDP<br>"
        "Industry: <b>%{customdata[5]:.1f}%</b> of GDP<br>"
        "Agriculture: <b>%{customdata[6]:.1f}%</b> of GDP<br>"
        "Services: <b>%{customdata[7]:.1f}%</b> of GDP<br>"
        "Military exp.: <b>%{customdata[8]:.2f}%</b> of GDP<br>"
        "<extra></extra>"
    ) # HTML

    for country, df in [('Germany', data['de']), ('Sri Lanka', data['sl'])]:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['GDP per capita (current US$)'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                    df['GDP per capita (current US$)'],
                    df['GDP (billion US$)'],
                    df['Government debt (% of GDP)'],
                    df['Industry (including construction), value added (% of GDP)'],
                    df['Agriculture, forestry, and fishing, value added (% of GDP)'],
                    df['Services, value added (% of GDP)'],
                    df['Military expenditure (% of GDP)'],
                )),
                hovertemplate=hovertemplate
            )
        )

    fig.update_layout(
        title_text="GDP per capita",
        yaxis=dict(range=[0, 61000]),
        hovermode='x unified'
    )

    return fig


# TODO: ask breunig about dotted line methodology change
def plot_happiness_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Rank: #%{customdata[2]:.0f}<br>"
        "Happiness Score: <b>%{y:.2f}</b><br><br>"
        "Score Breakdown:<br>"
        "GDP per capita: <b>%{customdata[3]:.3f}</b><br>"
        "Social support: <b>%{customdata[4]:.3f}</b><br>"
        "Healthy life expectancy: <b>%{customdata[5]:.3f}</b><br>"
        "Freedom to make life choices: <b>%{customdata[6]:.3f}</b><br>"
        "Generosity: <b>%{customdata[7]:.3f}</b><br>"
        "Perceptions of corruption: <b>%{customdata[8]:.3f}</b><br>"
        "Dystopia + residual: <b>%{customdata[9]:.3f}</b><br>"
        "<extra></extra>"
    ) # HTML

    for country, data_df in [('Germany', data['de']), ('Sri Lanka', data['sl'])]:
        # better data source starting from 2015
        for df in [data_df[data_df.index < 2015], data_df[data_df.index >= 2015]]:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['Happiness score'],
                    line=dict(color=COLORS[country]),
                    customdata=np.column_stack((
                        [country] * len(df),
                        [COLORS[country]] * len(df),
                        df['Happiness rank'],
                        df['GDP per capita'],
                        df['Social support'],
                        df['Healthy life expectancy'],
                        df['Freedom to make life choices'],
                        df['Generosity'],
                        df['Perceptions of corruption'],
                        df['Dystopia + residual']
                    )),
                    hovertemplate=hovertemplate
                )
            )

    # Missing data
    fig.add_vrect(
        x0=1999.1,
        x1=2004.5,
        label=dict(
            text="No Data",
            textposition="middle center",
            font=dict(size=14, color="gray")
        ),
        fillcolor="rgba(211, 211, 211, 0.2)",
        opacity=0.4,
        line_width=2,
        line_dash="dash",
        line_color="gray"
    )

    # better data source starting from 2015
    fig.add_vline(
        x=2014.5,
        line_dash="dot",
        line_color="gray",
        line_width=1
    )

    fig.add_annotation(
        x=2014.5,
        y=10,
        text="Methodology change",
        showarrow=False
    )

    fig.update_layout(
        title_text="Happiness Score",
        yaxis=dict(range=[0, 10.05]), # 10 or 10.05
        # hovermode='x unified'
    )

    return fig


def plot_tourism_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        # "Year: %{x}<br>"
        "Tourists per capita: <b>%{y:,.3f}</b><br>"
        "Total Tourists: <b>%{customdata[2]:,.1f} million</b><br>"
        "Population: <b>%{customdata[3]:,.1f} million</b><br>"
        "<extra></extra>"
    )

    for country, df in [('Germany', data['de']), ('Sri Lanka', data['sl'])]:
        df['tourists_per_capita'] = df['tourists arrived'] / df['population']

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['tourists_per_capita'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                    df["tourists arrived"] / 1e6,
                    df["population"] / 1e6
                )),
                hovertemplate=hovertemplate
            )
        )

    fig.update_layout(
        title_text="Yearly Tourist Arrivals per capita",
        yaxis=dict(range=[0, 0.51]),
        hovermode='x unified'
    )

    return fig

def load_plot_descriptions(file_path: str) -> dict[str, str]:
    """
    Load plot descriptions from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict[str, str]: A dictionary with plot keys as keys and descriptions as values.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error(f"Error loading plot descriptions: {e}")
        return {}

def plot_panel2(data: dict[str, dict[str, pd.DataFrame]], plot_desc: dict[int, dict[str, str]]) -> None:
    st.title("Comparison Charts") # TODO: improve title

    # Add time range selector at the top
    year_range = st.slider(
        "Select Time Period",
        min_value=2000,
        max_value=2024,
        value=(2000, 2024)
    )

    # TODO: styling
    common_layout = dict(
        height=400,
        # Extend range by 1 year on each side for better visualization
        xaxis=dict(range=(year_range[0] - 1, year_range[1] + 1)),
        showlegend=False,
    )

    # TODO: styling
    common_traces = dict(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )

    # row1_cols = st.columns(2)
    # row2_cols = st.columns(2)

    # figs = [
    #     plot_inflation_data(data['inflation']), # Top left
    #     plot_GDP_data(data['GDP']),             # Top right
    #     plot_happiness_data(data['happiness']), # Bottom left
    #     plot_tourism_data(data['tourism'])      # Bottom right
    # ]

    # for column, fig in zip(row1_cols + row2_cols, figs):
    #     fig.update_layout(**common_layout, overwrite=False)
    #     fig.update_traces(**common_traces, overwrite=False)
    #     with column:
    #         st.plotly_chart(fig, use_container_width=True)

# List of plots and their corresponding keys
    figs_and_keys = [
        (plot_inflation_data(data['inflation']), "inflation"),
        (plot_GDP_data(data['GDP']), "GDP"),
        (plot_happiness_data(data['happiness']), "happiness"),
        (plot_tourism_data(data['tourism']), "tourism")
    ]

    for fig, key in figs_and_keys:
        col1, col2 = st.columns([2, 1])  # Column widths: 2/3 for plot, 1/3 for text

        # Configure the plot
        fig.update_layout(**common_layout, overwrite=False)
        fig.update_traces(**common_traces, overwrite=False)

        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            description = plot_desc.get(key, "Description not available")
            st.write(f"**{key.capitalize()}**")
            st.write(description)
            
            # st.write(plot_desc.get(plot_key, "Description not available"))
            
                # Display the selected event name and description
            # try:
            #     if plot_key in plot_desc:
            #         description = plot_desc[plot_key]
            #         with st.container():
            #     # Display the description for the plot
            #             st.write(f"**{plot_key.capitalize()} Plot Description**")
            #             st.write(description)
            #     else:
            #         st.write(f"No description available for the {plot_key} plot.")
            # except Exception as e:
            #     st.write("Error loading plot description!")
            #     st.write(e)

            # Center-align the text description
            # st.markdown(
            #     f"""
            #     <div style="text-align: center; font-size: 16px;">
            #         {plot_descriptions[key]}
            #     </div>
            #     """,
            #     unsafe_allow_html=True
            # )