import streamlit as st


# main heading, intro
def add_heading_and_intro() -> None:
    """
    Adds a heading and an introduction to the Streamlit app.
    """
    # Title - left aligned by default
    # st.title("Sri Lanka's Journey: A comparative Study with Germany")

    # Center-aligned title
    st.markdown(
        """
        <h1 style='text-align: center'>
            Sri Lanka's Journey: A comparative Study with Germany
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Add a header
    st.header("Introduction")

    # Add introductory text
    st.write("""
    Sri Lanka, often referred to as the "Pearl of the Indian Ocean", is an island located in
    South Asia. It is renowed for its rich history, vibrant culture, and stunning natural
    beauty.

    Being a developing country, Sri Lanka is heavily reliant on agriculture, manufacturing and services.
    While the economy has shown resilience, it has also faced challenges, including fiscal deficits,
    debt burdens, and external shocks.

    Sri Lanka has experienced several pivotal events that have shaped its socio-economic landscape.
    These incidents have had implications on various aspects of the nation, including its
    inflation rates, Gross Domestic Product (GDP), tourism industry, and overall happiness of its citizens.
    """)


def add_outlook() -> None:
    st.header("Outlook")
    st.write("TODO: PUT OUTLOOK HERE")
