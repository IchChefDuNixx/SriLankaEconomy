from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="HIIII THIS IS THE BROWSER TAB NAME",
    page_icon="🇱🇰",
    layout='centered', # or wide
    initial_sidebar_state="expanded")


st.page_link(
    page=f"vis.py{'#'+sl_events[selected_year]["Event"] if False else ""}", # TODO: unfinished!
    label=f"**BACK**")


# Title of the page
st.title("Detailed Analysis of Sri Lanka's History and Current Situation")

# Define sections with their respective content
sections = [
    {
        "header": "Status quo in Sri Lanka",
        "text": """
            Here you can describe the current political, economic, and social situation in Sri Lanka.
            Use this space to provide a brief overview of the current state of affairs in the country.
        """,
        "image_path": "path/to/image1.jpg",
        "image_caption": "Caption for image 1",
        "id": "status-quo-in-sri-lanka"
    },
    {
        "header": "Tsunami",
        "text": """
            Discuss the 2004 Indian Ocean tsunami and its impact on Sri Lanka, including loss of life,
            property damage, and the recovery efforts.
        """,
        "image_path": "path/to/image2.jpg",
        "image_caption": "Caption for image 2",
        "id": "tsunami"
    },
    {
        "header": "Civil War Ended",
        "text": """
            Provide details about the end of the Sri Lankan Civil War in 2009. Discuss the key figures
            involved, the peace process, and the aftermath.
        """,
        "image_path": "path/to/image3.jpg",
        "image_caption": "Caption for image 3",
        "id": "civil-war-ended"
    },
    {
        "header": "Tourism boom",
        "text": """
            Describe the rise of tourism in Sri Lanka, including key factors that contributed to its growth,
            popular destinations, and economic impact.
        """,
        "image_path": "path/to/image4.jpg",
        "image_caption": "Caption for image 4",
        "id": "tourism-boom"
    },
    {
        "header": "Terrorist attacks (Easter Attacks)",
        "text": """
            Detail the Easter Sunday attacks in 2019, their impact on the country, and the response from
            the government and international community.
        """,
        "image_path": "path/to/image5.jpg",
        "image_caption": "Caption for image 5",
        "id": "terrorist-attacks"
    },
    {
        "header": "COVID-19 Pandemic",
        "text": """
            Explain how the COVID-19 pandemic affected Sri Lanka, including measures taken to control the
            spread of the virus, the impact on the economy, and the response from the government.
        """,
        "image_path": "path/to/image6.jpg",
        "image_caption": "Caption for image 6",
        "id": "covid-19"
    },
    {
        "header": "Economic Crisis",
        "text": """
            Discuss the current economic crisis in Sri Lanka, including factors that led to it, its impact
            on various sectors, and efforts to mitigate the crisis.
        """,
        "image_path": "path/to/image7.jpg",
        "image_caption": "Caption for image 7",
        "id": "economic-crisis"
    },
    {
        "header": "Protests against the government",
        "text": """
            Describe the public protests in Sri Lanka, the reasons behind them, and the government's response.
        """,
        "image_path": "path/to/image8.jpg",
        "image_caption": "Caption for image 8",
        "id": "protests-against-the-government"
    },
    {
        "header": "Today",
        "text": """
            Provide an overview of the current situation in Sri Lanka, summarizing the events and trends
            discussed in previous sections and looking ahead to the future.
        """,
        "image_path": "path/to/image9.jpg",
        "image_caption": "Caption for image 9",
        "id": "today"
    }
]

# Create each section using columns and add unique IDs
for section in sections:
    st.markdown(f'<a id="{section["id"]}"></a>', unsafe_allow_html=True)
    st.header(section["header"])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(section["text"])
    # with col2:
    #     image = Image.open(section["image_path"])
    #     st.image(image, caption=section["image_caption"], use_column_width=True)