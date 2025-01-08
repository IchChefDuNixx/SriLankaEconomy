import pandas as pd

# Data for Germany
data_germany = {
    "Year": list(range(2000, 2024)),
    "Country": ["Germany"] * 24,
    "Inflation Value (%)": [
        2.0, 1.9, 1.4, 1.0, 1.8, 1.6, 1.8, 2.3, 2.8, 0.3, 1.1, 2.1, 2.0, 1.5,
        0.8, 0.3, 0.5, 1.5, 1.9, 1.4, 0.5, 3.2, 8.7, 6.0
    ],
    "Reason": [
        "Stable Eurozone growth, rising oil prices",
        "Global slowdown post-dot-com bubble",
        "Euro introduction stabilizing prices",
        "Eurozone slowdown and weak growth",
        "Oil price rise and economic recovery",
        "Labor market reforms (Hartz IV)",
        "Export-driven economic recovery",
        "Oil and food price hikes",
        "Oil price peak before financial crisis",
        "Global recession from financial crisis",
        "Economic stabilization post-crisis",
        "Higher energy prices, Eurozone recovery",
        "Eurozone debt crisis effects",
        "Slow economic growth in Germany",
        "Falling global oil prices",
        "Deflationary pressures, low energy prices",
        "Energy prices stabilize",
        "Higher energy prices, strong growth",
        "Robust domestic demand, moderate oil prices",
        "Global trade tensions slowing growth",
        "COVID-19 pandemic, VAT reductions",
        "Supply chain disruptions, energy price spikes",
        "Ukraine war, energy crisis",
        "Moderated energy prices, ECB rate hikes"
    ]
}

# Data for Sri Lanka
data_srilanka = {
    "Year": list(range(2000, 2024)),
    "Country": ["Sri Lanka"] * 24,
    "Inflation Value (%)": [
        6.2, 14.2, 9.6, 6.3, 7.6, 11.6, 10.0, 15.8, 22.6, 3.5, 6.2, 6.7, 9.2, 6.9,
        3.3, 0.9, 4.0, 7.7, 2.1, 4.3, 6.0, 9.9, 45.0, 12.0
    ],
    "Reason": [
        "High fiscal deficits during civil war",
        "Recession due to war and instability",
        "Peace talks reduced economic pressures",
        "Improved economic conditions post-tsunami",
        "Tsunami recovery costs, oil prices rise",
        "Energy costs and post-tsunami recovery",
        "Ongoing war, food and fuel price hikes",
        "Oil price spikes and conflict spending",
        "Post-war stabilization of economy",
        "Post-war reconstruction and food costs",
        "Global commodity price rise",
        "Currency depreciation, high import costs",
        "Improved stability, tighter policies",
        "Low oil prices, fiscal consolidation",
        "Stable commodity prices, fiscal reforms",
        "Drought-induced higher food prices",
        "Severe drought increased dependency on imports",
        "Agricultural recovery post-drought",
        "Easter attacks disrupted supply chains",
        "COVID-19 disruptions, supply shortages",
        "Currency depreciation, money printing",
        "Economic crisis, food and fuel shortages",
        "IMF reforms stabilized economy and currency"
    ]
}

# Identify the mismatched length for Germany
print("Checking Germany data:")
for key, value in data_germany.items():
    print(f"{key}: {len(value)} entries")

# Identify the mismatched length for Sri Lanka
print("Checking Sri Lanka data:")
for key, value in data_srilanka.items():
    print(f"{key}: {len(value)} entries")

# If mismatched lengths are found, fix them
# Example: Add placeholders or remove excess elements
for key, value in data_germany.items():
    while len(value) < 24:
        value.append(None)  # Add placeholder
    data_germany[key] = value[:24]  # Trim excess if needed

for key, value in data_srilanka.items():
    while len(value) < 24:
        value.append(None)  # Add placeholder
    data_srilanka[key] = value[:24]  # Trim excess if needed

# Create DataFrames
df_germany = pd.DataFrame(data_germany)
df_srilanka = pd.DataFrame(data_srilanka)

# Combine the data
df_combined = pd.concat([df_germany, df_srilanka], ignore_index=True)

# Save to CSV
file_path = "/Users/amindudesilva/Desktop/vis24/srilanka/data/inflation/Inflation_Germany_SriLanka_2000_2023.csv"
df_combined.to_csv(file_path, index=False)

print(f"CSV file has been saved at: {file_path}")
