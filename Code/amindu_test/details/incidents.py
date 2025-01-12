import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import matplotlib.pyplot as plt


# Displaying brief information about the 2004 tsunami
st.title("Incidents in Sri Lanka and Germany")
st.header("Tsunami 2004 in Sri Lanka")

info = """The 2004 Indian Ocean tsunami was one of the deadliest natural disasters in history.
It occurred on December 26, 2004, triggered by a 9.1-9.3 magnitude undersea earthquake.
Sri Lanka was among the worst-affected countries, with significant loss of life,
destruction of infrastructure, and economic devastation."""
st.markdown(info)

# Displaying images related to the tsunami
st.header("Images from the 2004 Tsunami")
image_paths = ["tsunami1.jpg", "tsunami2.jpg"]  # Image filenames in the same directory
for img_path in image_paths:
    try:
        img = Image.open(img_path)
        st.image(img, use_column_width=True, caption=img_path)
    except FileNotFoundError:
        st.warning(f"Image {img_path} not found. Please ensure the image is in the same directory.")

# Displaying the map image
st.header("Map of Sri Lanka with Affected Districts")
map_path = "sri_lanka_districts.png"  # Replace with the path to your uploaded map image
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
        xref="x",
        yref="y",
        x=79.5,  # Adjust these coordinates to align with the map
        y=10.0,
        sizex=3,
        sizey=3,
        xanchor="left",
        yanchor="top",
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
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
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

# Displaying images related to the civilwar
st.header("Images from the 2009 civil war")
image_paths = ["tsunami1.jpg", "tsunami2.jpg"]  # Image filenames in the same directory
for img_path in image_paths:
    try:
        img = Image.open(img_path)
        st.image(img, use_column_width=True, caption=img_path)
    except FileNotFoundError:
        st.warning(f"Image {img_path} not found. Please ensure the image is in the same directory.")

st.header("Map of Sri Lanka with Major Battles In Civil War")

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
    ],
    "SL_Army_Deaths": [
        500, 200, 300, 200, 400, 150, 0, 50, 100,
        100, 150, 200, 250, 300, 200, 300, 400, 250,
        150, 250, 300, 250, 200, 500, 300, 400, 500, 600, 450, 300
    ],
    "LTTE_Deaths": [
        300, 100, 200, 50, 300, 200, 0, 100, 150,
        200, 300, 250, 400, 500, 350, 600, 800, 500,
        400, 500, 600, 500, 300, 700, 800, 1000, 1100, 1800, 1300, 900
    ],
    "Details": [
        "Strategic base falls to LTTE forces.", "Major battle for Jaffna control.", "LTTE attacks military outpost.",
        "Suicide attack damages 13 aircraft at Katunayake airport.", "Fierce battle in Muttur.", "LTTE regains control of Elephant Pass.",
        "Temporary peace established through Norwegian mediation.", "Political leaders targeted by LTTE.", "Attack on Batticaloa base.",
        "LTTE launches surprise naval attack.", "Major battle in Trincomalee region.", "Ambush in Vavuniya region.",
        "Series of bombings in the Eastern Province.", "Attempted assassination by LTTE.", "Unrest erupts in Kandy.",
        "Offensive operation in Mannar district.", "Sampur falls to Sri Lankan forces.", "Colombo targeted by bombers.",
        "LTTE closes the sluice gates of Mavil Aru, sparking conflict.", "LTTE attacks Trincomalee.", "Sampur liberated by Sri Lankan forces.",
        "Eastern stronghold of LTTE falls.", "Operation to secure Silavathurai begins.", "Battle for Mannar region intensifies.",
        "LTTE conducts air raids on Colombo.", "Sri Lankan forces capture Kilinochchi.", "Major offensive in northern regions.",
        "Sri Lankan Army defeats the LTTE, ending the war.", "Final battle at Mullivaikkal.", "Operation to secure Wadamarachchi region."
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
        xref="x",
        yref="y",
        x=79.5,
        y=10.0,
        sizex=3,
        sizey=3,
        xanchor="left",
        yanchor="top",
        layer="below"
    )
)

# Add markers for the selected year's events
for _, row in filtered_events.iterrows():
    war_fig.add_trace(go.Scattergeo(
        lon=[row["Longitude"]],
        lat=[row["Latitude"]],
        text=f"Year: {row['Year']}<br>Event: {row['Event']}<br>SL Army Deaths: {row['SL_Army_Deaths']}<br>LTTE Deaths: {row['LTTE_Deaths']}<br>Details: {row['Details']}",
        marker=dict(size=12, color="blue"),
        name=row["Event"]
    ))

# Update layout for the war map
war_fig.update_layout(
    title=f"Sri Lankan Civil War Major Events in {selected_year}",
    geo=dict(
        showland=True,
        showcountries=True,
        projection_type="mercator",
        resolution=50,
        lataxis=dict(range=[5.8, 10.0]),
        lonaxis=dict(range=[79.5, 82.0]),
    ),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)

# Display the war map
st.plotly_chart(war_fig)



# 2008/09 Financial Crisis in Germany
st.header("2008/09 Financial Crisis in Germany")

financial_crisis_info = """The 2008/09 financial crisis had a significant impact on Germany, Europe's largest economy.
The crisis led to a contraction in industrial output, increased unemployment, and a significant
rise in government spending to stabilize the economy. German states experienced varied levels of
financial losses, with some regions being hit harder due to their reliance on specific industries."""
st.markdown(financial_crisis_info)

# Social and economic changes during the financial crisis
data_social_economic = {
    "Year": [2007, 2008, 2009, 2010],
    "Unemployment Rate (%)": [8.1, 7.5, 8.2, 7.1],
    "GDP Growth Rate (%)": [3.3, 1.0, -5.7, 4.0],
    "Industrial Output Change (%)": [4.5, -3.2, -20.0, 10.1]
}
df_social_economic = pd.DataFrame(data_social_economic)

# Line plot for social and economic changes
st.subheader("Social and Economic Changes During the Crisis")
fig_social = plt.figure()
plt.plot(df_social_economic["Year"], df_social_economic["Unemployment Rate (%)"], label="Unemployment Rate (%)", marker="o")
plt.plot(df_social_economic["Year"], df_social_economic["GDP Growth Rate (%)"], label="GDP Growth Rate (%)", marker="o")
plt.plot(df_social_economic["Year"], df_social_economic["Industrial Output Change (%)"], label="Industrial Output Change (%)", marker="o")
plt.title("Social and Economic Changes (2007-2010)")
plt.xlabel("Year")
plt.ylabel("Percentage Change")
plt.legend()
st.pyplot(fig_social)

# Financial losses by state
st.subheader("Financial Losses by German States")

states = ["Bavaria", "North Rhine-Westphalia", "Baden-Württemberg", "Hesse", "Lower Saxony"]
losses = [50, 70, 60, 40, 30]  # Example financial losses in billion euros

data_losses = {
    "State": states,
    "Loss (Billion Euros)": losses
}
df_losses = pd.DataFrame(data_losses)

# Generate image showing losses by state (similar to uploaded map)
fig_losses = plt.figure(figsize=(10, 6))
plt.bar(states, losses, color="orange")
plt.title("Financial Losses During the 2008/09 Crisis by State")
plt.xlabel("State")
plt.ylabel("Loss (Billion Euros)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig_losses)
