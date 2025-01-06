import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
import pandas as pd



# Define the data for the timeline
events = [
    {"Year": 2000, "Event": "Whats happening in Sri Lanka in 2000", "Description": "intro on how the country was."},
    {"Year": 2004, "Event": "Tsunami", "Description": "Tsunami hit the island on 26th December 2004. 30000 people lost there lives and thousands were displaced. Infrastructure destroyed and fishing communities were wiped out. "},
    {"Year": 2009, "Event": "Civil War Ended", "Description": "Sri Lanka suffered from civil war from 1983 till 2009. 18th may 2009 Sri Lanka declared victory, defeating the Liberation Tigers of Tamil Eelam(LTTE). "},
    {"Year": 2018, "Event": "Tourism blooming", "Description": "Tourism at peak. Factors such as end of war had an effect on this. "},
    {"Year": 2019, "Event": "Terrorist attack (Easter Attack)", "Description": "Jihadist suicide bombers attack churches and luxury hotels on Easter Sunday (21st April 2019). More than 350 people were killed and hundreds were wounded. "},
    {"Year": 2020, "Event": "COVID-19 Pandemic", "Description": "Lockdown was imposed for months in multiple occasions. Tourism came to a halt. Unemployment increased from 4.8% in 2019 to 5.5% in 2020. "},
    {"Year": 2022, "Event": "Protests against the governance", "Description": "Protests lasts from 15th March 2022 to 14th November 2022. Main two reasons for the protests were High inflation and rapid rise in the cost of living, Authoritarianism, corruption and nepotism of the Rajapaksa family. "},
    {"Year": 2024, "Event": "Current situation", "Description": "how is Sri Lanka doing."}
]

# Convert to DataFrame
#data = pd.DataFrame(events)
df = pd.DataFrame(events)

year_options = [2000, 2004, 2009, 2018, 2019, 2020, 2022, 2024]

selected_year = st.select_slider(
    "Select Year Range",
    options=year_options,
    value=2000,
    format_func=lambda x: str(int(x))
)

# Filter event data based on selected year
event_details = df[df["Year"] == selected_year].iloc[0]
event_name = event_details["Event"]
event_description = event_details["Description"]

# Display the selected event details
st.write(f"**Year:** {selected_year}")
st.write(f"**Event:** {event_name}")
st.write(f"**Description:** {event_description}")
