from os import PathLike

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# TODO: load other data
# TODO: https://plotly.com/python/range-slider/
# TODO: decide on styling (colors, marks, etc.)

inflation_path = '../../data/inflation/results.csv'
GDP_path = '../../data/GDP/results.csv'
happiness_path = '../../data/happiness/results.csv'
tourism_path = '../../data/tourism/sltda.csv'


def load_inflation_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    years = pd.date_range(start='2000', end='2025', freq='YE').strftime('%Y')
    return {
        "de": pd.Series(np.random.normal(2, 1, len(years)), index=years),
        "sl": pd.Series(np.random.normal(6, 3, len(years)), index=years)
    }


def load_GDP_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    years = pd.date_range(start='2000', end='2024', freq='YE').strftime('%Y')
    return {
        "de": pd.Series(
            np.linspace(25000, 45000, len(years)) + np.random.normal(0, 1000, len(years)),
            index=years
        ),
        "sl": pd.Series(
            np.linspace(2000, 4000, len(years)) + np.random.normal(0, 200, len(years)),
            index=years
        )
    }


def load_happiness_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = df.xs('Germany', level=1)
    sl = df.xs('Sri Lanka', level=1)
    return {"de": de, "sl": sl}


def load_tourism_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0])
    return {"sl": df}


def load_data(
    inflation_path: str | PathLike[str],
    GDP_path: str | PathLike[str],
    happiness_path: str | PathLike[str],
    tourism_path: str | PathLike[str]
) -> dict[str, dict[str, pd.DataFrame]]:
    data = {
        'inflation': load_inflation_data(inflation_path),
        'GDP': load_GDP_data(GDP_path),
        'happiness': load_happiness_data(happiness_path),
        'tourism': load_tourism_data(tourism_path)
    }
    return data


def plot_inflation_data(data: dict[str, dict[str, pd.DataFrame]]):
    fig = go.Figure()
    for country, label in [('sl', 'Sri Lanka'), ('de', 'Germany')]:
        fig.add_trace(
            go.Scatter(
                x=data['inflation'][country].index,
                y=data['inflation'][country].values,
                name=label,
                hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>Inflation: %{{y:.1f}}%<br><extra></extra>"
            )
        )

    fig.update_layout(
        title_text="Inflation",
        yaxis=dict(range=[0, 20]),
        hovermode='x unified'
    )

    return fig


def plot_GDP_data(data: dict[str, dict[str, pd.DataFrame]]):
    fig = go.Figure()
    for country, label in [('sl', 'Sri Lanka'), ('de', 'Germany')]:
        fig.add_trace(
            go.Scatter(
                x=data['GDP'][country].index,
                y=data['GDP'][country].values,
                name=label,
                hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>GDP per capita: $%{{y:,.0f}}<br><extra></extra>"
            )
        )

    fig.update_layout(
        title_text="GDP per capita",
        yaxis=dict(range=[0, 50000]),
        hovermode='x unified'
    )

    return fig


def plot_happiness_data(data: dict[str, dict[str, pd.DataFrame]]):
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Rank: %{customdata[2]:.0f}<br>"
        "Happiness score: %{y:.2f}<br>"
        "GDP per capita: %{customdata[3]:.3f}<br>"
        "Social support: %{customdata[4]:.3f}<br>"
        "Healthy life expectancy: %{customdata[5]:.3f}<br>"
        "Freedom to make life choices: %{customdata[6]:.3f}<br>"
        "Generosity: %{customdata[7]:.3f}<br>"
        "Perceptions of corruption: %{customdata[8]:.3f}<br>"
        "Dystopia + residual: %{customdata[9]:.3f}<br>"
        "<extra></extra>"
    ) # HTML

    COLORS = {'Germany': '#4DB6AC', 'Sri Lanka': '#FF7043'}
    for country, data_df in [('Sri Lanka', data['happiness']['sl']), ('Germany', data['happiness']['de'])]:
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
        yaxis=dict(range=[0, 10])
    )

    return fig


def plot_tourism_data(data: dict[str, dict[str, pd.DataFrame]]):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['tourism']['sl'].index,
            y=data['tourism']['sl']['tourists arrived'],
            name='Sri Lanka',
            hovertemplate="<b>Sri Lanka</b><br>Year: %{x}<br>Tourists: %{y:,.0f}<br><extra></extra>"
        )
    )

    fig.update_layout(
        title_text="Tourism",
        yaxis=dict(range=[0, 3e6])
    )

    return fig


def plot_data(data: dict[str, dict[str, pd.DataFrame]]):
    st.title("Sri Lanka Indicators")
    row1_cols = st.columns(2)
    row2_cols = st.columns(2)

    figs = [
        plot_inflation_data(data),  # Top left
        plot_GDP_data(data),        # Top right
        plot_happiness_data(data),  # Bottom left
        plot_tourism_data(data)     # Bottom right
    ]

    common_layout = dict(
        height=400,
        xaxis=dict(range=[1999, 2025]),
        showlegend=False,
    )

    common_traces = dict(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )

    for column, fig in zip(row1_cols + row2_cols, figs):
        fig.update_layout(**common_layout)
        fig.update_traces(**common_traces)
        with column:
            st.plotly_chart(fig)


data = load_data(inflation_path, GDP_path, happiness_path, tourism_path)
plot_data(data)
