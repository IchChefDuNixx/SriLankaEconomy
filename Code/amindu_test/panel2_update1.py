import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# File path to the CSV containing inflation values and reasons
inflation_path = 'data/inflation/Inflation_Germany_SriLanka_2000_2023.csv'
GDP_path = 'data/gdp/gdp_de_sl.csv'
happiness_path = 'data/happiness/results_new.csv'
tourism_path = 'data/tourism/tourism_de_sl.csv'
COLORS = {'Germany': '#4DB6AC', 'Sri Lanka': '#FF7043'}

def load_inflation_data(path: str):
    df = pd.read_csv(path, index_col=0)
    de = df[df['Country'] == 'Germany'][['Inflation Value (%)', 'Reason']].rename(columns={'Inflation Value (%)': 'Value', 'Reason': 'Reason'})
    sl = df[df['Country'] == 'Sri Lanka'][['Inflation Value (%)', 'Reason']].rename(columns={'Inflation Value (%)': 'Value', 'Reason': 'Reason'})
    return {"de": de, "sl": sl}


def load_GDP_data(path: str) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = df.xs('Germany', level=1)
    sl = df.xs('Sri Lanka', level=1)
    return {"de": de, "sl": sl}

def load_happiness_data(path: str) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = df.xs('Germany', level=1)
    sl = df.xs('Sri Lanka', level=1)
    return {"de": de, "sl": sl}

def load_tourism_data(path: str) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    sl = df.xs('Sri Lanka', level=1)
    de = df.xs('Germany', level=1)
    return {"sl": sl, "de": de}

def load_data(
    inflation_path: str,
    GDP_path: str,
    happiness_path: str,
    tourism_path: str
) -> dict[str, dict[str, pd.DataFrame]]:
    data = {
        'inflation': load_inflation_data(inflation_path),
        'GDP': load_GDP_data(GDP_path),
        'happiness': load_happiness_data(happiness_path),
        'tourism': load_tourism_data(tourism_path)
    }
    return data

def plot_inflation_data(data: dict[str, dict[str, pd.DataFrame]], year_range: tuple[int, int]) -> go.Figure:
    fig = go.Figure()
    
    for country, label in [('sl', 'Sri Lanka'), ('de', 'Germany')]:
        # Filter the data based on the selected year range
        country_data = data[country].loc[year_range[0]:year_range[1]]

        fig.add_trace(
            go.Scatter(
                x=country_data.index,
                y=country_data['Value'],
                name=label,
                customdata=np.column_stack((
                    country_data['Reason'],  # Add the 'Reason' column to customdata
                )),
                hovertemplate=(
                    f"<b>{label}</b><br>Year: %{{x}}<br>Inflation: %{{y:.1f}}%<br>Reason: %{{customdata[0]}}<br><extra></extra>"
                )
            )
        )

    fig.update_layout(
        title_text="Inflation",
        yaxis=dict(range=[0, 20]),
        hovermode='x unified'
    )

    return fig


def plot_GDP_data(data: dict[str, dict[str, pd.DataFrame]]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
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

def plot_happiness_data(data: dict[str, dict[str, pd.DataFrame]]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Rank: #%{customdata[2]:.0f}<br>"
        "Happiness Score: <b>%{y:.2f}</b><br><br>"
        "Score Breakdown:<br>"
        "GDP per capita: <b>+%{customdata[3]:.3f}</b><br>"
        "Social support: <b>+%{customdata[4]:.3f}</b><br>"
        "Healthy life expectancy: <b>+%{customdata[5]:.3f}</b><br>"
        "Freedom to make life choices: <b>+%{customdata[6]:.3f}</b><br>"
        "Generosity: <b>+%{customdata[7]:.3f}</b><br>"
        "Perceptions of corruption: <b>+%{customdata[8]:.3f}</b><br>"
        "Dystopia + residual: <b>+%{customdata[9]:.3f}</b><br>"
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
        line_color="gray"
    )

    fig.add_annotation(
        x=2014.5,
        y=10,
        text="Methodology change",
        showarrow=False
    )

    fig.update_layout(
        title_text="Happiness Score",
        yaxis=dict(range=[0, 10]), # 10 or 10.5
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


def plot_data(data: dict[str, dict[str, pd.DataFrame]]) -> None:
    st.title("Sri Lanka Indicators") # TODO: improve title

    # Add time range selector at the top
    year_range = st.slider(
        "Select Time Period",
        min_value=2000,
        max_value=2024,
        value=(2000, 2024)
    )

    # Common layout and trace settings for consistency across charts
    common_layout = dict(
        height=400,
        xaxis=dict(range=(year_range[0] - 1, year_range[1] + 1)),
        showlegend=False,
    )

    common_traces = dict(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )

    row1_cols = st.columns(2)
    row2_cols = st.columns(2)

    figs = [
        plot_inflation_data(data['inflation'],(2000,2023)), # Top left
        plot_GDP_data(data['GDP']),             # Top right
        plot_happiness_data(data['happiness']), # Bottom left
        plot_tourism_data(data['tourism'])      # Bottom right
    ]

    for column, fig in zip(row1_cols + row2_cols, figs):
        fig.update_layout(**common_layout)
        fig.update_traces(**common_traces)
        with column:
            st.plotly_chart(fig)

# Load the data
data = load_data(inflation_path, GDP_path, happiness_path, tourism_path)

# Plot the data
plot_data(data)
