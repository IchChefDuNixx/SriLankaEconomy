
# app.py
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit_scroll_component import ScrollComponent  # You'll need to create this package

def create_visualization(selected_year):
    years = np.arange(2000, 2025)
    
    # Your existing data arrays
    inflation = np.array([6.2, 14.2, 9.6, 6.3, 7.6, 11.0, 10.0, 15.8, 22.6, 3.5,
                         6.2, 6.7, 7.5, 6.9, 3.3, 3.8, 4.0, 7.7, 4.3, 4.8,
                         6.2, 7.0, 70.0, 45.0, 12.0])
    
    gdp = np.array([869, 840, 904, 1010, 1063, 1242, 1421, 1614, 2014, 2057,
                    2744, 3223, 3351, 3609, 3819, 3842, 3857, 4077, 4057, 3848,
                    3337, 3682, 3293, 3354, 3500])
    
    happiness = np.array([4.2, 4.2, 4.2, 4.3, 4.3, 4.3, 4.4, 4.4, 4.4, 4.4,
                          4.2, 4.2, 4.2, 4.3, 4.3, 4.4, 4.4, 4.4, 4.3, 4.3,
                          4.1, 4.0, 3.8, 3.9, 4.0])
    
    tourism = np.array([0.4, 0.34, 0.39, 0.50, 0.57, 0.55, 0.56, 0.49, 0.44, 0.45,
                        0.65, 0.86, 1.01, 1.27, 1.53, 1.80, 2.05, 2.12, 2.33, 1.91,
                        0.51, 0.15, 0.19, 0.33, 0.42])

    mask = (years >= 2000) & (years <= selected_year)
    years_filtered = years[mask]
    
    fig = go.Figure()
    
    # Add traces with custom hover templates
    fig.add_trace(go.Scatter(
        x=inflation[mask],
        y=years_filtered,
        name="Inflation (%)",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{y}<br>Inflation: %{x:.1f}%<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=gdp[mask],
        y=years_filtered,
        xaxis="x2",
        name="GDP per capita",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{y}<br>GDP: $%{x:,.0f}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=happiness[mask],
        y=years_filtered,
        xaxis="x3",
        name="Happiness",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{y}<br>Score: %{x:.1f}/10<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=tourism[mask],
        y=years_filtered,
        xaxis="x4",
        name="Tourism",
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{y}<br>Arrivals: %{x:.2f}M<extra></extra>"
    ))

    # Update layout with improved styling
    fig.update_layout(
        height=600,
        margin=dict(t=80, b=40),
        xaxis=dict(
            domain=[0, 0.23],
            range=[0, 90],
            title=dict(text="Inflation (%)", standoff=15),
            side="top",
            gridcolor='lightgray'
        ),
        xaxis2=dict(
            domain=[0.27, 0.48],
            range=[0, 4500],
            title=dict(text="GDP per capita (USD)", standoff=15),
            side="top",
            gridcolor='lightgray'
        ),
        xaxis3=dict(
            domain=[0.52, 0.73],
            range=[0, 9],
            title=dict(text="Happiness Score", standoff=15),
            side="top",
            gridcolor='lightgray'
        ),
        xaxis4=dict(
            domain=[0.77, 1],
            range=[0, 2.5],
            title=dict(text="Tourism (millions)", standoff=15),
            side="top",
            gridcolor='lightgray'
        ),
        yaxis=dict(
            range=[2024.5, 1999.5],
            tickmode='linear',
            dtick=5,
            gridcolor='lightgray'
        ),
        yaxis2=dict(showticklabels=False, range=[2024.5, 1999.5]),
        yaxis3=dict(showticklabels=False, range=[2024.5, 1999.5]),
        yaxis4=dict(showticklabels=False, range=[2024.5, 1999.5]),
        showlegend=False,
        plot_bgcolor='white',
        hovermode="y unified"
    )
    
    return fig

def main():
    st.title("Economic Indicators Over Time")
    st.markdown("Scroll to explore the data through the years")
    
    # Add the custom scroll component
    year = ScrollComponent()
    
    if year is None:
        year = 2000
    
    # Create and display the visualization
    fig = create_visualization(year)
    st.plotly_chart(fig, use_container_width=True)
    
    # Add some context below the chart
    st.markdown(f"""
    ### Year: {year}
    
    Key observations for {year}:
    - Inflation: {inflation[year-2000]:.1f}%
    - GDP per capita: ${gdp[year-2000]:,.0f}
    - Happiness Score: {happiness[year-2000]:.1f}/10
    - Tourism Arrivals: {tourism[year-2000]:.2f}M
    """)

if __name__ == "__main__":
    main()