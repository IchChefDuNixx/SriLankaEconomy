from pathlib import Path
from data_utils import load_data, load_sl_events
from plot_utils import plot_panel1, plot_panel2


# TODO: https://plotly.com/python/range-slider/
# TODO: decide on styling (colors, marks, etc.)


data_dir = Path(__file__).parent.parent / 'data'
sl_events_path = data_dir / 'sl_events.json'
inflation_path = data_dir / 'inflation/Inflation_Germany_SriLanka_2000_2023.csv'
GDP_path = data_dir / 'gdp/gdp_de_sl_V2.csv'
happiness_path = data_dir / 'happiness/happiness_de_sl.csv'
tourism_path = data_dir / 'tourism/tourism_de_sl.csv'


data = load_data(inflation_path, GDP_path, happiness_path, tourism_path)
sl_events = load_sl_events(sl_events_path)

plot_panel1(data, sl_events)
plot_panel2(data)
