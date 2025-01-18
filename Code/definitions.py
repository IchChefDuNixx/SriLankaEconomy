import os
import streamlit as st


# main heading, intro
def add_heading_and_intro() -> None:
    """
    Adds a heading and an introduction to the Streamlit app.
    """
    # Center-aligned title
    st.markdown(
        """
        <h1 style='text-align: center; color: #FF7043;'>
            Sri Lanka's Journey:<br>A comparative Study with Germany
        </h1><br>
        """,
        unsafe_allow_html=True
    )

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
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

    # Adding 2 images
    with col2:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        st.image(
            os.path.join(base_dir, "../data/pictures/srilanka_ella.jpg"),
            caption="Scenic Ella train ride in Sri Lanka",
            use_column_width=True
        )

        st.image(
            os.path.join(base_dir, "../data/pictures/srilanka_surf.jpg"),
            caption="Surfing in Sri Lanka",
            use_column_width=True
        )


def add_summary() -> None:
    st.header("Summary")
    st.write("TODO: PUT OUTLOOK HERE")
