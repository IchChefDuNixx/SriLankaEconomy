import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# TODO: load other data
# TODO: https://plotly.com/python/range-slider/
# TODO: decide on styling (colors, marks, etc.)

inflation_path = '../../data/inflation/results.csv'
GDP_path = '../../data/GDP/results.csv'
happiness_path = '../../data/happiness/results.csv'
tourism_path = '../../data/tourism/sltda.csv'

def load_inflation_data(path):
    years = pd.date_range(start='2000', end='2025', freq='YE').strftime('%Y')
    return {
        "de": pd.Series(np.random.normal(2, 1, len(years)), index=years),
        "sl": pd.Series(np.random.normal(6, 3, len(years)), index=years)
    }

def load_GDP_data(path):
    years = pd.date_range(start='2000', end='2024', freq='YE').strftime('%Y')
    return {
        "de": pd.Series(np.linspace(25000, 45000, len(years)) + np.random.normal(0, 1000, len(years)), index=years),
        "sl": pd.Series(np.linspace(2000, 4000, len(years)) + np.random.normal(0, 200, len(years)), index=years)
    }

def load_happiness_data(path):
    df = pd.read_csv(path, index_col=[0, 1], dtype={'Year': str})
    de = df.xs('Germany', level=1)
    sl = df.xs('Sri Lanka', level=1)
    return {"de":de, "sl":sl}

def load_tourism_data(path):
    df = pd.read_csv(path, index_col=[0], dtype={'Year': str})
    return {"sl":df}

def load_data(inflation_path, GDP_path, happiness_path, tourism_path):
    data = {
        'inflation': load_inflation_data(inflation_path),
        'GDP': load_GDP_data(GDP_path),
        'happiness': load_happiness_data(happiness_path),
        'tourism': load_tourism_data(tourism_path)
    }
    return data

def plot_inflation_data(data):
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
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
    return fig

def plot_GDP_data(data):
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
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
    return fig

def plot_happiness_data(data):
    fig = go.Figure()
    hovertemplate = (
        "<b>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Rank: %{customdata[1]:.0f}<br>"
        "Happiness score: %{y:.2f}<br>"
        "GDP per capita: %{customdata[2]:.3f}<br>"
        "Social support: %{customdata[3]:.3f}<br>"
        "Healthy life expectancy: %{customdata[4]:.3f}<br>"
        "Freedom to make life choices: %{customdata[5]:.3f}<br>"
        "Generosity: %{customdata[6]:.3f}<br>"
        "Perceptions of corruption: %{customdata[7]:.3f}<br>"
        "Dystopia + residual: %{customdata[8]:.3f}<br>"
        "<extra></extra>"
    )

    for country, data_df in [('Sri Lanka', data['happiness']['sl']), ('Germany', data['happiness']['de'])]:
        for df in [data_df[data_df.index < '2015'], data_df[data_df.index >= '2015']]:
            if not df.empty:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['Happiness score'],
                        name=country,
                        customdata=np.column_stack((
                            [country] * len(df),
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
    # better data source starting from 2015
    fig.add_vline(
        x='2014.5',
        line_dash="dot",
        line_color="gray"
    )
    fig.add_annotation(
        x='2014.5',
        y=10,
        text="Methodology change",
        showarrow=False
    )
    fig.update_layout(
        title_text="Happiness Score",
        height=400,
        yaxis=dict(range=[0, 10]),
        showlegend=False
    )
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
    return fig

def plot_tourism_data(data):
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
        height=400,
        yaxis=dict(range=[0, 3e6]),
        showlegend=False
    )
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
    return fig

def plot_data(data):
    st.title("Sri Lanka Indicators")
    row1_cols = st.columns(2)
    row2_cols = st.columns(2)
    plot_functions = [
        plot_inflation_data,    # Top left
        plot_GDP_data,          # Top right
        plot_happiness_data,    # Bottom left
        plot_tourism_data       # Bottom right
    ]

    for column, plot_function in zip(row1_cols + row2_cols, plot_functions):
        with column:
            st.plotly_chart(plot_function(data))

data = load_data(inflation_path, GDP_path, happiness_path, tourism_path)
plot_data(data)
