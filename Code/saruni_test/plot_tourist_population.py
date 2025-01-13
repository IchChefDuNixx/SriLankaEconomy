import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# todo : hovering info
# seperate graph for germany
# ' should we change the graphs?'

current_population_sl = 22040000 # 22.04 million (2023)
current_population_sl = 84480000 # 84.48 million (2023)

# Load the data
data_file = 'srilanka/data/tourism/tourism_arrival_srilanka.csv'
data = pd.read_csv(data_file)

# Streamlit app title
st.title('Yearly Tourist Arrivals in Sri Lanka')

# Slider for selecting a year
min_year = int(data['Year'].min())
max_year = int(data['Year'].max())
selected_year = st.slider(
    'Select a year:',
    min_value=min_year,
    max_value=max_year,
    value=min_year  # Default year
)

# Filter data to include only years up to the selected year
filtered_data = data[data['Year'] <= selected_year]

# Create the base figure
fig = go.Figure()

# Add the line and scatter points for the selected data
fig.add_trace(go.Scatter(
    x=filtered_data['Year'],
    y=filtered_data['tourists arrived'],
    mode='lines+markers',
    name='Tourist Arrivals'
))

# Update layout
fig.update_layout(
    title=f"Yearly Tourist Arrivals in Sri Lanka (up to {selected_year})",
    xaxis_title="Year",
    yaxis_title="Number of Tourists",
    xaxis=dict(range=[min_year, max_year]),
    yaxis=dict(range=[0, data['tourists arrived'].max()]),
)

# Display the graph in Streamlit
st.plotly_chart(fig)
