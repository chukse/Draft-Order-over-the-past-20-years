import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

# Load the dataset
file_path = 'draft_picks (3).csv'
draft_data = pd.read_csv(file_path)

# Filter the data for the last 20 years
draft_recent = draft_data[draft_data['season'] >= 2003]

# Calculate the average draft order and total weighted AV
average_draft_order = draft_recent.groupby('team')['pick'].mean().sort_values()
team_performance = draft_recent.groupby('team')['w_av'].sum().sort_values(ascending=False)

# Create DataFrame
team_overview = pd.DataFrame({
    'Average Draft Order': average_draft_order,
    'Total Weighted AV': team_performance
})

# Function to read and return an image as a matplotlib object
def getImage(path):
    with Image.open(path) as img:
        return OffsetImage(img, zoom=0.05)  # Adjust zoom as needed

# Plotting
dpi = 100  # Define the DPI for the plot
fig_width, fig_height = 1080 / dpi, 1350 / dpi  # Convert pixel dimensions to inches
fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
ax.set_xlabel('Average Draft Order', fontsize=14)
ax.set_ylabel('Total Weighted AV', fontsize=14)
ax.grid(True)
plt.title('NFL Draft Success Over 20 Years', fontsize=16, pad=20)

# Customize colors
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Mapping from dataset team abbreviations to actual logo file names
team_logo_mapping = {
    'GNB': 'GB',
    'KAN': 'KC',
    'LVR': 'LV',
    'NOR': 'NO',
    'NWE': 'NE',
    'SDG': 'SD',
    'SFO': 'SF',
    'TAM': 'TB'
}

# Path to your logos directory, ensure it ends with a slash
logos_path = 'C:/Users/Chuks/Documents/draft order/logos/'

for i, row in team_overview.iterrows():
    x = row['Average Draft Order']
    y = row['Total Weighted AV']
    if pd.isna(x) or pd.isna(y):
        print(f"Missing data for team: {i}")
        continue
    team_abbreviation = team_logo_mapping.get(i, i)
    logo_path = f'{logos_path}{team_abbreviation}.tif'
    try:
        imagebox = getImage(logo_path)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)
    except FileNotFoundError:
        print(f'Logo file not found for team: {team_abbreviation} (Original: {i})')

# Set plot limits to include all points and adjust margins
ax.set_xlim(team_overview['Average Draft Order'].min() - 10, team_overview['Average Draft Order'].max() + 10)
ax.set_ylim(team_overview['Total Weighted AV'].min() - 100, team_overview['Total Weighted AV'].max() + 100)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

plt.show()
