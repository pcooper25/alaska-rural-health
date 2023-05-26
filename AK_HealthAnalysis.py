# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:55:58 2023

@author: pcooper
"""
#Import necessary modules for analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
plt.rcParams['figure.dpi'] = 300
#%% Reading in the previous data file 
AK_Health = pd.read_pickle("AK_SocialDeterminants_2020.pkl")

#much of this data is represented in percentage form, lets begin some premiliminary analysis
#%% Ranking Highest amount of perople by distance to a facility 

# Convert the distance columns to numeric type
AK_Health[['DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', 'DistanceRehab']] = AK_Health[['DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', 'DistanceRehab']].astype(float)


# Calculate the maximum distance for each county
county_max_distance = AK_Health.groupby('COUNTY')['DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', 'DistanceRehab'].apply(lambda x: x.max().max())

# Get the top 5 counties with the largest distances
top_counties = county_max_distance.nlargest(5)

# Create the bar plot
fig, ax = plt.subplots(figsize=(8, 6))

# Create a colormap
colors = plt.cm.Set3(np.linspace(0, 1, len(top_counties)))

# Create the bar plot with custom colors for each county label
bars = ax.bar(top_counties.index, top_counties.values, color=colors)

for bar, color in zip(bars, colors):
    bar.set_color(color)
    
ax.set_xlabel('Alaska Census Tract Designation')
ax.set_ylabel('Maximum Distance to Health Facility')
ax.set_title('AK Counties/Boroughs with Highest Distance to Health Facility')

# Adjust the X-axis labels rotation
plt.xticks(rotation=45)

# Adjust the layout to evenly space the y-axis label
fig.tight_layout(pad=2)
fig.savefig("Alaska Health Facility Distance.png")

#%% Percentage of people uninsured in these counties

# Convert the columns to string data type
AK_Health['DistanceClinic'] = AK_Health['DistanceClinic'].astype(str)
AK_Health['DistanceER'] = AK_Health['DistanceER'].astype(str)
AK_Health['DistanceMedSurg/ICU'] = AK_Health['DistanceMedSurg/ICU'].astype(str)
AK_Health['DistanceTrauma'] = AK_Health['DistanceTrauma'].astype(str)
AK_Health['DistanceRehab'] = AK_Health['DistanceRehab'].astype(str)
AK_Health['UninsuredPop'] = AK_Health['UninsuredPop'].astype(str)
AK_Health['PublicTransit'] = AK_Health['PublicTransit'].astype(str)

# Clean and convert the columns to numeric data types
AK_Health['DistanceClinic'] = AK_Health['DistanceClinic'].str.replace('[^\d.]', '', regex=True).astype(float)
AK_Health['DistanceER'] = AK_Health['DistanceER'].str.replace('[^\d.]', '', regex=True).astype(float)
AK_Health['DistanceMedSurg/ICU'] = AK_Health['DistanceMedSurg/ICU'].str.replace('[^\d.]', '', regex=True).astype(float)
AK_Health['DistanceTrauma'] = AK_Health['DistanceTrauma'].str.replace('[^\d.]', '', regex=True).astype(float)
AK_Health['DistanceRehab'] = AK_Health['DistanceRehab'].str.replace('[^\d.]', '', regex=True).astype(float)
AK_Health['UninsuredPop'] = AK_Health['UninsuredPop'].str.replace('[^\d.]', '', regex=True).astype(float)
AK_Health['PublicTransit'] = AK_Health['PublicTransit'].str.replace('[^\d.]', '', regex=True).astype(float)

AK_Health.to_csv("AK_Health.csv")

# Calculate the maximum distance and uninsured percentage for each county
county_max_distance = AK_Health.groupby('COUNTY')['DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', 'DistanceRehab'].apply(lambda x: x.max().max())
county_uninsured_percentage = AK_Health.groupby('COUNTY')['UninsuredPop'].mean()

# Get the top 5 counties with the largest distances
top_counties = county_max_distance.nlargest(5)

# Create the figure and axes
fig1, ax = plt.subplots(figsize=(8, 6))

# Create the scatter plot
ax.scatter(top_counties.values, county_uninsured_percentage[top_counties.index], color='blue')

# Customize the label names for each point
label_names = ['Aleutians East', 'Northwest Arctic', 'North Slope', 'Yukon-Koyukuk', 'Bethel']

# Add labels for each point
for i, county in enumerate(top_counties.index):
    distance = top_counties.values[i]
    uninsured_percentage = county_uninsured_percentage[county]
    label = label_names[i]
    
    ax.text(distance, uninsured_percentage + 0.2 , label, ha='center', va='bottom', fontsize=6)

ax.set_xlabel('Maximum Distance')
ax.set_ylabel('Percentage of Uninsured Residents')
ax.set_title('Percentage of Uninsured Residents vs. Maximum Distance to Health Facility')

fig1.tight_layout()
fig1.savefig("Uninsured Distance AK.png")
#%%

# Assuming you have a DataFrame named 'AK_Health' with columns 'COUNTY', 'DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU',
# 'DistanceTrauma', 'DistanceRehab', and 'PublicTransit'
# Modify the column names and DataFrame as per your data

# Calculate the maximum distance and transit percentage for each county
transit_max_distance = AK_Health.groupby('COUNTY')['DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', 'DistanceRehab'].apply(lambda x: x.max().max())
county_transit_percentage = AK_Health.groupby('COUNTY')['PublicTransit'].mean()

# Create a figure and axes
fig2, ax = plt.subplots(figsize=(8, 6))

# Scatter plot
ax.scatter(transit_max_distance, county_transit_percentage, color='green')

# Set labels and title
ax.set_xlabel('Maximum Distance to Facility (in miles)')
ax.set_ylabel('Percentage of People Taking Public Transportation')
ax.set_title('Percentage of People Taking Public Transportation vs. Maximum Distance to Facility')

# Show the plot
fig2.tight_layout()
fig2.savefig("Public Transit and Distance.png")

