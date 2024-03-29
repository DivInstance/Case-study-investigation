# -*- coding: utf-8 -*-
"""Divyaranjan_cse_study.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16tYZf6WxRYRQNSWQxT_dfQzLpCk2uYuj

#**NEBULA SPACE ORGANISATION - CAB CASE STUDY**
###***BY DIVYARANJAN SAHOO***
<hr>

###**Problem Description**

XYZ, a private equity firm in the US, is eyeing the growing Cab Industry for potential investment. With the sector experiencing significant growth and having several key players, XYZ sees an opportunity to invest in this thriving market.
<br><br>
###**Data Description**
Data provided here is semi-structured. File format: CSV (comma-separated values)
CSV Files
Provided:

1. Cab_Data.csv -
Contents: Transaction details for two cab companies, including:
Transaction ID, Date of Travel, Company, City, KM Travelled, Price Charged and Cost of Trip in the time period: January 31, 2018, to December 31, 2020



2. Customer_ID.csv - Contents: Customer demographic details, including:
Customer ID, Gender, Age, Income (USD/Month)

3. Transaction_ID.csv - Contents: Mapping table linking transaction IDs to customer IDs and payment modes:
Transaction ID, Customer ID, Payment_Mode

4. City.csv - Contents: Information about US cities, including:
City, Population, Users

<br>
Additional Information: -

Data quality: The data has been reviewed for completeness and consistency, but there are possibilities of potential errors or anomalies, which has to be checked once before analysis.

Missing values: Some fields may contain missing values, which will be addressed during data cleaning.<br><br>

###**Investigation Algorithm**

* Review the Source Documentation
* Understand the field names and data types
* Identify relationships across the files
* Field/feature transformations
* Determine which files should be joined versus which ones should be appended
* Aggregate the data into smaller files and define relationships
* Identify and remove duplicates
* Identify any biasness existing in the data item
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy import stats

"""####**Loading the files**
CSV files are loaded using pandas module into data frames

"""

cab_data = pd.read_csv("Cab_Data.csv")
customer_id = pd.read_csv("Customer_ID.csv")
transaction_id = pd.read_csv("Transaction_ID.csv")
city_data = pd.read_csv("City.csv")

"""Head command to show first 5 values of the table including column attribute

"""

cab_data.head()
customer_id.head()
transaction_id.head()
city_data.head()

"""####**Handling missing values**

Missing data can throw a wrench in our analysis, but fear not! Here is how pandas can be used to handle missing values in the dataset.




"""

#Find missing data
cab_data.isnull().sum()
customer_id.isnull().sum()
transaction_id.isnull().sum()
city_data.isnull().sum()

"""####**Imputation: Fill in the blanks with smart estimates.**

Mean method: Missing values are replaced with the average value for that column to handle null value issue.
"""

#Imputation: Fill empty data with mean
cab_data.fillna(cab_data.mean())
customer_id.fillna(cab_data.mean())
transaction_id.fillna(cab_data.mean())
city_data.fillna(cab_data.mean())

cab_data["Date of Travel"] = pd.to_datetime(cab_data["Date of Travel"])

cab_data.head()

# Merged cab_data and customer_id dataframe
merged_data = transaction_id.merge(cab_data, on="Transaction ID").merge(customer_id, on="Customer ID").merge(city_data, on ="City")

#Data description
merged_data.describe()

merged_data.isnull().sum()
merged_data.fillna(cab_data.mean())

"""##**FROM DATA TO DECISIONS: KEY INSIGHTS AND ANALYTICS**

Here I have presented the data driven analytics using statistical methods, tabular data and graph plotting, the following points were taken care here:

*   Highlighting the specific statistical methods used and how they were applied to the data.
*   Summarizing the key insights and findings uncovered from the analysis.
*   Conveying the significance and impact of my findings in the context of the analysis done here, leading to the final decisions.


"""

# Dataframe information
merged_data.info();

#Check Duplicate rows
duplicate = merged_data[merged_data.duplicated()]
duplicate

"""<hr>

####**Hypothesis testing**

Hypothesis testing is a statistical method used to make inferences about a population based on sample data. Here I have done hypothesis testing by:

1. Formulating a hypothesis: Based on certain decision points, researech questions are formulated
2. Connecting it to data analysis: Comparing fares, transaction volumes, customer profiles, and time series data.
3. Emphasizing the value of data-driven insights: Finding the investment sweet spot and uncovering broader truths.

Here, we'll procceed with our investigation on certain assumptions and get analysis results to encourage/foster our decision to invest.
<br><hr>
#####Hypothesis testing 1 - Los angeles is the city with maximum number of running cabs
"""

#Hypothesis testing 1 -Los angeles is the city with maximum number of running cabs
hypothesis1 = merged_data['City'].value_counts()
hypothesis1

hypothesis1.plot(kind='bar', title='Payment mode dependence')
plt.title('City vs Number of running cabs')
plt.xlabel('City')
plt.ylabel('Number of running cabs')
plt.show()

"""Inference ~ New York and Chicago city has the maximum number of running cabs, it contradicts the hypotesis, i.e Los angeles is the city with maximum number of running cabs <hr>

#####Hypothesis testing 2 - There's no gender based preferences for chosing cab
"""

#Hypothesis testing 2 - There's no gender based preferences for chosing cab
hypothesis2 = pd.crosstab(merged_data['Gender'], merged_data['Company'])
hypothesis2

div_colors = ['pink','yellow']
hypothesis2.plot(kind='bar', title='Gender preference', color=div_colors)
plt.title('Gender based cab preference')
plt.xlabel('Gender')
plt.ylabel('Number of running cabs')
plt.show()

"""#####Inference - The analysis output shows that male are more consumers of cab in US than female, overally yellow cab are more prefered <br><hr>

####Hypothesis Testing 3 - People prefer yellow cabs more in winter (November (11) to January (1))
"""

# Hypothesis testing 3 - People prefer yellow cabs more in winter (November (11) to January (1))
winter_months = [11,12,1]
other_months = [2,3,4,5,6,7,8,9,10]
nonwinter_trips = merged_data[((merged_data["Company"] == "Pink Cab") | (merged_data["Company"] == "Yellow Cab")) & (merged_data["Date of Travel"].dt.month.isin(other_months))]
winter_trips = merged_data[((merged_data["Company"] == "Pink Cab") | (merged_data["Company"] == "Yellow Cab")) & (merged_data["Date of Travel"].dt.month.isin(winter_months))]
hypothesis3 = winter_trips.groupby("Company")["Transaction ID"].count()
hypothesis3

hypothesis3.plot(kind='bar', title='Winter Preference')
plt.title('Winter cab preference')
plt.xlabel('Cab company')
plt.ylabel('Number of running cabs')
plt.show()

#Hypothesis Testing 4 - Payment mode is dependent variable for clients
hypothesis4 = pd.crosstab(merged_data['Payment_Mode'], merged_data['Company'])
hypothesis4

#Plot, with color assigned to company
#div_colors = ['pink' if company == 'Pink Cab' else 'yellow' for company in merged_data['Company']]
div_colors = ['pink','yellow']
hypothesis4.plot(kind='bar', title='Payment Mode Dependence', color=div_colors)
plt.xlabel('Payment Mode')
plt.ylabel('Company')
plt.show()

#Hypothesis Testing 5 - Margin proportionally increase with increase in number of customers

merged_data['Margin'] = merged_data['Price Charged'] - merged_data['Cost of Trip']

# Visualize the relationship between Number of Customers and Margin
plt.scatter(merged_data.groupby('Transaction ID').size(), merged_data.groupby('Transaction ID')['Margin'].mean())
plt.title('Margin vs Number of Customers')
plt.xlabel('Number of Customers')
plt.ylabel('Average Margin')
plt.show()

customer_segments = merged_data.groupby('Customer ID').agg({ 'Gender': 'first', 'Age': 'mean','Income (USD/Month)': 'mean','Transaction ID': 'count'}).rename(columns={'Transaction ID': 'Number of Transactions'})
customer_segments.describe()

"""<hr>

####**Hypothesis Testing 6 - Young customers (Age 18 to 24) prefer yellow cabs more**
"""

#Hypothesis testing 6 - Young customers (Age 18 to 24 )prefer yellow cabs more
young_people_data = merged_data[(merged_data['Age'] >= 18) & (merged_data['Age'] <= 24)]
hypothesis6 = young_people_data.groupby('Company').size()
hypothesis6

hypothesis6.plot(kind='bar', title='Cab Preferences of Young People (Aged 18-24)')
plt.xlabel('Cab Company')
plt.ylabel('Number of Trips')
plt.show()

"""Inference - Hypothesis true
<br><hr>
"""

#Hypothesis 7 - There's no variance of cab preference between cities
# Contingency Table
hypothesis7 = pd.crosstab(merged_data['City'], merged_data['Company'])
hypothesis7

hypothesis7.plot(kind='bar', title='Cab preference over cities')
plt.xlabel('City')
plt.ylabel('Number of Trips')
plt.show()

df = merged_data.groupby("Company")["Transaction ID"].count()
df

hypothesis6.plot(kind='bar', title='Yellow vs Pink',color='red')
plt.xlabel('Cab company')
plt.ylabel('Customers')
plt.show()

