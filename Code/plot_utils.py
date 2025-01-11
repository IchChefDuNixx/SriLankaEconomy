import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


COLORS = {'Inflation': '#FF7043',
          'GDP': '#4DB6AC',
          'Happiness': '#81C784',
          'Tourism': '#7986CB',
          'Germany': '#4DB6AC',
          'Sri Lanka': '#FF7043'}


def plot_panel1(data: dict[str, dict[str, pd.DataFrame]]) -> None:
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

    # Filter data while handling missing values
    all_years = np.arange(2000, 2025)
    visible_years = all_years[all_years <= selected_year]

    inflation_filtered = data['inflation']['sl']['Inflation'].reindex(visible_years)
    gdp_filtered = data['GDP']['sl']['GDP per capita (current US$)'].reindex(visible_years)
    happiness_filtered = data['happiness']['sl']['Happiness score'].reindex(visible_years)
    tourism_filtered = data['tourism']['sl']['tourists arrived'].reindex(visible_years)

    common_traces = dict(
        y=visible_years,
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )

    # plot data
    fig = go.Figure()

    for i, (data, name) in enumerate([
        (inflation_filtered, 'Inflation'),
        (gdp_filtered, 'GDP'),
        (happiness_filtered, 'Happiness'),
        (tourism_filtered, 'Tourism')
    ], start=1):
        fig.add_trace(
            go.Scatter(
                x=data,
                xaxis=f"x{i}",  # Use different x-axis for each trace
                line_color=COLORS[name],
                **common_traces
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
    st.plotly_chart(fig)


def plot_inflation_data(data: dict[str, dict[str, pd.DataFrame]]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Inflation: <b>%{y:.1f}%</b><br>"
        "<extra></extra>"
    )

    # different order because sri lanka's line is above germany
    # different order affects the tooltip order
    # high inflation = bad whereas high gdp/happiness/tourism = good
    for country, df in [('Sri Lanka', data['sl']), ('Germany', data['de'])]:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Inflation'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
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


def plot_GDP_data(data: dict[str, dict[str, pd.DataFrame]]) -> go.Figure:
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

# TODO: text to explain composition of happiness score
# TODO: ask breunig about dotted line methodology change
def plot_happiness_data(data: dict[str, dict[str, pd.DataFrame]]) -> go.Figure:
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


def plot_tourism_data(data: dict[str, dict[str, pd.DataFrame]]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Tourists: <b>%{y:,.0f}</b><br>"
        "<extra></extra>"
    )

    for country, df in [('Germany', data['de']), ('Sri Lanka', data['sl'])]:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['tourists arrived'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                )),
                hovertemplate=hovertemplate
            )
        )

    fig.update_layout(
        title_text="Yearly Tourist Arrivals",
        yaxis=dict(range=[0, 41e6])  # Removed fixed range to accommodate both countries
    )

    return fig


def plot_panel2(data: dict[str, dict[str, pd.DataFrame]]) -> None:
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

    row1_cols = st.columns(2)
    row2_cols = st.columns(2)

    figs = [
        plot_inflation_data(data['inflation']), # Top left
        plot_GDP_data(data['GDP']),             # Top right
        plot_happiness_data(data['happiness']), # Bottom left
        plot_tourism_data(data['tourism'])      # Bottom right
    ]

    for column, fig in zip(row1_cols + row2_cols, figs):
        fig.update_layout(**common_layout)
        fig.update_traces(**common_traces)
        with column:
            st.plotly_chart(fig)
