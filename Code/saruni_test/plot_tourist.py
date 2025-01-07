import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
data_file = 'srilanka/data/tourism/tourism_arrival_srilanka.csv'
data = pd.read_csv(data_file)

# Create the line graph using Plotly
fig = px.line(
    data, 
    x='Year', 
    y='tourists arrived', 
    title='Yearly Tourist Arrivals in Sri Lanka',
    labels={'Year': 'Year', 'Tourist_Count': 'Number of Tourists'},
    markers=True
)

# Display the graph in Streamlit
st.plotly_chart(fig)