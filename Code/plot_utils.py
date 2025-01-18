import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Sri Lanka's Journey: A comparative study with Germany",
    page_icon="🇱🇰",
    layout='centered', # or wide
    initial_sidebar_state="collapsed")


COLORS = {'good': '#34C759',
          'bad': '#FF3737',
          'neutral': '#808080',
          'inflation': '#FF7043',
          'GDP': '#4DB6AC',
          'happiness': '#81C784',
          'tourism': '#7986CB',
          'Germany': '#4DB6AC',
          'Sri Lanka': '#FF7043'}


def plot_panel1(data: dict[str, dict[str, pd.DataFrame]], sl_events: dict[int, dict[str, str]]) -> None:
    st.title("Sri Lanka Indicators")

    st.write("""
    Here by moving through specific years using the timeline, we can see how events happened in
    these years affected inflation rates, GDP, tourism industry, and happiness of its citizens.
    """)

# Define specific years for the slider
    year_options = [2000, 2004, 2009, 2018, 2019, 2020, 2021, 2022, 2024]
    selected_year = st.select_slider(
        label="Select Year Range",
        options=year_options,
        value=2000, # == starting value
        help=f"You can choose from {year_options}",
        label_visibility="visible"
    )
    assert type(selected_year) == int # typ checking fix


    # Display the selected event name and description
    try:
        with st.container(border=True, height=220):
            # st.write(f"**Year:** {selected_year}")
            selected_event = sl_events[selected_year]['Event']
            # syntax: [label](page_name#section-ID)
            st.write(f"[**{selected_event}**](incidents#{selected_event.lower().replace(' ', '-')})")
            st.write(f"{sl_events[selected_year]['Description']}")
            st.write(f"{sl_events[selected_year]['Effect']}")

    except Exception as e:
        st.write("Error loading event descriptions!")
        st.write(e)


    # Filter data while handling missing values
    all_years = np.arange(2000, 2025)
    visible_years = all_years[all_years <= selected_year]

    inflation_filtered = data['inflation']['sl']['Inflation Value (%)'].reindex(visible_years)
    gdp_filtered = data['GDP']['sl']['GDP per capita (current US$)'].reindex(visible_years)
    happiness_filtered = data['happiness']['sl']['Happiness score'].reindex(visible_years)
    tourism_filtered = data['tourism']['sl']['tourists arrived'].reindex(visible_years)


    g, b, n = COLORS["good"], COLORS["bad"], COLORS["neutral"]

    color_highlights = {
        "inflation": [
            (2000, n),
            (2004, n),
            (2005, b),
            (2008, n),
            (2009, g),
            (2021, n),
            (2022, b),
            (2025, n)
        ],
        "GDP": [
            (2000, n),
            (2009, n),
            (2018, g),
            (2021, n),
            (2022, b),
            (2025, n),
        ],
        "happiness": [
            (2000, n),
            (2015, n),
            (2018, g),
            (2023, n),
            (2025, b),
        ],
        "tourism": [
            (2000, n),
            (2009, n),
            (2018, g),
            (2021, b),
            (2025, n),
        ],
    }

    common_traces = dict(
        mode='lines', # hide markers
        line=dict(width=3),
        marker=dict(size=6),#, color=n),
        hoverinfo="none", # TODO: would be nice to see the year (y-value without the line color inside the tooltip)
    )

    # plot data
    fig = go.Figure()

    for i, (filtered_data, metric) in enumerate([
        (inflation_filtered, 'inflation'),
        (gdp_filtered, 'GDP'),
        (happiness_filtered, 'happiness'),
        (tourism_filtered, 'tourism')
    ], start=1):
        for (start_year, _), (end_year, color) in zip(color_highlights[metric], color_highlights[metric][1:]):
            selection=filtered_data[(filtered_data.index >= start_year) & (filtered_data.index <= end_year)]

            fig.add_trace(
                go.Scatter(
                    x=selection,
                    y=selection.index,
                    xaxis=f"x{i}",      # Use different x-axis for each metric
                    line_color=color,   # if color != n else COLORS[metric],
                    # only highlight markers inside sections >= 2 years
                    marker_color=[n] + [color]*(len(selection) - 2) + [color if len(selection) > 1 else n],
                    **common_traces,
                )
            )

    if selected_year > 2000:
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="y",
            x0=0.5,  # Start of the happiness chart domain
            x1=0.75,  # End of the happiness chart domain
            y0=2000,  # Start of the y-range
            y1=min(selected_year, 2005),  # End of the y-range
            label=dict(
                text="No Data",
                textposition="middle center",
                font=dict(size=14, color="gray")
            ),
            fillcolor="rgba(211, 211, 211, 0.2)",
            opacity=0.4,
            line_width=2,
            line_dash="dash",
            line_color="gray"
        )

    # don't touch domain or side
    fig.update_layout(
        xaxis1=dict(
            domain=[0, 0.25],
            range=[0, 55],
            title="Inflation (%)",
            side="top"
        ),
        xaxis2=dict(
            domain=[0.25, 0.5],
            range=[0, 5100],
            title="GDP per capita",
            side="top"
        ),
        xaxis3=dict(
            domain=[0.5, 0.75],
            range=[0, 9],
            title="Happiness Score",
            side="top"
        ),
        xaxis4=dict(
            domain=[0.75, 1],
            range=[0, 2.5e6],
            title="Yearly Tourist Arrivals",
            side="top"
        ),

        # Reverse range and styling
        yaxis=dict(range=[2025.1, 1999.8]),

        showlegend=False,
        hovermode="y unified",
        height=600
    )

    # Add vertical lines between subplots
    for x in [0.25, 0.5, 0.75]:
        fig.add_vline(
            x=x,
            xref="paper",
            line_dash="dot",
            line_color="gray",
            line_width=0.25
        )

    # render in streamlit
    st.plotly_chart(fig, use_container_width=True)


def plot_inflation_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        # "Year: %{x}<br>"
        "Inflation: <b>%{y:.1f}%</b><br>"
        "Reason: %{customdata[2]}<br>"
        "<extra></extra>"
    )

    # different order because sri lanka's line is above germany
    # different order affects the tooltip order
    # high inflation = bad whereas high gdp/happiness/tourism = good
    for country, df in [('Sri Lanka', data['sl']), ('Germany', data['de'])]:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                # y=df['Inflation'],
                y=df['Inflation Value (%)'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                    df['Reason']
                )),
                hovertemplate=hovertemplate,
                name=country # legend label
            )
        )

    fig.update_layout(
        title_text="Inflation",
        yaxis=dict(range=[0, 51]),
        hovermode='x unified'
    )

    return fig


def plot_GDP_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        # "Year: %{x}<br>"
        "Change YoY <b>%{y:,.2f}%</b><br>"
        "GDP per capita: <b>%{customdata[2]:,.0f}</b> US$<br>"
        "GDP: <b>%{customdata[3]:,.1f}</b> billion US$<br>"
        "Gov. debt: <b>%{customdata[4]:.1f}%</b> of GDP<br>"
        "Industry: <b>%{customdata[5]:.1f}%</b> of GDP<br>"
        "Agriculture: <b>%{customdata[6]:.1f}%</b> of GDP<br>"
        "Services: <b>%{customdata[7]:.1f}%</b> of GDP<br>"
        "Military exp.: <b>%{customdata[8]:.2f}%</b> of GDP<br>"
        "<extra></extra>"
    ) # HTML

    # order, see explanation in plot_inflation_data()
    for country, df in [('Sri Lanka', data['sl']), ('Germany', data['de'])]:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['GDP (billion US$) Annual Change (%)'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                    df['GDP per capita (current US$)'],
                    df['GDP (billion US$)'],
                    df['Government debt (% of GDP)'],
                    df['Industry (including construction), value added (% of GDP)'],
                    df['Agriculture, forestry, and fishing, value added (% of GDP)'],
                    df['Services, value added (% of GDP)'],
                    df['Military expenditure (% of GDP)'],
                )),
                hovertemplate=hovertemplate,
                name=country
            )
        )

    fig.update_layout(
        title_text="GDP per capita (yearly change in %)",
        yaxis=dict(range=[-21, 41]),
        hovermode='x unified'
    )

    return fig


# TODO: ask breunig about dotted line methodology change
def plot_happiness_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Year: %{x}<br>"
        "Rank: #%{customdata[2]:.0f}<br>"
        "Happiness Score: <b>%{y:.2f}</b><br><br>"
        "Score Breakdown:<br>"
        "GDP per capita: <b>%{customdata[3]:.3f}</b><br>"
        "Social support: <b>%{customdata[4]:.3f}</b><br>"
        "Healthy life expectancy: <b>%{customdata[5]:.3f}</b><br>"
        "Freedom to make life choices: <b>%{customdata[6]:.3f}</b><br>"
        "Generosity: <b>%{customdata[7]:.3f}</b><br>"
        "Perceptions of corruption: <b>%{customdata[8]:.3f}</b><br>"
        "Dystopia + residual: <b>%{customdata[9]:.3f}</b><br>"
        "<extra></extra>"
    ) # HTML

    for country, data_df in [('Germany', data['de']), ('Sri Lanka', data['sl'])]:
        # better data source starting from 2015
        for i, df in enumerate([data_df[data_df.index < 2015], data_df[data_df.index >= 2015]]):
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['Happiness score'],
                    line=dict(color=COLORS[country]),
                    customdata=np.column_stack((
                        [country] * len(df),
                        [COLORS[country]] * len(df),
                        df['Happiness rank'],
                        df['GDP per capita'],
                        df['Social support'],
                        df['Healthy life expectancy'],
                        df['Freedom to make life choices'],
                        df['Generosity'],
                        df['Perceptions of corruption'],
                        df['Dystopia + residual']
                    )),
                    hovertemplate=hovertemplate,
                    name=country,
                    showlegend=(i == 0) # hide second identical legend label
                )
            )

    # Missing data
    fig.add_vrect(
        x0=1999.1,
        x1=2004.5,
        label=dict(
            text="No Data",
            textposition="middle center",
            font=dict(size=14, color="gray")
        ),
        fillcolor="rgba(211, 211, 211, 0.2)",
        opacity=0.4,
        line_width=2,
        line_dash="dash",
        line_color="gray"
    )

    # better data source starting from 2015
    fig.add_vline(
        x=2014.5,
        line_dash="dot",
        line_color="gray",
        line_width=1
    )

    fig.add_annotation(
        x=2014.5,
        y=10,
        text="Methodology change",
        showarrow=False
    )

    fig.update_layout(
        title_text="Happiness Score",
        yaxis=dict(range=[0, 10.05]), # 10 or 10.05
        # hovermode='x unified'
    )

    return fig


def plot_tourism_data(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    hovertemplate = (
        "<b style='color:%{customdata[1]}'>%{customdata[0]}</b><br>"
        "Tourists per capita: <b>%{y:,.3f}</b><br>"
        "Total Tourists: <b>%{customdata[2]:,.1f} million</b><br>"
        "Population: <b>%{customdata[3]:,.1f} million</b><br>"
        "<extra></extra>"
    )

    for country, df in [('Germany', data['de']), ('Sri Lanka', data['sl'])]:
        df['tourists_per_capita'] = df['tourists arrived'] / df['population']

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['tourists_per_capita'],
                line=dict(color=COLORS[country]),
                customdata=np.column_stack((
                    [country] * len(df),
                    [COLORS[country]] * len(df),
                    df["tourists arrived"] / 1e6,
                    df["population"] / 1e6
                )),
                hovertemplate=hovertemplate,
                name=country
            )
        )

    fig.update_layout(
        title_text="Yearly Tourist Arrivals per capita",
        yaxis=dict(range=[0, 0.51]),
        hovermode='x unified'
    )

    return fig


def plot_panel2(data: dict[str, dict[str, pd.DataFrame]], plot_descriptions: dict[str, str]) -> None:
    st.title("Comparison Charts") # TODO: improve title

    # TODO: styling
    # Common config for all plots
    common_layout = dict(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    # TODO: styling
    common_traces = dict(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=6)
    )

    figs = {
        'inflation': plot_inflation_data(data['inflation']),
        'GDP': plot_GDP_data(data['GDP']),
        'happiness': plot_happiness_data(data['happiness']),
        'tourism': plot_tourism_data(data['tourism'])
    }

    for key, fig in figs.items():
        col1, col2 = st.columns([2, 1])  # Column widths: 2/3 for plot, 1/3 for text

        # Configure the plot
        fig.update_layout(**common_layout, overwrite=False)
        fig.update_traces(**common_traces, overwrite=False)

        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("<br><br><br>", unsafe_allow_html=True)
            st.write(plot_descriptions.get(key, "Description not available"))

    # add sidebar navigation
    sidebar_items = [
        ("title", "sri-lanka-s-journey-a-comparative-study-with-germany"),
        ("intro", "introduction"),
        ("panel1", "sri-lanka-indicators"),
        ("panel2", "comparison-charts"),
        ("outlook", "outlook")
    ]
    for label, section in sidebar_items:
        st.sidebar.write(f"[{label}](#{section})")