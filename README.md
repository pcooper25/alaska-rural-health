# Alaskan Rural Health: Barriers with Distance

## Introduction

This repository contains an insight into the healthcare barriers in the State of Alaska. The analysis focuses on identifying and understanding how various social determninants of health are impacting outcomes, particularly for rural residents. This repository explores various factors such distance to health facilities, percentage of uninsured residents, and presence of public transport. 

## Background

Health disparities between rural and urban populations in the U.S. are well documented. According to the Centers for Disease Control, over 46 million Americans, or 15% of the US population live in rural areas defined by the US Census Bureau. Barriers to healthcare access due to geographic location, limited transportation, and insufficient healthcare infrastructure disproportionately impact rural Americans and result in poor health outcomes and increased healthcare costs. In Alaska, a state with unique geographic challenges and limited transportation options, these barriers are particularly pronounced when it comes to understanding the challenges associated with healthcare access for residents. 

The 49th state according to the [Health Resources & Services Administration](https://data.hrsa.gov/tools/shortage-area) is found to have the following designations which describe some of the challenges the state faces for healthcare:

* Health Professional Shortage Area (HPSA)

* Medically Underserved Area (MUAs)

* Medically Underserved Populations (MUPs)

An HPSA can be anything from geographic areas, populations, or facilities that have a shortage of primary, dental, and/or mental health care providers. MUA/MUPs are designations that identify a geographic areas and populations that have a lack of access to primary care services. Specifically, MUAs have a shortage of services within a certain geographic area and MUPs have a shortage of services for a specific population subset within a given geographic area. 

This is only the surface of the complex nature for healthcare access in Alaska. Not only are there general workforce and supply challenges for the healthcare industry, there are numerous social, economic, geographic, and technological barriers that are also considered in these designations. Understanding these factors is critical to identifying the limitations and difficulties when delivering healthcare in the Last Frontier. 
___
## Data Cleaning, Preparation, and Collection

### *Data Collection*:

The primary data source for this analysis comes from The Agency for Healthcare Research and Quality (AHRQ), which is apart of the Department of Health and Human Services. Data was collected from the AHRQ's database on the Social Determinants of Health, which contains social determinant and demographic data from multiple sources/surveys across the United States. Below is a link to the data source documentation that provides details on the structure and contents of the database:

[Social Determinants of Health Database and Documentation](https://www.ahrq.gov/sites/default/files/wysiwyg/sdoh/SDOH-Data-Sources-Documentation-v1-Final.pdf)

This extensive database contains county, zip code, and census tract data to evaluate the social determinant factors. For this short analysis, the focus was on census tract data for 2020, which is the most recent compilation of availiable. 

The key variables chosen are a sampling of the dataset that are relevant for this anaylsis:

* ACS_AVG_HH_SIZE: Average household size 
* ACS_MEDIAN_AGE: Median age of total population
* ACS_PCT_HEALTH_INC_BELOW137: Percentage of population under 1.37 of the poverty threshold
* ACS_PCT_MEDICAID_ANY: Percentage of population with any Medicaid/Means-tested public health insurance coverage
* ACS_PCT_PUBL_TRANSIT: Percentage of workers taking public transportatin, excluding taxicab (ages 16 and over)
* ACS_PCT_UNINSURED: Percentage of population with no health insurance coverage
* ACS_PER_CAPITA_INC: Per capita income (dollars, inflation-adjusted to data file year)
* ACS_TOT_HH: Total Number of Households
* ACS_TOT_POP_US_ABOVE1: Total population in the U.S. (ages 1 and over)
* POST_DIST_CLINIC_TRACT: Distance in miles to the nearest health clinic (FQHC, RHC),
calculated using population weighted tract centroids
* POS_DIST_ED_TRACT: Distance in miles to the nearest emergency department,
calculated using population weighted tract centroids
* POS_DIST_MEDSURG_ICU_TRACT: Distance in miles to the nearest medical-surgical ICU,
calculated using population weighted tract centroids
* POS_DIST_TRAUMA_TRACT: Distance in miles to the nearest designated trauma center,
calculated using population weighted tract centroids
* POS_DIST_ALC_TRACT: Distance in miles to the nearest hospital with alcohol and
drug abuse inpatient care, calculated using population weighted tract centroids

The SDOH Database for county and census tract files contain ACS 5-year estimates for every year from 2009 to 2020. 

### Data Cleaning: *Health_Clean.py*

* Due to the extensive and detailed nature of this database, the file is too large to be stored on the repository. However, it is publically available to download for use on [Social Determinants of Health Database](https://www.ahrq.gov/sdoh/data-analytics/sdoh-data.html). From there, please choose Census Tract Data for 2020, and then save as a CSV file renamed as **"social_determinants_2020.csv"** This step can be replicated or altered for the different file types and years, depending on user preferance. Please complete this step before following this code. 

This file is the majority of the cleaning for this large database, employing data cleaning strategies to make the dataset more readable and easier to work with. The original dataset encompasses all 50 states and their respective counties, which is then cleaned to only hold the chosen variables and all counties/boroughs in Alaska. Below is an outline of the steps taken in this file:

1. The necessary packages are imported, specifically the pandas library for data manipulation.
- The "social_determinants_2020.csv" file is read using the pd.read_csv() function and stored in the Health DataFrame. The dtype parameter is set to (str) to ensure all columns are read as strings.
- The Health DataFrame is filtered to include only data for Alaska (AK) by using the query() function and the condition "STATEFIPS == '02'". The filtered DataFrame is stored in Health_trim.
- A subset of columns that may be useful for later analysis and aggregation is created using indexing, and the trimmed DataFrame is stored in Health_trim.
- The column names in Health_trim are renamed for easier understanding using the rename() function and a dictionary that maps the old column names to the new names. The renamed DataFrame is stored in Health_20.
- NA values in the Health_trim_20 DataFrame are dropped using the dropna() function, and the resulting DataFrame is stored in Health_trim_20.

2. The Tract_Pop DataFrame is created by grouping the Health_20 DataFrame by 'COUNTY' and applying the join() function to concatenate the 'TotalPop' values for each county.
- The 'TotalPop' values in the Tract_Pop DataFrame are converted to integers and summed using the split() and apply() functions. The summed values are stored in a new column named 'TotalPop_Sum'.
- The 'TotalPop' column is dropped from the Tract_Pop DataFrame.

3. The Tract_Pop DataFrame is merged with the Health_20 DataFrame on the 'COUNTY' column using the merge() function. The merging is done as an inner join, and the resulting DataFrame is stored in Health_AK.
- Duplicate rows in the Health_AK DataFrame are dropped using the drop_duplicates() function.
- The index of the Health_AK DataFrame is set to 'TRACTFIPS' using the set_index() function.
- The '_merge' column, which was created during the merge, is dropped from the Health_AK DataFrame using the drop() function with the columns parameter.

4. The Health_AK DataFrame is saved as a pickle file named "**AK_SocialDeterminants_2020.pkl**" using the to_pickle() function.


### Data Cleaning: *AK_HealthAnalysis.py*

This takes the previously cleaned dataframe of the social determinant data, and continue to clean up the data to be manipulated and aggregated for general analysis on the healthcare barriers in Alaska. 

1. The necessary modules for analysis are imported, including pandas, matplotlib.pyplot, and numpy. The figure's DPI (dots per inch) is set to 300 for better resolution in the saved figures.
- The previously saved DataFrame, "**AK_SocialDeterminants_2020.pkl**," is read using the pd.read_pickle() function and stored in the AK_Health DataFrame.
- The distance columns in the AK_Health DataFrame, namely 'DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', and 'DistanceRehab', are converted to numeric type using the astype() function.
- The maximum distance for each county is calculated by applying the max() function twice on the distance columns for each county using the groupby() function. The results are stored in the county_max_distance Series.
- The top 5 counties with the largest distances are selected from the county_max_distance Series using the nlargest() function and stored in the top_counties Series.
2. A bar plot is created using matplotlib.pyplot. The x-axis represents the counties, and the y-axis represents the maximum distance to a health facility. Each county is assigned a unique color, and the bar plot is saved as "**Alaska Health Facility Distance.png**".
- The columns 'DistanceClinic', 'DistanceER', 'DistanceMedSurg/ICU', 'DistanceTrauma', 'DistanceRehab', 'UninsuredPop', and 'PublicTransit' in the AK_Health DataFrame are converted to string data type.
- The columns mentioned in the previous step are cleaned by removing non-numeric characters using regular expressions with the str.replace() function. After cleaning, the columns are converted to float data type using astype().
3. The cleaned and converted DataFrame is saved as a CSV file named "**AK_Health.csv**" using the to_csv() function.
- The maximum distance and uninsured percentage for each county are calculated by applying the max() function and mean() function, respectively, on the distance and uninsured columns for each county using the groupby() function. The results are stored in the county_max_distance and county_uninsured_percentage Series, respectively.
- The top 5 counties with the largest distances are selected from the county_max_distance Series using the nlargest() function and stored in the top_counties Series.
4. A scatter plot is created using matplotlib.pyplot. The x-axis represents the maximum distance, and the y-axis represents the percentage of uninsured residents. The top 5 counties' points are labeled with their corresponding county names, and the scatter plot is saved as "**Uninsured Distance AK.png**".
- The maximum distance and transit percentage for each county are calculated by applying the max() function and mean() function, respectively, on the distance and transit columns for each county using the groupby() function. The results are stored in the transit_max_distance and county_transit_percentage Series, respectively.
- A scatter plot is created using matplotlib.pyplot. The x-axis represents the maximum distance to a facility, and the y-axis represents the percentage of people taking public transportation. The scatter plot is saved as "**Public Transit and Distance.png**".
___
## Results 
### *Distance to Health Facilities for Alaska Areas*

This figure looks at the different census areas in Alaska, ranking the top 5 counties by the maximum distance to any health facility in the state. With 29 census tract areas in the state, the Aleutians East Borough, Northwest Arctic Borough, North Slope Borough, Yukon-Koyukuk Census Area, and Bethel Census Area residents facing the largest distances to a health care facility. The combined total population of these areas is 36,392 residents as of 2020, which translates to an estimate of 5% of all Alaskan residents facing distances over 250 miles in order to reach a health facility. 

![AK Counties/Boroughs with Highest Distance to Health Facility](Alaska%20Health%20Facility%20Distance.png)

### *Uninsured and Distance Healthcare*

This figure takes the previous finding of the top 5 census areas with the highest distances to a facility, plotting them according to the percentage of residents who are uninsured in that area. 3 of the census areas fall into the range of 22-25% of residents being uninsured and facing maximum distances of 400-425 miles. This is an interesting dispersion of the variables, but it appears that the rate of uninsured residents gets higher as the distance to a health facility increases. 

![Percentage of Uninsured Residents vs. Maximum Distance to Health Facility](Uninsured%20Distance%20AK.png)

### *Public Transit Usage and Distance to Health Facility*

The final figure is now looking at the relationship between the average percentage of residents who take public transit and maximum distance to a health facility. There are a few outliers, but the rates of public transit usage in Alaska are much lower than in other states. Under 10% of total residents on average use public transport as their main form of transportation. Most residents who live in areas with distances to a facility over 50 miles, only account for 0-2% of the average total population who takes public transit. 

![Public Transit and Distance](Public%20Transit%20and%20Distance.png)

___
## Conclusion

This analysis of social determinants of health in Alaska provides valuable insights into factors that may influence health outcomes and access to healthcare services. The findings highlight the significant challenges faced by certain areas in terms of distance to health facilities and how access to reliable transportation, insurance, and other resources are critical to improve these barriers. 

Understanding these social determinants of health can help policymakers and healthcare professionals identify areas that require targeted interventions and resource allocation. By addressing these disparities in access to healthcare services, it is possible to improve health outcomes and promote equity in healthcare delivery for Alaskan residents. 

Th code provided in this repository serves as a starting point for further analysis and exploration of social determinants of health. There is ample opportunity to extend this research to include additional variables, perform further statistical analyses, or explore other geographical areas and spatial relationships. 


