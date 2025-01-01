import matplotlib.pyplot as plt

# TODO - Add definitions for the events
# make it interactive
# add the graphs

# Data
years = [2004, 2009, 2018, 2019, 2020, 2022]
events = [
    "2004 - Tsunami",
    "2009 - Civil War Ended",
    "2018 - Tourism blooming",
    "2019 - Terrorist attack (Easter Attack)",
    "2020 - COVID-19 Pandemic",
    "2022 - Protests against the governance"
]

# Create the plot
fig, ax = plt.subplots(figsize=(6, 10))
ax.set_ylim(2000, 2024)
ax.set_xlim(0, 1)

# Plot each event
for year, event in zip(years, events):
    ax.plot(0.5, year, 'o', color='blue')  # Mark the event on the line
    ax.text(0.6, year, event, fontsize=10, va='center')  # Add the event name

# Add lines and labels
ax.axvline(0.5, color='black', linestyle='--', linewidth=1)  # Vertical timeline
ax.set_yticks(range(2000, 2025, 2))
ax.set_xticks([])
ax.set_title("Timeline of Key Events (2000–2024)", fontsize=12)
ax.set_ylabel("Years")

# Invert y-axis to have 2000 on top
ax.invert_yaxis()

plt.tight_layout()
plt.show()
