# create a line chart with tooltips using plotly and streamlit
import pandas as pd
import streamlit as st
import plotly.express as px

# Custom CSS for vertical slider
st.markdown("""
    <style>
    .stSlider {
        transform: rotate(270deg);
        padding: 50px 0;
        width: 200px;
        margin-left: -75px;
    }
    div[data-baseweb="slider"] {
        width: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

# load data
df = pd.read_csv('../../srilanka/data/happiness/results.csv', index_col=[1])

# Combine data for both countries
combined_data = pd.concat([
    df.xs('Sri Lanka').assign(Country='Sri Lanka'),
    df.xs('Germany').assign(Country='Germany')
])

# Create two columns - one for slider and one for chart
col1, col2 = st.columns([1, 4])

# add a slider in the first column
with col1:
    st.write("")  # Add some spacing
    slider = st.slider('Select a value',
                      min_value=1,
                      max_value=5,
                      value=3)
    st.write(f'Value: {slider}')

# create a line chart
fig = px.line(combined_data,
              x='Happiness rank',
              y='Year',
              color='Country',
              title='Line Chart')

# Reverse the y-axis and set x-axis range
fig.update_layout(
    yaxis=dict(autorange="reversed"),
    xaxis=dict(range=[1, 150])
)

# add a tooltip to the chart
fig.update_traces(hovertemplate='x: %{x}, y: %{y}')

# display the chart in the second column
with col2:
    st.plotly_chart(fig, use_container_width=True)