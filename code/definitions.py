import os
import pandas as pd
import streamlit as st


COLORS = {'good': '#34C759',
          'bad': '#FF3737',
          'neutral': '#808080',
          'inflation': '#FF7043',
          'GDP': '#4DB6AC',
          'happiness': '#81C784',
          'tourism': '#7986CB',
          'Germany': '#4DB6AC',
          'Germany1': '#4DB6AC', # same as Germany
          'Germany2': '#26A69A',
          'Germany3': '#80CBC4',
          'Sri Lanka': '#FF7043',
          'Sri Lanka1': '#FF7043', # same as Sri Lanka
          'Sri Lanka2': '#FF8767',
          'Sri Lanka3': '#FFA183',
          'Sri Lanka4': '#FFBBA7',
}


# main heading, intro
def add_heading_and_intro() -> None:
    """
    Adds a heading and an introduction to the Streamlit app.
    """
    # Center-aligned title
    st.markdown(
        f"""
        <h1 style='text-align: center; color: {COLORS["Sri Lanka"]};'>
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
        Sri Lanka, often referred to as the "Pearl of the Indian Ocean", is an island located in South Asia. It is renowned for its rich history, vibrant culture, and stunning natural beauty.

        Being a developing country, Sri Lanka is heavily reliant on agriculture, manufacturing, and services. While the economy has shown resilience, it has also faced challenges, including fiscal deficits, debt burdens, and external shocks.

        Sri Lanka has experienced several pivotal events that have shaped its socio-economic landscape. These incidents have had implications on various aspects of the nation, including its inflation rates, Gross Domestic Product (GDP), tourism industry, and overall happiness of its citizens.

        This application will compare Sri Lanka to Germany, highlighting the similarities and differences between them and providing insights into their respective economic and social landscapes.
        """, unsafe_allow_html=True)

    # Adding 2 images
    with col2:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        st.image(
            os.path.join(base_dir, "../data/pictures/srilanka_ella.jpg"),
            caption="Scenic Ella train ride in Sri Lanka",
            width="stretch"
        )

        st.image(
            os.path.join(base_dir, "../data/pictures/srilanka_surf.jpg"),
            caption="Surfing in Sri Lanka",
            width="stretch"
        )


def add_summary() -> None:
    heading_colour = COLORS['Sri Lanka']
    st.markdown(
        f"<h1 style='color:{heading_colour};'>Summary</h1>",
        unsafe_allow_html=True
    )

    summary_text = """
    Over the past 25 years, Sri Lanka has faced significant challenges, including the deadliest tsunami in human history. The country also suffered severely from the effects of coordinated terrorist attacks and the global COVID-19 pandemic. However, Sri Lanka has managed to end the civil war and experienced a period of continuous improvements from 2009 to 2018.
    <br>
    Germany encountered difficulties during the 2015 refugee crisis, which strained its social services and infrastructure. The outbreak of the Ukraine war lead to a significant rise in energy prices and economic uncertainty. The comparisons indicate that Germany maintains a more stable economy and a higher standard of living. Factors such as a stronger social safety net and higher average income contribute to the higher reported happiness.
    <br>
    Today, Sri Lanka is recovering from the pandemic, with tourism starting to pick up again and inflation remaining low. The government is implementing economic reforms and attracting foreign investment to stimulate growth and improve living standards.
    """

    # colorful country names
    for country in ["Sri Lanka", "Germany"]:
        summary_text = summary_text.replace(country, f'<font color="{COLORS[country]}">{country}</font>')

    st.markdown(summary_text, unsafe_allow_html=True)

    # a dataframe is very convenient for styling a table
    reasons_to_stay = pd.DataFrame({
        "Reasons to stay in Sri Lanka": [
            """
            <ul>
                <li>Rich culture and warm hospitality</li>
                <li>Beautiful, very distinct landscape</li>
                <li>Relatively low cost of living compared to Western countries</li>
            </ul>
            """
        ],
        "Reasons <u>not</u> to stay in Sri Lanka": [
            """
            <ul>
                <li>Limited job opportunities in certain industries</li>
                <li>Generally high and fluctuating inflation</li>
                <li>Unstable government and potential for social unrest</li>
            </ul>
            """
        ],
    })

    df_style = reasons_to_stay.style.set_table_attributes('style="width:100%"').hide()
    st.markdown(df_style.to_html(), unsafe_allow_html=True)

    st.markdown(
        f"""
        Despite its progress, <font color={COLORS["Sri Lanka"]}>Sri Lanka</font>  remains a country marked by instability and uncertainty, making it difficult to predict even its near future.""", unsafe_allow_html=True)
