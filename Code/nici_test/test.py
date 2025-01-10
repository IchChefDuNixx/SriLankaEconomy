import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def create_dashboard():
    # Set page config
    st.set_page_config(layout="wide", page_title="Sri Lanka Economic Indicators")

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stSlider > div > div > div > div {
            background-color: #ff4b4b;
        }
        .css-1v0mbdj.ebxwdo61 {
            width: 100%;
            max-width: 100%;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sample data (replace with your actual data)
    years = list(range(2000, 2021))
    data = {
        'Inflation': {
            'values': [6.2, 14.2, 9.6, 6.3, 7.6, 11.6, 10.0, 15.8, 22.6, 3.5,
                       6.2, 6.7, 7.5, 6.9, 3.3, 3.8, 4.0, 7.7, 2.1, 4.3, 6.0],
            'color': '#EF4444',
            'range': [0, 25],
            'suffix': '%'
        },
        'GDP per capita': {
            'values': [855, 840, 870, 984, 1063, 1242, 1422, 1614, 2014, 2057,
                       2400, 2836, 3351, 3610, 3819, 3842, 3857, 4077, 3853, 3682, 3325],
            'color': '#22C55E',
            'range': [0, 4500],
            'suffix': ' USD'
        },
        'Happiness Score': {
            'values': [4.3, 4.3, 4.4, 4.4, 4.4, 4.3, 4.3, 4.2, 4.2, 4.3,
                       4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.1, 4.9, 4.8],
            'color': '#3B82F6',
            'range': [0, 6],
            'suffix': ''
        },
        'Tourist Arrivals': {
            'values': [400, 420, 450, 500, 550, 600, 650, 700, 750, 800,
                       900, 1000, 1200, 1400, 1600, 1800, 2000, 2100, 1900, 500, 700],
            'color': '#8B5CF6',
            'range': [0, 2500],
            'suffix': 'K'
        }
    }

    # Title and description
    st.title("Sri Lanka Economic Indicators")
    st.markdown("Interactive dashboard showing key economic and social indicators for Sri Lanka")

    # Year range slider
    selected_year = st.slider(
        "Select Year Range",
        min_value=min(years),
        max_value=max(years),
        value=2019,
        step=1
    )

    # Create subplot figure
    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=list(data.keys()),
        horizontal_spacing=0.02
    )

    # Add traces for each indicator
    for idx, (indicator, indicator_data) in enumerate(data.items(), 1):
        # Filter data based on selected year
        year_idx = years.index(selected_year) + 1
        filtered_years = years[:year_idx]
        filtered_values = indicator_data['values'][:year_idx]

        fig.add_trace(
            go.Scatter(
                x=filtered_values,
                y=filtered_years,
                mode='lines+markers',
                line=dict(
                    color=indicator_data['color'],
                    width=2
                ),
                marker=dict(
                    size=6,
                    color=indicator_data['color']
                ),
                name=indicator,
                customdata=[[year, val] for year, val in zip(filtered_years, filtered_values)],
                hovertemplate=(
                        "Year: %{customdata[0]}<br>" +
                        f"{indicator}: %{{customdata[1]:.1f}}{indicator_data['suffix']}<br>" +
                        "<extra></extra>"
                )
            ),
            row=1, col=idx
        )

        # Update layout for each subplot
        fig.update_xaxes(
            title_text=indicator,
            range=indicator_data['range'],
            row=1, col=idx,
            gridcolor='rgba(128, 128, 128, 0.1)',
            title_font=dict(size=12)
        )

    # Update y-axis properties
    fig.update_yaxes(
        range=[max(years) + 0.5, min(years) - 0.5],
        gridcolor='rgba(128, 128, 128, 0.1)',
        showgrid=True
    )

    # Update layout
    fig.update_layout(
        height=600,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='y unified',
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Arial, sans-serif"),
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Add explanatory text
    st.markdown("""
        ### Key Insights
        - The dashboard shows four key indicators for Sri Lanka from 2000 to 2020
        - Use the slider to explore different time periods
        - Hover over data points to see exact values
        - Each indicator is color-coded for easy identification
    """)


if __name__ == "__main__":
    create_dashboard()