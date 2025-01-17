import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os

# Page configuration
st.set_page_config(
    page_title="Sri Lanka and Germany: Incidents Overview",
    page_icon="\U0001F1F1\U0001F1F0",
    layout='centered',
    initial_sidebar_state="expanded"
)

# File paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "data", "incidents"))
geojson_dir = base_dir  # GeoJSON files are in the same folder as this script

# Sidebar navigation
st.sidebar.markdown("""
### Navigation
- [Tsunami 2004](#tsunami-2004-in-sri-lanka)
- [Civil War](#sri-lankan-civil-war-2000-2009)
- [2008/09 Financial Crisis](#200809-financial-crisis-in-germany)
- [2015 Refugee Crisis](#2015-refugee-crisis-in-germany)
- [2019 Easter Attacks](#2019-easter-attacks-in-sri-lanka)
- [COVID-19 Pandemic](#covid-19-pandemic)
- [Economic Crisis](#economic-crisis-in-sri-lanka)
""")

# Title and Introduction
st.title("Incidents in Sri Lanka and Germany")
st.markdown("""Explore key historical incidents, their impact, and related interactive visualizations.""")

# Tsunami 2004 Section
st.header("Tsunami 2004 in Sri Lanka")
st.markdown("""
The 2004 Indian Ocean tsunami was one of the deadliest natural disasters in history.
It occurred on December 26, 2004, triggered by a 9.1-9.3 magnitude undersea earthquake.
Sri Lanka was among the worst-affected countries, with significant loss of life,
destruction of infrastructure, and economic devastation.
""")

try:
    tsunami_df = pd.read_csv(os.path.join(data_dir, "tsunami_data.csv"))
    tsunami_fig = px.scatter_mapbox(
        tsunami_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="District",
        hover_data=["Deaths", "Damage"],
        color_discrete_sequence=["red"],
        zoom=7,
        center={"lat": 7.8731, "lon": 80.7718},
    )
    tsunami_fig.update_layout(
        mapbox_style="carto-positron",
        title="Sri Lanka Tsunami 2004 Affected Districts",
        height=800,
        width=1000
    )
    st.plotly_chart(tsunami_fig)
except FileNotFoundError:
    st.error("Tsunami data file not found. Please ensure 'tsunami_data.csv' is located in the 'data/incidents/' directory.")




# Civil War Section
st.header("Sri Lankan Civil War (2000-2009)")
st.markdown("""
The Sri Lankan Civil War was a prolonged armed conflict between the government and the LTTE.
It caused widespread destruction and loss of life, particularly in the Northern and Eastern provinces.
""")

try:
    civil_war_df = pd.read_csv(os.path.join(data_dir, "civil_war_events_2000_2009.csv"))
    
    # Explicitly cast numeric columns to object to allow 'N/A'
    numeric_columns = ["Army Casualties", "LTTE Casualties", "Civilian Casualties"]
    for col in numeric_columns:
        civil_war_df[col] = civil_war_df[col].astype(object)
    
    civil_war_df.fillna("N/A", inplace=True)  # Replace empty values with 'N/A'

    selected_year = st.slider("Select a year to view events", 2000, 2009, 2000)
    filtered_df = civil_war_df[civil_war_df["Year"] == selected_year]

    civil_war_fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Description",
        hover_data={
            "Year": True,
            "Army Casualties": True,
            "LTTE Casualties": True,
            "Civilian Casualties": True
        },
        color_discrete_sequence=["blue"],
        zoom=7,
        center={"lat": 7.8731, "lon": 80.7718},
    )
    civil_war_fig.update_layout(
        mapbox_style="carto-positron",
        title=f"Sri Lankan Civil War Events in {selected_year}",
        height=800,
        width=1000
    )
    st.plotly_chart(civil_war_fig)
except FileNotFoundError:
    st.error("Civil war data file not found. Please ensure 'civil_war_events_2000_2009.csv' is located in the 'data/incidents/' directory.")




# 2008/09 Financial Crisis Section
st.header("2008/09 Financial Crisis in Germany")
st.markdown("""
The 2008/09 financial crisis had a significant impact on Germany, Europe's largest economy.
It caused a contraction in industrial output, increased unemployment, and higher government spending.
""")

try:
    financial_crisis_df = pd.read_csv(os.path.join(data_dir, "financial_crisis_data.csv"))
    financial_crisis_df.fillna("N/A", inplace=True)  # Replace empty values with 'N/A'

    financial_crisis_fig = px.scatter_mapbox(
        financial_crisis_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="State",
        hover_data={
            "2008 Unemployment Rate (%)": True,
            "2009 Unemployment Rate (%)": True,
            "2008 Industrial Output Change (%)": True,
            "2009 Industrial Output Change (%)": True
        },
        color_discrete_sequence=["darkred"],
        zoom=5,
        center={"lat": 51.1657, "lon": 10.4515},
    )
    financial_crisis_fig.update_layout(
        mapbox_style="carto-positron",
        title="Germany 2008/09 Financial Crisis Impact",
        height=800,
        width=1000
    )
    st.plotly_chart(financial_crisis_fig)
except FileNotFoundError:
    st.error("Financial crisis data file not found. Please ensure 'financial_crisis_data.csv' is located in the 'data/incidents/' directory.")

# 2015 Refugee Crisis Section
st.header("2015 Refugee Crisis in Germany")
st.markdown("""
In 2015, Germany became a primary destination for refugees fleeing conflict, particularly from Syria, Afghanistan, and Iraq.
The crisis placed significant strain on resources but highlighted Germany's humanitarian efforts.
""")

try:
    refugee_crisis_df = pd.read_csv(os.path.join(data_dir, "refugee_crisis_data.csv"))
    refugee_crisis_fig = px.scatter_mapbox(
        refugee_crisis_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="State",
        hover_data=["Refugees Accepted", "Cost (Million Euros)"],
        color_discrete_sequence=["green"],
        zoom=5,
        center={"lat": 51.1657, "lon": 10.4515},
    )
    refugee_crisis_fig.update_layout(
        mapbox_style="carto-positron",
        title="Germany Refugee Crisis Impact",
        height=800,
        width=1000
    )
    st.plotly_chart(refugee_crisis_fig)
except FileNotFoundError:
    st.error("Refugee crisis data file not found. Please ensure 'refugee_crisis_data.csv' is located in the 'data/incidents/' directory.")

# 2019 Easter Attacks Section
st.header("2019 Easter Attacks in Sri Lanka")
st.markdown("""
The 2019 Easter attacks were a series of coordinated bombings targeting churches and hotels in Sri Lanka.
These attacks resulted in significant loss of life and were among the deadliest in the country's history.
""")

try:
    easter_attacks_df = pd.read_csv(os.path.join(data_dir, "easter_attacks_data.csv"))
    easter_attacks_fig = px.scatter_mapbox(
        easter_attacks_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Location",
        hover_data=["Killed", "Injured", "Terrorists Killed"],
        color_discrete_sequence=["orange"],
        zoom=7,
        center={"lat": 7.8731, "lon": 80.7718},
    )
    easter_attacks_fig.update_layout(
        mapbox_style="carto-positron",
        title="Easter Attacks Locations",
        height=800,
        width=1000
    )
    st.plotly_chart(easter_attacks_fig)
except FileNotFoundError:
    st.error("Easter attacks data file not found. Please ensure 'easter_attacks_data.csv' is located in the 'data/incidents/' directory.")





# COVID-19 Pandemic Section
st.header("COVID-19 Pandemic")
st.markdown("""
The COVID-19 pandemic had a profound impact globally, including in Germany and Sri Lanka.
It caused waves of infections, significant fatalities, and widespread economic challenges.
""")

try:
    covid_df = pd.read_csv(os.path.join(data_dir, "covid_data.csv"))

    # Combine data for both countries
    fig = go.Figure()
    for country in covid_df['Country'].unique():
        country_data = covid_df[covid_df['Country'] == country]
        if country == "Germany":
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Infections'],
                name=f"{country} Infections",
                marker_color="blue"
            ))
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Deaths'],
                name=f"{country} Deaths",
                marker_color="red"
            ))
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Economic Loss (Billion USD)'],
                name=f"{country} Economic Loss",
                marker_color="purple"
            ))
        else:
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Infections'],
                name=f"{country} Infections",
                marker_color="green"
            ))
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Deaths'],
                name=f"{country} Deaths",
                marker_color="orange"
            ))
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Economic Loss (Billion USD)'],
                name=f"{country} Economic Loss",
                marker_color="cyan"
            ))

    fig.update_layout(
        title="COVID-19 Impact in Germany and Sri Lanka",
        barmode="group",
        xaxis_title="Year",
        yaxis_title="Values",
        height=800,
        width=1000,
        legend=dict(
            groupclick="toggleitem"  # Group legend items for clarity
        )
    )
    st.plotly_chart(fig)
except FileNotFoundError:
    st.error("COVID-19 data file not found. Please ensure 'covid_data.csv' is located in the 'data/incidents/' directory.")


# Economic Crisis Section
st.header("Economic Crisis in Sri Lanka")
st.markdown("""
The Sri Lankan economic crisis, starting in 2019, is considered the worst since independence in 1948.
It was marked by unsustainable debt, inflation, and shortages of essential goods.
""")

try:
    economic_crisis_df = pd.read_csv(os.path.join(data_dir, "economic_crisis_data.csv"))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=economic_crisis_df['Year'],
        y=economic_crisis_df['GDP Growth (%)'],
        name="GDP Growth (%)",
        marker_color="blue"
    ))
    fig.add_trace(go.Bar(
        x=economic_crisis_df['Year'],
        y=economic_crisis_df['Inflation (%)'],
        name="Inflation (%)",
        marker_color="red"
    ))
    fig.add_trace(go.Bar(
        x=economic_crisis_df['Year'],
        y=economic_crisis_df['Debt to GDP Ratio (%)'],
        name="Debt to GDP Ratio (%)",
        marker_color="green"
    ))
    fig.add_trace(go.Bar(
        x=economic_crisis_df['Year'],
        y=economic_crisis_df['Unemployment Rate (%)'],
        name="Unemployment Rate (%)",
        marker_color="orange"
    ))

    fig.update_layout(
        title="Sri Lanka Economic Crisis Indicators",
        barmode="group",
        xaxis_title="Year",
        yaxis_title="Percentage",
        height=800,
        width=1000,
        legend=dict(
            groupclick="toggleitem"  # Group legend items for clarity
        )
    )
    st.plotly_chart(fig)
except FileNotFoundError:
    st.error("Economic crisis data file not found. Please ensure 'economic_crisis_data.csv' is located in the 'data/incidents/' directory.")

# Footer
st.markdown("""
---
This dashboard provides a comparative study of significant incidents in Sri Lanka and Germany.
""")
