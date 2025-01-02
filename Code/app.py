import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

# Set page config
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* Make the top-level container taller */
    div[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] {
        height: 600px; /* adjust as needed */
        justify-content: center; /* center slider vertically */
    }

    /* Force the internal container of the slider to stretch */
    div[data-baseweb="select"] {
        display: flex;
        flex-direction: column-reverse; /* so that bigger years appear at the bottom if you prefer */
        height: 100% !important;
        justify-content: space-between;
    }

    /* The "red bar" track that looks like a thermometer */
    /* We insert a pseudo-element behind the handle */
    div[data-baseweb="select"]::before {
        content: "";
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 8px;         /* thickness of the track */
        top: 0;
        bottom: 0;          /* full vertical */
        background: red;    /* color of the thermometer track */
        border-radius: 4px;
        z-index: 0;
    }

    /* Style each "option" in the select_slider, i.e. each year text */
    /* You might want them stacked on the left or right, etc. */
    ul[data-baseweb="select-menu"] > li {
        font-size: 16px;
        font-weight: bold;
        color: white; 
        background: black; /* or whatever background you prefer for the popup */
    }

    /* Style the displayed label (i.e. the chosen year) if needed */
    div[data-baseweb="single-value"] {
        color: #FFFFFF;
        font-weight: bold;
        position: relative;
        z-index: 1; /* on top of the red bar */
        margin: 0 0 5px 0;
    }

    /* Optionally hide the default "dropdown arrow" icon */
    div[data-baseweb="select"] svg {
        display: none;
    }

    </style>
""", unsafe_allow_html=True)



def generate_sample_data():
    dates = pd.date_range(start='2000-01-01', end='2024-12-31', freq='3M')

    data_a = pd.DataFrame({
        'date': dates,
        'value_a': np.random.normal(50, 10, len(dates)),
        'color_a': np.random.choice(['red', 'green', 'blue'], len(dates))
    })

    data_b = pd.DataFrame({
        'date': dates,
        'value_b': np.random.normal(100, 15, len(dates)),
        'color_b': np.random.choice(['red', 'green', 'blue'], len(dates))
    })

    data_c = pd.DataFrame({
        'date': dates,
        'value_c': np.random.normal(150, 20, len(dates)),
        'color_c': np.random.choice(['red', 'green', 'blue'], len(dates))
    })

    data_d = pd.DataFrame({
        'date': dates,
        'value_d': np.random.normal(200, 25, len(dates)),
        'color_d': np.random.choice(['red', 'green', 'blue'], len(dates))
    })

    return data_a, data_b, data_c, data_d


def main():
    st.title("Timeline Visualization")

    # Create columns for layout
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1.5, 1.5, 1.5])

    # Timeline column with single vertical slider
    with col1:
        st.markdown("### Timeline")

        # Create vertical slider
        current_year = st.select_slider(
            "",
            options=list(range(2000, 2025)),
            value=2000,
            key='timeline_slider',
        )

    # Generate and filter data
    data_a, data_b, data_c, data_d = generate_sample_data()

    # Filter data based on selected year
    current_date = pd.Timestamp(f"{current_year}-12-31")
    data_a = data_a[data_a['date'] <= current_date]
    data_b = data_b[data_b['date'] <= current_date]
    data_c = data_c[data_c['date'] <= current_date]
    data_d = data_d[data_d['date'] <= current_date]

    # Column visualizations
    with col2:
        st.markdown("### Column A (0-50)")
        chart_a = alt.Chart(data_a).mark_line(point=True).encode(
            y=alt.Y('date:T',
                    scale=alt.Scale(domain=['2000', '2024']),
                    sort='descending'),
            x=alt.X('value_a:Q', scale=alt.Scale(domain=[0, 50])),
            color=alt.Color('color_a:N', legend=None)
        ).properties(height=600)
        st.altair_chart(chart_a, use_container_width=True)

    with col3:
        st.markdown("### Column B (50-100)")
        chart_b = alt.Chart(data_b).mark_line(point=True).encode(
            y=alt.Y('date:T',
                    scale=alt.Scale(domain=['2000', '2024']),
                    sort='descending'),
            x=alt.X('value_b:Q', scale=alt.Scale(domain=[50, 100])),
            color=alt.Color('color_b:N', legend=None)
        ).properties(height=600)
        st.altair_chart(chart_b, use_container_width=True)

    with col4:
        st.markdown("### Column C (100-150)")
        chart_c = alt.Chart(data_c).mark_line(point=True).encode(
            y=alt.Y('date:T',
                    scale=alt.Scale(domain=['2000', '2024']),
                    sort='descending'),
            x=alt.X('value_c:Q', scale=alt.Scale(domain=[100, 150])),
            color=alt.Color('color_c:N', legend=None)
        ).properties(height=600)
        st.altair_chart(chart_c, use_container_width=True)

    with col5:
        st.markdown("### Column D (150-200)")
        chart_d = alt.Chart(data_d).mark_line(point=True).encode(
            y=alt.Y('date:T',
                    scale=alt.Scale(domain=['2000', '2024']),
                    sort='descending'),
            x=alt.X('value_d:Q', scale=alt.Scale(domain=[150, 200])),
            color=alt.Color('color_d:N', legend=None)
        ).properties(height=600)
        st.altair_chart(chart_d, use_container_width=True)


if __name__ == "__main__":
    main()