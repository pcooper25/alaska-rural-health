# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:13:17 2023

@author: pcooper
"""
#installing necessary packages for data cleaning and to begin creating my dataframe
import pandas as pd
#%%
#reading in social determinant data for 2020, then filtering for AK (fips = '02')
#The dataset is quite large, and not all columns are necessary for this analysis
#lets create a subset of the column that may be useful for later analysis and aggregation


Health = pd.read_csv("social_determinants_2020.csv", dtype=(str))
Health_trim = Health.query("STATEFIPS == '02'")

#The dataset is quite large, and not all columns are necessary for this analysis
#lets create a subset of the column that may be useful for later analysis and aggregation

Health_trim = Health_trim[["YEAR","TRACTFIPS","COUNTYFIPS","STATEFIPS","STATE","COUNTY","ACS_AVG_HH_SIZE","ACS_MEDIAN_AGE",
                              "ACS_PCT_HEALTH_INC_BELOW137","ACS_PCT_MEDICAID_ANY","ACS_PCT_PUBL_TRANSIT","ACS_PCT_UNINSURED","ACS_PER_CAPITA_INC",
                              "ACS_TOT_HH","ACS_TOT_POP_US_ABOVE1","POS_DIST_ED_TRACT", "POS_DIST_MEDSURG_ICU_TRACT", "POS_DIST_TRAUMA_TRACT",
                              "POS_DIST_CLINIC_TRACT", "POS_DIST_ALC_TRACT"]]

#we've trimmed down the data set, but lets set the index to county designation
#Health_trim = Health_trim.set_index("COUNTY")

#now we need to check for NA's in the data, and check it worked
Health_trim_20 =Health_trim.dropna()
print(Health_trim_20) #looks good!

#Need to rename columns for easier understanding, creating a dictionary to do so and attaching to a new dataframe
Health_20 = Health_trim_20.rename(columns={'ACS_AVG_HH_SIZE': 'AvgHHsize','ACS_MEDIAN_AGE':'MedianAge','ACS_PCT_HEALTH_INC_BELOW137':'PercentUnder1.37Poverty',
                                       'ACS_PCT_MEDICAID_ANY':'PopWithMedicaid/Means-Tested','ACS_PCT_PUBL_TRANSIT':'PublicTransit',
                                       'ACS_PCT_UNINSURED':'UninsuredPop','ACS_PER_CAPITA_INC':'IncomePerCapita','ACS_TOT_HH':'TotalHouseholds',
                                       'ACS_TOT_POP_US_ABOVE1':'TotalPop','POS_DIST_ED_TRACT':'DistanceER', 'POS_DIST_MEDSURG_ICU_TRACT': 'DistanceMedSurg/ICU',
                                       'POS_DIST_TRAUMA_TRACT':'DistanceTrauma','POS_DIST_CLINIC_TRACT':'DistanceClinic','POS_DIST_ALC_TRACT':'DistanceRehab'})

#%% 
#There are several entries for each municipality/borough/county. We need a better way to evaluate them
#group the counties and calculate each area's population. 

Tract_Pop = Health_20.groupby('COUNTY', as_index=False)['TotalPop'].apply(lambda x: ' '.join(x.astype(str)))

# Convert 'Tract_Pop' values to integers and sum them
Tract_Pop['TotalPop_Sum'] = Tract_Pop['TotalPop'].str.split().apply(lambda x: sum(int(val) for val in x))

#dropping the total pop column for our new summed total pop
Tract_Pop = Tract_Pop.drop(columns='TotalPop')

#now we need to merge this new dataframe onto our trimmed dataframe
Health_AK = Tract_Pop.merge(Health_20,on='COUNTY',how='inner',indicator=True)
Health_AK.drop_duplicates()
Health_AK = Health_AK.set_index("TRACTFIPS")
Health_AK = Health_AK.drop(columns='_merge')

Health_AK.to_pickle("AK_SocialDeterminants_2020.pkl")
