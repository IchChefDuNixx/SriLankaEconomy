import streamlit as st
import plotly.graph_objects as go
import numpy as np

# TODO: fancy tooltips
# TODO: optimize ticks
# TODO: make modular/functions

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
