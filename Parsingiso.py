import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
pd.set_option('display.max_rows', None)

#---------------------------Parse Iban.com to add ISO Alpha 3 and Country Names using beautiful soup
response_iban = requests.get('https://www.iban.com/country-codes')
soup_iban = BeautifulSoup(response_iban.content, 'lxml')
table_iban = soup_iban.find('table', class_=["table table-bordered downloads tablesorter"])
tbody_iban = table_iban.find('tbody')
tr_list_iban = tbody_iban.findAll('tr')

#Save the data into a dictionary
dataiso = {}
n = 0
country_number = 0
for tr in tr_list_iban:
    for td in tr:
        n = n + 1
        if n == 4:
            country_name = td.find_previous().text
            iso2 = td.text
            iso3 = td.find_next().text
            dataiso[country_number] = {"ISO": iso2,
                                      "ISO3": iso3,
                                      "Country Name": country_name}    
            country_number = country_number + 1    
    n = 0


#Import data from the previous program
excel_file = pd.read_csv('wikiparsing.csv')
df = pd.DataFrame(excel_file)
df = df.set_index('Unnamed: 0')


#Certain exceptions (essential to merge tables), not found in Wikipedia, had to fill in manually
df.loc["Canada", "ISO"] = "CA"
df.loc["Republic_of_Congo", "ISO"] = "CG"
df.loc["Democratic_Republic_of_Congo", "ISO"] = "CD"
df.loc["Northern_Cyprus", "ISO"] = "CY"
df.loc["Eritrea", "Population"] = "3600000" #population is not essential but helpful later on
df.loc["Monaco", "Density"] = "100"


#Create and merge Dataframes
df_dataiso = pd.DataFrame(dataiso).T
df_merged = pd.merge(df, df_dataiso, on='ISO')


#Reorder columns:
df_merged = df_merged[["Country Name", 
                        "Capital", 
                        "Government", 
                        "Population", 
                        "Density", 
                        "Area", 
                        "Water %", 
                        "GDP Total", 
                        "GDP Per Capita", 
                        "HDI", 
                        "Gini", 
                        "Currency", 
                        "Top Traded Currency", 
                        "Religion",
                        "ISO", 
                        "ISO3"]]


# save the DataFrame to a CSV file
df_merged.to_csv('wikiso.csv')






