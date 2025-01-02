import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

# TODO: load other data
# TODO: add other plots
# TODO: decide on styling (colors, marks, etc.)
STYLING = {
    'mode': 'lines+markers',  # Add line+markers mode
    'line': dict(width=2),    # Set consistent line width
    'marker': dict(size=6),   # Set consistent marker size
    'showlegend': False,
}

def load_inflation_data(path):
    years = pd.date_range(start='2000', end='2025', freq='Y').strftime('%Y')
    return {
        "de": pd.Series(np.random.normal(2, 1, len(years)), index=years),
        "sl": pd.Series(np.random.normal(6, 3, len(years)), index=years)
    }

def load_GDP_data(path):
    years = pd.date_range(start='2000', end='2024', freq='Y').strftime('%Y')
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

def load_data():
    inflation_path = '../../srilanka/data/inflation/results.csv'
    GDP_path = '../../srilanka/data/GDP/results.csv'
    happiness_path = '../../srilanka/data/happiness/results.csv'
    tourism_path = '../../srilanka/data/tourism/sltda.csv'

    data = {
        'inflation': load_inflation_data(inflation_path),
        'GDP': load_GDP_data(GDP_path),
        'happiness': load_happiness_data(happiness_path),
        'tourism': load_tourism_data(tourism_path)
    }
    return data

def plot_inflation_data(data, fig):
    for country, label in [('sl', 'Sri Lanka'), ('de', 'Germany')]:
        fig.add_trace(
            go.Scatter(
                x=data['inflation'][country].index,
                y=data['inflation'][country].values,
                name=label,
                hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>Inflation: %{{y:.1f}}%<br><extra></extra>",
                **STYLING,
            ),
            row=1, col=1
        )

def plot_GDP_data(data, fig):
    for country, label in [('sl', 'Sri Lanka'), ('de', 'Germany')]:
        fig.add_trace(
            go.Scatter(
                x=data['GDP'][country].index,
                y=data['GDP'][country].values,
                name=label,
                hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>GDP per capita: $%{{y:,.0f}}<br><extra></extra>",
                **STYLING,
            ),
            row=1, col=2
        )

def plot_happiness_data(data, fig):
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

    # Plot happiness data for Sri Lanka and Germany, splitting into pre-2015 and post-2015 periods
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
                        hovertemplate=hovertemplate,
                        **STYLING,
                    ),
                    row=2, col=1
                )
    fig.update_yaxes(range=[0, 10], row=2, col=1)

def plot_tourism_data(data, fig):
    fig.add_trace(
        go.Scatter(
            x=data['tourism']['sl'].index,
            y=data['tourism']['sl']['tourists arrived'],
            name='Sri Lanka',
            hovertemplate="<b>Sri Lanka</b><br>Year: %{x}<br>Tourists: %{y:,.0f}<br><extra></extra>",
            **STYLING,
        ),
        row=2, col=2
    )
    fig.update_yaxes(range=[0, 3e6], row=2, col=2)

def plot_data(data, fig):
    plot_inflation_data(data, fig)
    plot_GDP_data(data, fig)
    plot_happiness_data(data, fig)
    plot_tourism_data(data, fig)

data = load_data()
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Inflation', 'GDP', 'Happiness Score', 'Tourism')
)
fig.update_layout(
    height=800, # TODO: make this dynamic?
    title_text="Sri Lanka Indicators", # TODO
    xaxis=dict(range=[2000, 2025])
)
plot_data(data, fig)

# render website
st.plotly_chart(fig)
