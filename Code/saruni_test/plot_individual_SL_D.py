import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load the data for Sri Lanka
data_file_sl = 'srilanka/data/tourism/tourism_arrival_srilanka.csv'
data_sl = pd.read_csv(data_file_sl)

# Load the data for Germany
data_file_de = 'srilanka/data/tourism/tourists_germany.csv'
data_de = pd.read_csv(data_file_de)

# Add population data (assuming it's constant for simplicity)
population_sl = 22040000  # 22.04 million (2023)
population_de = 84480000  # 84.48 million (2023)

# Calculate percentages for Sri Lanka and Germany
data_sl['Percentage of Tourists'] = (data_sl['tourists arrived'] / population_sl) * 100
data_de['Percentage of Tourists'] = (data_de['tourists arrived'] / population_de) * 100

# Streamlit app title
st.title('Yearly Tourist Arrivals (Sri Lanka & Germany)')

# Slider for selecting a year
min_year = max(int(data_sl['Year'].min()), int(data_de['Year'].min()))
max_year = min(int(data_sl['Year'].max()), int(data_de['Year'].max()))
selected_year = st.slider(
    'Select a year:',
    min_value=min_year,
    max_value=max_year,
    value=min_year  # Default year
)

# Filter data to include only years up to the selected year
filtered_data_sl = data_sl[data_sl['Year'] <= selected_year]
filtered_data_de = data_de[data_de['Year'] <= selected_year]

# Create the figure for Sri Lanka
fig_sl = go.Figure()
fig_sl.add_trace(go.Scatter(
    x=filtered_data_sl['Year'],
    y=filtered_data_sl['Percentage of Tourists'],
    mode='lines+markers',
    name='Sri Lanka',
    hovertemplate=(
        'Year: %{x}<br>'
        'Percentage of Population: %{y:.2f}%<br>'
        'Number of Tourists: %{customdata:,}'),
    customdata=filtered_data_sl['tourists arrived']
))
fig_sl.update_layout(
    title=f"Yearly Tourist Arrivals in Sri Lanka (up to {selected_year}) as Percentage of Population",
    xaxis_title="Year",
    yaxis_title="Percentage of Population",
    xaxis=dict(range=[min_year, max_year]),
    yaxis=dict(range=[0, max(filtered_data_sl['Percentage of Tourists'].max()+2, 1)]),
)

# Create the figure for Germany
fig_de = go.Figure()
fig_de.add_trace(go.Scatter(
    x=filtered_data_de['Year'],
    y=filtered_data_de['Percentage of Tourists'],
    mode='lines+markers',
    name='Germany',
    hovertemplate=(
        'Year: %{x}<br>'
        'Percentage of Population: %{y:.2f}%<br>'
        'Number of Tourists: %{customdata:,}'),
    customdata=filtered_data_de['tourists arrived']
))
fig_de.update_layout(
    title=f"Yearly Tourist Arrivals in Germany (up to {selected_year}) as Percentage of Population",
    xaxis_title="Year",
    yaxis_title="Percentage of Population",
    xaxis=dict(range=[min_year, max_year]),
    yaxis=dict(range=[0, max(filtered_data_de['Percentage of Tourists'].max()+2, 1)]),
)

# Display the graphs in Streamlit
st.plotly_chart(fig_sl)
st.plotly_chart(fig_de)
