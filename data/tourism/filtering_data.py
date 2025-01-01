import pandas as pd

# Read the original CSV file
input_file = 'air-passengers-carried.csv'
output_file = 'passengers_from_2000.csv'

# Load the CSV into a DataFrame
data = pd.read_csv(input_file)

# Filter the data for rows where the Year column equals 2000
filtered_data = data[data['Year'] == 2000]

# Save the filtered data to a new CSV file
filtered_data.to_csv(output_file, index=False)

print(f"Filtered data has been saved to {output_file}.")
