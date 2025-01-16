import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image


st.set_page_config(
    page_title="HIIII THIS IS THE BROWSER TAB NAME",
    page_icon="🇱🇰",
    layout='centered', # or wide
    initial_sidebar_state="expanded")

for i in range(10):
    st.sidebar.write(f"[a](#a)")


# Displaying brief information about the 2004 tsunami
st.title("Incidents in Sri Lanka and Germany")
st.header("Tsunami 2004 in Sri Lanka")

info = """The 2004 Indian Ocean tsunami was one of the deadliest natural disasters in history.
It occurred on December 26, 2004, triggered by a 9.1-9.3 magnitude undersea earthquake.
Sri Lanka was among the worst-affected countries, with significant loss of life,
destruction of infrastructure, and economic devastation."""
st.markdown(info)

# Displaying the map image
st.header("Map of Sri Lanka with Affected Districts")
map_path = "pages/sri_lanka_districts.png"
try:
    img = Image.open(map_path)
    st.image(img, caption="Sri Lanka District Map", use_column_width=True)
except FileNotFoundError:
    st.warning(f"Map image not found at {map_path}. Please upload the map file.")

# Affected districts data
data = {
    "District": ["Ampara", "Batticaloa", "Galle", "Matara", "Hambantota", "Jaffna", "Trincomalee", "Kalutara"],
    "Latitude": [7.25, 7.71, 6.03, 5.95, 6.14, 9.66, 8.58, 6.58],
    "Longitude": [81.85, 81.68, 80.22, 80.54, 81.12, 80.02, 81.23, 79.96],
    "Time": ["9:20 AM", "9:30 AM", "9:15 AM", "9:25 AM", "9:30 AM", "9:45 AM", "9:20 AM", "9:10 AM"],
    "Deaths": [10625, 2840, 4000, 1700, 5000, 2800, 970, 265],
    "Damage": ["$500M", "$300M", "$200M", "$150M", "$250M", "$100M", "$80M", "$60M"]
}
df = pd.DataFrame(data)

# Create Plotly figure
fig = go.Figure()

# Add the background map
fig.add_layout_image(
    dict(
        source=map_path,
        xref="x", yref="y",
        x=79.5, y=10.0,
        sizex=3, sizey=3,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for affected districts
for _, row in df.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"{row['District']}<br>Time: {row['Time']}<br>Deaths: {row['Deaths']}<br>Damage: {row['Damage']}",
        marker=dict(size=10, color="red"),
        name=row["District"]
    ))

# Update layout for the map
fig.update_layout(
    title="Sri Lanka Tsunami 2004 Affected Districts",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[5.8, 10.0]),
        lonaxis=dict(range=[79.5, 82.0]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the map
st.plotly_chart(fig)

# Information about the Sri Lankan Civil War (2000-2009)
st.header("Sri Lankan Civil War (2000-2009)")

civil_war_info = """The Sri Lankan Civil War was a prolonged armed conflict between the government of Sri Lanka
and the Liberation Tigers of Tamil Eelam (LTTE). The war intensified during the early 2000s,
culminating in the defeat of the LTTE in May 2009. The conflict caused widespread destruction
and loss of life, particularly in the Northern and Eastern provinces."""
st.markdown(civil_war_info)

# Expanded Civil War events data
events_data = {
    "Year": [
        2000, 2000, 2000, 2001, 2001, 2001, 2002, 2002, 2002,
        2003, 2003, 2003, 2004, 2004, 2004, 2005, 2005, 2005,
        2006, 2006, 2006, 2007, 2007, 2007, 2008, 2008, 2008, 2009, 2009, 2009
    ],
    "Event": [
        "Elephant Pass falls to LTTE", "Battle of Jaffna", "Attack on Mullaitivu",
        "Katunayake airport attack", "Battle of Muttur", "LTTE seizes Elephant Pass",
        "Ceasefire agreement signed", "LTTE political assassinations", "Attack on Batticaloa",
        "LTTE naval attack", "Battle of Trincomalee", "LTTE ambush in Vavuniya",
        "Eastern Province bombings", "LTTE assassination attempt", "Kandy unrest",
        "LTTE offensive in Mannar", "Battle of Sampur", "Colombo bombing",
        "Mavil Aru conflict begins", "Trincomalee attacks", "Liberation of Sampur",
        "Battle of Thoppigala", "Operation Silavathurai", "Battle of Mannar",
        "LTTE air raids", "Battle of Kilinochchi", "Northern offensive begins",
        "End of the Civil War - LTTE defeated", "Battle of Mullivaikkal", "Operation Wadamarachchi"
    ],
    "Latitude": [
        9.5, 9.65, 9.28, 7.17, 8.57, 9.5, 8.57, 8.4, 7.72,
        9.12, 8.57, 8.75, 7.98, 7.34, 7.3, 9.26, 8.56, 6.93,
        7.85, 8.58, 8.56, 7.95, 7.56, 9.2, 9.2, 9.22, 9.18, 8.35, 9.25, 9.37
    ],
    "Longitude": [
        80.3, 80.03, 80.72, 79.87, 81.55, 80.3, 80.65, 80.48, 81.68,
        80.5, 81.24, 80.45, 81.32, 80.65, 80.56, 80.7, 81.26, 79.84,
        81.55, 81.23, 81.26, 81.6, 80.23, 80.4, 80.8, 80.84, 80.81, 81.23, 80.9, 81.12
    ]
}
events_df = pd.DataFrame(events_data)

# Add a slider for selecting the year
selected_year = st.slider("Select a year to view major events", 2000, 2009, 2000)
filtered_events = events_df[events_df["Year"] == selected_year]

# Create a map for Civil War events
war_fig = go.Figure()

# Add the background map
war_fig.add_layout_image(
    dict(
        source=map_path,
        xref="x", yref="y",
        x=79.5, y=10.0,
        sizex=3, sizey=3,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for the selected year's events
for _, row in filtered_events.iterrows():
    war_fig.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"Event: {row['Event']}",
        marker=dict(size=12, color="blue"),
        name=row["Event"]
    ))

# Update layout for the Civil War map
war_fig.update_layout(
    title=f"Sri Lankan Civil War Events in {selected_year}",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[5.8, 10.0]),
        lonaxis=dict(range=[79.5, 82.0]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the Civil War map
st.plotly_chart(war_fig)



# Information about the 2008/09 Financial Crisis in Germany
st.header("2008/09 Financial Crisis in Germany")

financial_crisis_info = """The 2008/09 financial crisis had a significant impact on Germany, Europe's largest economy.\n" \
                       "The crisis led to a contraction in industrial output, increased unemployment, and a significant\n" \
                       "rise in government spending to stabilize the economy. German states experienced varied levels of\n" \
                       "economic strain, with some regions being hit harder than others."""
st.markdown(financial_crisis_info)

# Define data for German states during the financial crisis
data_germany = {
    "State": [
        "Bavaria", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse", "Lower Saxony",
        "Hamburg", "Bremen", "Berlin", "Saxony", "Thuringia", "Saxony-Anhalt", "Brandenburg",
        "Mecklenburg-Western Pomerania", "Rhineland-Palatinate", "Saarland", "Schleswig-Holstein"
    ],
    "Latitude": [
        48.7904, 48.6616, 51.4332, 50.5673, 52.6367, 53.5511, 53.0793, 52.5200, 51.1045,
        50.9848, 51.9503, 52.4084, 53.6127, 49.9929, 49.3964, 54.2194
    ],
    "Longitude": [
        11.4979, 9.3501, 7.6616, 9.6847, 10.1411, 9.9937, 8.8017, 13.4050, 13.2016,
        11.0249, 11.7005, 12.5218, 12.4296, 8.2310, 6.9634, 9.6961
    ],
    "2008": {
        "Unemployment Rate": [4.2, 3.6, 7.5, 5.2, 6.1, 4.8, 9.0, 13.0, 10.5, 8.5, 10.0, 11.3, 14.1, 6.5, 7.9, 6.7],
        "Industrial Output Change": [-3.0, -2.8, -3.5, -3.2, -3.1, -3.0, -2.9, -4.0, -3.7, -3.6, -3.8, -3.9, -4.1, -2.7, -2.8, -3.0],
        "GDP Growth Rate": [1.0, 1.2, 0.8, 1.1, 0.9, 1.0, 0.7, 0.5, 0.6, 0.6, 0.5, 0.4, 0.3, 1.1, 1.0, 1.0]
    },
    "2009": {
        "Unemployment Rate": [5.1, 4.5, 8.2, 6.0, 7.1, 5.7, 10.2, 14.5, 12.0, 9.7, 11.5, 12.8, 16.0, 7.6, 8.8, 7.8],
        "Industrial Output Change": [-10.0, -9.5, -11.0, -10.5, -10.2, -9.8, -10.0, -12.0, -11.7, -11.4, -11.9, -12.3, -12.8, -9.7, -9.8, -10.2],
        "GDP Growth Rate": [-5.7, -5.5, -5.9, -5.6, -5.8, -5.7, -5.9, -6.0, -5.9, -5.8, -6.1, -6.2, -6.3, -5.4, -5.5, -5.7]
    }
}

# Convert data to DataFrame
states_df = pd.DataFrame({
    "State": data_germany["State"],
    "Latitude": data_germany["Latitude"],
    "Longitude": data_germany["Longitude"]
})

# Add a slider for selecting the year
selected_year = st.slider("Select a year to view data", 2008, 2009, 2008)
selected_data = data_germany[str(selected_year)]

# Generate unique colors for each state
state_colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94"
]

# Create map for German states
germany_fig = go.Figure()

# Add the background map
germany_map_path = "Germany-States-Map.avif"
germany_fig.add_layout_image(
    dict(
        source=germany_map_path,
        xref="x", yref="y",
        x=5.5, y=55.0,
        sizex=10, sizey=10,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for each state
for i, row in states_df.iterrows():
    germany_fig.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"State: {row['State']}<br>Unemployment Rate: {selected_data['Unemployment Rate'][i]}%<br>"
             f"Industrial Output Change: {selected_data['Industrial Output Change'][i]}%<br>"
             f"GDP Growth Rate: {selected_data['GDP Growth Rate'][i]}%",
        marker=dict(size=12, color=state_colors[i]),
        name=row["State"]
    ))

# Update layout for the map
germany_fig.update_layout(
    title=f"German States Data During {selected_year} Financial Crisis",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[47.0, 55.0]),
        lonaxis=dict(range=[5.5, 15.5]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the map
st.plotly_chart(germany_fig)



# Information about the 2015 Refugee Crisis in Germany
st.header("2015 Refugee Crisis in Germany")

refugee_crisis_info = """The 2015 refugee crisis was a significant event in Germany's recent history.\n" \
                      "Germany became a primary destination for refugees fleeing conflict, primarily from Syria, Afghanistan,\n" \
                      "and Iraq. The country welcomed over one million asylum seekers, placing a significant\n" \
                      "strain on resources and infrastructure, but also showcasing Germany's humanitarian commitment."""
st.markdown(refugee_crisis_info)

# Define data for German states during the refugee crisis
data_refugees = {
    "State": [
        "Bavaria", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse", "Lower Saxony",
        "Hamburg", "Bremen", "Berlin", "Saxony", "Thuringia", "Saxony-Anhalt", "Brandenburg",
        "Mecklenburg-Western Pomerania", "Rhineland-Palatinate", "Saarland", "Schleswig-Holstein"
    ],
    "Latitude": [
        48.7904, 48.6616, 51.4332, 50.5673, 52.6367, 53.5511, 53.0793, 52.5200, 51.1045,
        50.9848, 51.9503, 52.4084, 53.6127, 49.9929, 49.3964, 54.2194
    ],
    "Longitude": [
        11.4979, 9.3501, 7.6616, 9.6847, 10.1411, 9.9937, 8.8017, 13.4050, 13.2016,
        11.0249, 11.7005, 12.5218, 12.4296, 8.2310, 6.9634, 9.6961
    ],
    "Refugees Accepted": [
        150000, 120000, 300000, 100000, 90000, 80000, 50000, 70000, 60000,
        45000, 50000, 55000, 40000, 75000, 35000, 65000
    ],
    "Cost (Million Euros)": [
        4500, 3600, 9000, 3000, 2700, 2400, 1500, 2100, 1800,
        1350, 1500, 1650, 1200, 2250, 1050, 1950
    ]
}

# Convert data to DataFrame
refugees_df = pd.DataFrame({
    "State": data_refugees["State"],
    "Latitude": data_refugees["Latitude"],
    "Longitude": data_refugees["Longitude"],
    "Refugees Accepted": data_refugees["Refugees Accepted"],
    "Cost (Million Euros)": data_refugees["Cost (Million Euros)"]
})

# Generate unique colors for each state
state_colors_refugees = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94"
]

# Create map for German states
germany_fig_refugees = go.Figure()

# Add the background map
germany_map_path = "Germany-States-Map.avif"
germany_fig_refugees.add_layout_image(
    dict(
        source=germany_map_path,
        xref="x", yref="y",
        x=5.5, y=55.0,
        sizex=10, sizey=10,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for each state
for i, row in refugees_df.iterrows():
    germany_fig_refugees.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"State: {row['State']}<br>Refugees Accepted: {row['Refugees Accepted']}<br>"
             f"Cost: €{row['Cost (Million Euros)']}M",
        marker=dict(size=12, color=state_colors_refugees[i]),
        name=row["State"]
    ))

# Update layout for the map
germany_fig_refugees.update_layout(
    title="German States Data During 2015 Refugee Crisis",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[47.0, 55.0]),
        lonaxis=dict(range=[5.5, 15.5]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the map
st.plotly_chart(germany_fig_refugees)




# Information about the 2019 Easter Attacks in Sri Lanka
st.header("2019 Easter Attacks in Sri Lanka")

easter_attacks_info = """The 2019 Easter attacks in Sri Lanka were a series of coordinated bombings\n" \
                       "targeting churches and luxury hotels on Easter Sunday, April 21, 2019.\n" \
                       "These attacks, carried out by Islamist extremists, resulted in the deaths of\n" \
                       "over 250 people and injuries to hundreds more, making it one of the deadliest\n" \
                       "terrorist attacks in Sri Lanka's history."""
st.markdown(easter_attacks_info)

# Define data for locations targeted during the Easter attacks
data_easter_attacks = {
    "Location": [
        "St. Anthony's Shrine", "St. Sebastian's Church", "Zion Church", "Shangri-La Hotel", "Cinnamon Grand Hotel", "Kingsbury Hotel"
    ],
    "Latitude": [7.2906, 7.1838, 8.5648, 6.9275, 6.9319, 6.9320],
    "Longitude": [79.8730, 79.9200, 81.2250, 79.8484, 79.8507, 79.8481],
    "Killed": [93, 115, 31, 45, 20, 18],
    "Injured": [150, 200, 70, 150, 80, 60],
    "Terrorists Killed": [2, 1, 0, 3, 0, 1]
}

# Convert data to DataFrame
easter_attacks_df = pd.DataFrame(data_easter_attacks)

# Generate unique colors for each location
location_colors = [
    "#ff5733", "#33ff57", "#3357ff", "#ff33a6", "#33fff3", "#a633ff"
]

# Create map for Easter attack locations
easter_fig = go.Figure()

# Add the background map
sri_lanka_map_path = "sri_lanka_districts.png"
easter_fig.add_layout_image(
    dict(
        source=sri_lanka_map_path,
        xref="x", yref="y",
        x=79.5, y=10.0,
        sizex=3, sizey=3,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for each location
for i, row in easter_attacks_df.iterrows():
    easter_fig.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"Location: {row['Location']}<br>Killed: {row['Killed']}<br>"
             f"Injured: {row['Injured']}<br>Terrorists Killed: {row['Terrorists Killed']}",
        marker=dict(size=12, color=location_colors[i]),
        name=row["Location"]
    ))

# Update layout for the map
easter_fig.update_layout(
    title="Locations Targeted During 2019 Easter Attacks in Sri Lanka",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[5.8, 10.0]),
        lonaxis=dict(range=[79.5, 82.0]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the map
st.plotly_chart(easter_fig)



# Information about the COVID-19 Pandemic in Germany
st.header("COVID-19 Pandemic in Germany")

covid_info = """The COVID-19 pandemic had a profound impact on Germany starting in early 2020.\n" \
            "The country faced waves of infections, significant fatalities, and widespread\n" \
            "economic challenges as lockdown measures were implemented to curb the virus's spread.\n" \
            "Vaccination campaigns and financial aid were critical in mitigating the crisis."""
st.markdown(covid_info)

# Define data for German states during the COVID-19 pandemic
data_covid = {
    "State": [
        "Bavaria", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse", "Lower Saxony",
        "Hamburg", "Bremen", "Berlin", "Saxony", "Thuringia", "Saxony-Anhalt", "Brandenburg",
        "Mecklenburg-Western Pomerania", "Rhineland-Palatinate", "Saarland", "Schleswig-Holstein"
    ],
    "Latitude": [
        48.7904, 48.6616, 51.4332, 50.5673, 52.6367, 53.5511, 53.0793, 52.5200, 51.1045,
        50.9848, 51.9503, 52.4084, 53.6127, 49.9929, 49.3964, 54.2194
    ],
    "Longitude": [
        11.4979, 9.3501, 7.6616, 9.6847, 10.1411, 9.9937, 8.8017, 13.4050, 13.2016,
        11.0249, 11.7005, 12.5218, 12.4296, 8.2310, 6.9634, 9.6961
    ],
    "2020": {
        "Sick": [300000, 250000, 400000, 200000, 150000, 80000, 50000, 120000, 90000,
                 70000, 60000, 80000, 40000, 100000, 50000, 70000],
        "Died": [8000, 6000, 10000, 5000, 3000, 2000, 1500, 3000, 2500,
                 2000, 1800, 2500, 1000, 3000, 1500, 2000],
        "Financial Loss (Million Euros)": [20000, 15000, 30000, 10000, 8000, 5000, 3000, 7000, 5000,
                                           4000, 3500, 4500, 2000, 8000, 3000, 5000]
    },
    "2021": {
        "Sick": [600000, 500000, 800000, 400000, 300000, 150000, 100000, 240000, 180000,
                 140000, 120000, 160000, 80000, 200000, 100000, 140000],
        "Died": [16000, 12000, 20000, 10000, 6000, 4000, 3000, 6000, 5000,
                 4000, 3600, 5000, 2000, 6000, 3000, 4000],
        "Financial Loss (Million Euros)": [40000, 30000, 60000, 20000, 16000, 10000, 6000, 14000, 10000,
                                           8000, 7000, 9000, 4000, 16000, 6000, 10000]
    }
}

# Convert data to DataFrame
states_covid_df = pd.DataFrame({
    "State": data_covid["State"],
    "Latitude": data_covid["Latitude"],
    "Longitude": data_covid["Longitude"]
})

# Add a slider for selecting the year
selected_year = st.slider("Select a year to view data", 2020, 2021, 2020)
selected_covid_data = data_covid[str(selected_year)]

# Generate unique colors for each state
state_colors_covid = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94"
]

# Create map for COVID-19 data in German states
covid_fig = go.Figure()

# Add the background map
germany_map_path = "Germany-States-Map.avif"
covid_fig.add_layout_image(
    dict(
        source=germany_map_path,
        xref="x", yref="y",
        x=5.5, y=55.0,
        sizex=10, sizey=10,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for each state
for i, row in states_covid_df.iterrows():
    covid_fig.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"State: {row['State']}<br>Sick: {selected_covid_data['Sick'][i]}<br>"
             f"Died: {selected_covid_data['Died'][i]}<br>Financial Loss: €{selected_covid_data['Financial Loss (Million Euros)']}M",
        marker=dict(size=12, color=state_colors_covid[i]),
        name=row["State"]
    ))

# Update layout for the map
covid_fig.update_layout(
    title=f"German States Data During COVID-19 Pandemic ({selected_year})",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[47.0, 55.0]),
        lonaxis=dict(range=[5.5, 15.5]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the map
st.plotly_chart(covid_fig)






# Information about the COVID-19 Pandemic in Sri Lanka
st.header("COVID-19 Pandemic in Sri Lanka")

covid_info_sri_lanka = """The COVID-19 pandemic impacted Sri Lanka significantly starting in early 2020.\n" \
                      "The country experienced multiple waves of infections, with extensive challenges\n" \
                      "in managing healthcare resources, enforcing lockdowns, and ensuring economic stability.\n" \
                      "Vaccination campaigns were a key measure to combat the spread of the virus."""
st.markdown(covid_info_sri_lanka)

# Define data for Sri Lankan districts during the COVID-19 pandemic
data_covid_sri_lanka = {
    "District": [
        "Colombo", "Gampaha", "Kandy", "Galle", "Jaffna", "Kurunegala", "Ratnapura", "Anuradhapura",
        "Batticaloa", "Trincomalee", "Hambantota", "Matara", "Badulla", "Nuwara Eliya", "Polonnaruwa", "Ampara"
    ],
    "Latitude": [
        6.9271, 7.0916, 7.2906, 6.0392, 9.6615, 7.4863, 6.6828, 8.3122,
        7.7102, 8.5874, 6.1246, 5.9549, 6.9894, 6.9497, 7.9403, 7.3024
    ],
    "Longitude": [
        79.8612, 79.9945, 80.6337, 80.2169, 80.0088, 80.3626, 80.3999, 80.4037,
        81.6748, 81.2332, 81.1241, 80.5480, 81.0566, 80.7689, 81.0011, 81.6743
    ],
    "2020": {
        "Sick": [50000, 45000, 30000, 25000, 15000, 20000, 18000, 12000, 11000, 10000, 8000, 8500, 9000, 7500, 7000, 6800],
        "Died": [1500, 1200, 800, 700, 500, 600, 550, 400, 350, 300, 250, 260, 300, 240, 230, 220],
        "Financial Loss (Million LKR)": [100000, 90000, 60000, 50000, 30000, 40000, 35000, 25000,
                                         20000, 18000, 15000, 16000, 17000, 14000, 13000, 12500]
    },
    "2021": {
        "Sick": [100000, 90000, 60000, 50000, 30000, 40000, 36000, 24000, 22000, 20000, 16000, 17000, 18000, 15000, 14000, 13600],
        "Died": [3000, 2400, 1600, 1400, 1000, 1200, 1100, 800, 700, 600, 500, 520, 600, 480, 460, 440],
        "Financial Loss (Million LKR)": [200000, 180000, 120000, 100000, 60000, 80000, 70000, 50000,
                                         40000, 36000, 30000, 32000, 34000, 28000, 26000, 25000]
    }
}

# Convert data to DataFrame
districts_covid_df = pd.DataFrame({
    "District": data_covid_sri_lanka["District"],
    "Latitude": data_covid_sri_lanka["Latitude"],
    "Longitude": data_covid_sri_lanka["Longitude"]
})

# Add a slider for selecting the year
selected_year_sri_lanka = st.slider("Select a year to view data (Sri Lanka)", 2020, 2021, 2020, key="sri_lanka_covid_year")
selected_covid_data_sri_lanka = data_covid_sri_lanka[str(selected_year_sri_lanka)]

# Generate unique colors for each district
district_colors_covid = [
    "#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6", "#c2f0c2", "#ff6666",
    "#9999ff", "#ff99cc", "#b3e6ff", "#99ccff", "#ffccff", "#e6e6e6", "#cccccc", "#ccffcc"
]

# Create map for COVID-19 data in Sri Lankan districts
covid_fig_sri_lanka = go.Figure()

# Add the background map
sri_lanka_map_path = "sri_lanka_districts.png"
covid_fig_sri_lanka.add_layout_image(
    dict(
        source=sri_lanka_map_path,
        xref="x", yref="y",
        x=79.5, y=10.0,
        sizex=3, sizey=3,
        xanchor="left", yanchor="top",
        layer="below"
    )
)

# Add markers for each district
for i, row in districts_covid_df.iterrows():
    covid_fig_sri_lanka.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"District: {row['District']}<br>Sick: {selected_covid_data_sri_lanka['Sick'][i]}<br>"
             f"Died: {selected_covid_data_sri_lanka['Died'][i]}<br>Financial Loss: LKR {selected_covid_data_sri_lanka['Financial Loss (Million LKR)']}M",
        marker=dict(size=12, color=district_colors_covid[i]),
        name=row["District"]
    ))

# Update layout for the map
covid_fig_sri_lanka.update_layout(
    title=f"Sri Lankan Districts Data During COVID-19 Pandemic ({selected_year_sri_lanka})",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[5.8, 10.0]),
        lonaxis=dict(range=[79.5, 82.0]),
        visible=False  # Removes axes
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=800,  # Enlarges the map
    width=1000
)

# Display the map
st.plotly_chart(covid_fig_sri_lanka)


# Information about the Economic Crisis in Sri Lanka
st.header("Economic Crisis in Sri Lanka")

Economic_info = """Crisis Origin — The Sri Lankan economic crisis began in 2019 and is considered the worst since the country's independence in 1948. It was triggered by a combination of tax cuts, money creation, and policy shifts, alongside external shocks like the COVID-19 pandemic.

Debt Default — In April 2022, Sri Lanka defaulted on its external debt, marking its first sovereign default since independence. This was due to unsustainable public debt and a lack of foreign reserves.

Inflation and Shortages — The crisis led to unprecedented inflation rates and severe shortages of essential goods, including fuel and medicine, causing widespread public protests.

International Assistance — Sri Lanka received a $3 billion loan from the International Monetary Fund (IMF) to help stabilize its economy. Additionally, India provided a $4 billion line of credit to assist with essential imports.


Economic Reforms — The government has implemented austerity measures and fiscal reforms as part of the IMF agreement, aiming to stabilize the economy and reduce fiscal deficits.."""
st.markdown(Economic_info)