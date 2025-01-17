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
- [Status Quo in Sri Lanka](#status-quo-in-sri-lanka)
- [Tsunami 2004](#tsunami-2004-in-sri-lanka)
- [Civil War](#sri-lankan-civil-war-2000-2009)
- [2008/09 Financial Crisis](#200809-financial-crisis-in-germany)
- [2015 Refugee Crisis](#2015-refugee-crisis-in-germany)
- [2019 Easter Attacks](#2019-easter-attacks-in-sri-lanka)
- [Tourism Boom](#tourism-boom-in-sri-lanka)
- [COVID-19 Pandemic](#covid-19-pandemic)
- [Economic Crisis](#economic-crisis-in-sri-lanka)
- [Protests against the Government](#protests-against-the-government)
- [Today](#today)
""")

# Title and Introduction
st.title("Incidents in Sri Lanka and Germany")
st.markdown("""Explore key historical incidents, their impact, and related interactive visualizations.""")

# Status Quo in Sri Lanka section
st.header("Status Quo in Sri Lanka")
st.markdown("""
In 2000, Sri Lanka's socio-economic situation was shaped by a mix of challenges and developments:

**Civil War Impact:** The country was in the midst of a prolonged civil war between the government and the Liberation Tigers of Tamil Eelam (LTTE). This conflict had significant economic and social repercussions, including reduced foreign investment, limited economic growth, and high defense spending.

**Economic Growth:** Despite the conflict, Sri Lanka maintained modest economic growth, driven by sectors like tea exports, textiles, and remittances from overseas workers. However, poverty and inequality remained significant issues, particularly in rural and war-affected areas.

**Global Relationships:** Sri Lanka's economy was reliant on global trade, with exports such as tea, rubber, and garments being crucial. Economic ties with countries like the United States, Europe, and neighboring India were essential.

**Political Climate:** The political landscape was polarized, with frequent changes in government and challenges in addressing corruption and governance. Efforts to negotiate peace with the LTTE often stalled, prolonging instability.

In summary, Sri Lanka in 2000 was a nation with significant potential but was constrained by conflict, socio-economic inequality, and political instability.
""")

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
        hover_data={
            "Deaths": True,
            "Damage": True,
            "Latitude": False,
            "Longitude": False
        },
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
            "Civilian Casualties": True,
            "Latitude": False,
            "Longitude": False
        },
        color_discrete_sequence=["red"],
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
            "2009 Industrial Output Change (%)": True,
            "Latitude": False,
            "Longitude": False
        },
        color_discrete_sequence=["red"],
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
        hover_data={"Refugees Accepted": True, "Cost (Million Euros)": True, "Latitude": False, "Longitude": False},
        color_discrete_sequence=["red"],
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



# Tourism Boom Section
st.header("Tourism Boom in Sri Lanka")
st.markdown("""
Before the 2019 Easter Attacks, Sri Lanka experienced a tourism boom, with the country being recognized
as a top travel destination. The tourism sector significantly contributed to foreign exchange earnings
and employment opportunities, showcasing the country's cultural and natural attractions.
""")

try:
    tourism_df = pd.read_csv(os.path.join(data_dir, "Tourism_Sri_Lanka_2016_2019.csv"))

    tourism_fig = px.line(
        tourism_df,
        x="Year",
        y="Arrivals_in_Millions",
        title="Tourist Arrivals in Sri Lanka (2016-2019)",
        markers=True,
        line_shape="spline",
        hover_data=["Revenue_in_Billions_USD"]
    )
    tourism_fig.update_traces(line_color="red")
    tourism_fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Arrivals (in Millions)",
        height=600,
        width=900
    )
    st.plotly_chart(tourism_fig)
except FileNotFoundError:
    st.error("Tourism data file not found. Please ensure 'Tourism_Sri_Lanka_2016_2019.csv' is located in the 'data/incidents/' directory.")



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
        hover_data={"Killed": True, "Injured": True, "Terrorists Killed": True, "Latitude": False, "Longitude": False},
        color_discrete_sequence=["red"],
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
        marker_color="purple"
    ))
    fig.add_trace(go.Bar(
        x=economic_crisis_df['Year'],
        y=economic_crisis_df['Unemployment Rate (%)'],
        name="Unemployment Rate (%)",
        marker_color="orange"
    ))

    fig.update_layout(
        title="Economic Crisis Impact in Sri Lanka",
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
    st.error("Economic crisis data file not found. Please ensure 'economic_crisis_data.csv' is located in the 'data/incidents/' directory.")

# Protests against the Government Section
st.header("Protests against the Government")
st.markdown("""
Year of 2022 has witnessed significant protests against the Sri Lankan government, driven by economic hardships,
social inequalities, and political dissatisfaction. These protests, often led by citizens from diverse backgrounds,
have brought attention to critical issues such as corruption, inflation, and governance failures.

**Major Protest Movements:**
- In 2022, mass demonstrations erupted due to severe shortages of essential goods and skyrocketing inflation.
- Youth-led movements highlighted the need for systemic reforms and accountability.

**Impact:**
These protests have resulted in notable political changes, including leadership transitions and increased calls for transparency
and reform in governance.
""")

# Today Section
st.header("Sri Lanka Today")
st.markdown("""
In 2025, Sri Lanka's socio-economic situation reflects a nation in recovery and transition:

**Economic Stabilization and Growth:** Following a severe economic downturn in 2022, Sri Lanka's economy has shown signs of stabilization.
The World Bank projects a growth rate of 4.4% for 2024, indicating a positive trajectory. This recovery is supported by declining inflation
and a current account surplus, bolstered by increased remittances and a rebound in tourism.

**Poverty and Inequality:** Despite economic improvements, poverty levels remain elevated. As of mid-2024, approximately 24.8% of the population
lived below the poverty line, highlighting ongoing challenges in income inequality and labor market disparities.

**Political Developments:** In September 2024, Anura Kumara Dissanayake, a Marxist lawmaker, was elected president, reflecting a public desire for
change from traditional political elites. His administration faces the task of implementing economic reforms and managing international relationships
to support the nation's recovery.

**International Support and Debt Restructuring:** Sri Lanka continues to engage with international partners for financial assistance. China has expressed
commitment to aiding Sri Lanka in achieving financial relief and debt sustainability. Additionally, the International Monetary Fund (IMF) approved the third review
of Sri Lanka's $2.9 billion bailout, emphasizing the need for continued reforms and debt restructuring.

**Social Initiatives:** The government has launched programs aimed at socio-economic transformation, such as the 'Clean Sri Lanka' initiative, which focuses
on political, social, and economic reforms to foster long-term development.

In summary, Sri Lanka in 2025 is navigating a path toward economic recovery and social reform, addressing persistent challenges while leveraging international
partnerships and domestic initiatives to build a more resilient future.
""")



# Footer
st.markdown("""
---
This dashboard provides a comparative study of significant incidents in Sri Lanka and Germany.
""")


