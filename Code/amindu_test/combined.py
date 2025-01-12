import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os


# Panel 1 Content
st.header("Sri Lanka Indicators")

years = np.arange(2000, 2025)

# Inflation data (%) - fluctuating, very high in recent years
inflation = np.array([6.2, 14.2, 9.6, 6.3, 7.6, 11.0, 10.0, 15.8, 22.6, 3.5,
                     6.2, 6.7, 7.5, 6.9, 3.3, 3.8, 4.0, 7.7, 4.3, 4.8,
                     6.2, 7.0, 70.0, 45.0, 12.0])  # Last few years estimated

# GDP per capita (USD) - generally increasing but drop in recent crisis
gdp = np.array([869, 840, 904, 1010, 1063, 1242, 1421, 1614, 2014, 2057,
                2744, 3223, 3351, 3609, 3819, 3842, 3857, 4077, 4057, 3848,
                3337, 3682, 3293, 3354, 3500])  # Last few years estimated

# Happiness score (0-10) - relatively stable with recent decline
happiness = np.array([4.2, 4.2, 4.2, 4.3, 4.3, 4.3, 4.4, 4.4, 4.4, 4.4,
                     4.2, 4.2, 4.2, 4.3, 4.3, 4.4, 4.4, 4.4, 4.3, 4.3,
                     4.1, 4.0, 3.8, 3.9, 4.0])  # Some values interpolated

# Tourism arrivals (millions) - growing then sharp drop due to COVID & crisis
tourism = np.array([0.4, 0.34, 0.39, 0.50, 0.57, 0.55, 0.56, 0.49, 0.44, 0.45,
                    0.65, 0.86, 1.01, 1.27, 1.53, 1.80, 2.05, 2.12, 2.33, 1.91,
                    0.51, 0.15, 0.19, 0.33, 0.42])  # Recent years estimated

# Define specific years for the slider
year_options = [2000, 2004, 2009, 2018, 2019, 2021, 2022, 2024]

# Add slider for year range
selected_year = st.select_slider(
    "Select Year Range",
    options=year_options,
    value=2000,
    format_func=lambda x: str(int(x))
)

# Update the filter to use fixed start year
mask = (years >= 2000) & (years <= selected_year)
years_filtered = years[mask]
inflation_filtered = inflation[mask]
gdp_filtered = gdp[mask]
happiness_filtered = happiness[mask]
tourism_filtered = tourism[mask]

fig = go.Figure()

# Add traces with filtered data
fig.add_trace(
    go.Scatter(
        x=inflation_filtered,
        y=years_filtered,
        xaxis="x",
        yaxis="y",
        name="Inflation (%)",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
)

fig.add_trace(
    go.Scatter(
        x=gdp_filtered,
        y=years_filtered,
        xaxis="x2",
        yaxis="y2",
        name="GDP per capita (USD)",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
)

fig.add_trace(
    go.Scatter(
        x=happiness_filtered,
        y=years_filtered,
        xaxis="x3",
        yaxis="y3",
        name="Happiness Score (0-10)",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
)

fig.add_trace(
    go.Scatter(
        x=tourism_filtered,
        y=years_filtered,
        xaxis="x4",
        yaxis="y4",
        name="Tourism (millions)",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )
)

# Update layout with appropriate ranges and titles
fig.update_layout(
    xaxis=dict(
        domain=[0, 0.25],
        range=[0, 90],
        title="Inflation (%)",
        side="top"
    ),
    xaxis2=dict(
        domain=[0.25, 0.5],
        range=[0, 4500],
        title="GDP per capita",
        side="top"
    ),
    xaxis3=dict(
        domain=[0.5, 0.75],
        range=[0, 9],
        title="Happiness",
        side="top"
    ),
    xaxis4=dict(
        domain=[0.75, 1],
        range=[0, 2.5],
        title="Tourism",
        side="top"
    ),
    # Add these settings for all y-axes to reverse them
    yaxis=dict(range=[2025, 2000]),
    yaxis2=dict(range=[2025, 2000]),
    yaxis3=dict(range=[2025, 2000]),
    yaxis4=dict(range=[2025, 2000]),
    showlegend=False,
    hovermode="y unified"
)

st.plotly_chart(fig, use_container_width=True)

# Panel 2 Content
st.header("Sri Lanka And Germany Indicators Comparison")

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
