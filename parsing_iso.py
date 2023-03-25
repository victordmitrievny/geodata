import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

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

#------------------------------------------------------------------------------------------------
#Import data from the previous program from the excel (СOMMENTED OUT AS A BACKUP)
# excel_file = pd.read_csv('wikiparsing.csv')
# df = pd.DataFrame(excel_file)
#df = df.set_index('Unnamed: 0')
#------------------------------------------------------------------------------------------------

#Import data from the MySQL server to the DataFrame
engine = create_engine('mysql+pymysql://root:@localhost/geodata')
df = pd.read_sql_table('geodata', engine)
df = df.set_index('ID')

#Certain exceptions (essential to merge tables), not found in Wikipedia, had to fill in manually

df.loc["Canada", "ISO"] = "CA"
df.loc["Republic_of_Congo", "ISO"] = "CG"
df.loc["Democratic_Republic_of_Congo", "ISO"] = "CD"
df.loc["Northern_Cyprus", "ISO"] = "CY"
df.loc["Eritrea", "Population"] = "3600000" #population is not essential but helpful later on
df.loc["Monaco", "Density"] = "100"


#Create and merge Dataframes
df_dataiso = pd.DataFrame(dataiso).T
df = pd.merge(df, df_dataiso, on='ISO')



#Reorder columns:
df = df[["Country Name", 
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


#----------------------------------------------------Additional formatting----------------------------------------
df = df.drop('ISO', axis=1)

#Format Country Name
for i in range(len(df)):
    df.loc[i, "Country Name"] = df.loc[i, "Country Name"].replace('(the)','')

#Format Population
for i in range(len(df)):
    df.loc[i, "Population"] = str(df.loc[i, "Population"])
    df.loc[i, "Population"] = df.loc[i, "Population"].replace(',','').replace(
                                        'nan','0').replace(
                                        '3.6-6.7million','4000000').split('or')[0]

#Format Density
df["Density"] = df["Density"].astype(str)
for i in range(len(df)):
    df.loc[i, "Density"] = df.loc[i, "Density"].replace(',','').split('.')[0].replace('n/a','0').replace('nan','0')

#Format Area
for i in range(len(df)):
   df.loc[i, "Area"] = str(df.loc[i, "Area"])
   df.loc[i, "Area"] = df.loc[i, "Area"].replace(',','').split('.')[0].split('–22072')[0].replace('nan','0') #'-22072' is one exception for a country

#Format Water
df["Water %"] = df["Water %"].astype(str)
for i in range(len(df)):
    df.loc[i, "Water %"] = df.loc[i, "Water %"].replace('Negligible','0').replace('nan','0').replace('N/a','0').replace('n/a','0').split('%')[0]

#Format GDP Total
df["GDP Total"] = df["GDP Total"].astype(str)
for i in range(len(df)):
    df.loc[i, "GDP Total"] = df.loc[i, "GDP Total"].replace(' ','').replace(
                                        'trillion','000000000000').replace(
                                        'billion','000000000').replace(
                                        'million','000000').replace(
                                        'nan','0').replace('n/a','0')
    
#Format GDP Per Capita
df["GDP Per Capita"] = df["GDP Per Capita"].astype(str)
for i in range(len(df)):
    df.loc[i, "GDP Per Capita"] = df.loc[i, "GDP Per Capita"].replace('n/a','0').replace('','0')
    
#Format HDI
df["HDI"] = df["HDI"].astype(str)
for i in range(len(df)):
    df.loc[i, "HDI"] = df.loc[i, "HDI"].replace('very','').replace('nan','0').replace('n/a','0')

#Format Gini
df["Gini"] = df["Gini"].astype(str)
for i in range(len(df)):
    df.loc[i, "Gini"] = df.loc[i, "Gini"].replace('medium','').replace('n/a','0')

#Format Religion string and create columns with diffirent religions
df["Religion"] = df["Religion"].astype(str)
for religion in ['Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism']:
  for i in range(len(df)):
      n = 0
      text = ''
      df.loc[i, religion] = df.loc[i, "Religion"].split(religion)[0].replace('%','').replace(' ','').replace('\n','')
      religion_string = df.loc[i,religion]
      for count in range(len(religion_string)):
        n = n - 1
        if religion_string[n].isalpha() or religion_string[n] in ('[]):-,'):
            df.loc[i,religion] = text
            #Convert the element to a float if its not empty
            if  df.loc[i, religion] != '':
              df.loc[i, religion] = float(df.loc[i, religion])
            break
        else:
            text = religion_string[n] + text
df = df.drop('Religion', axis=1)

#Rearrange column order
df.insert(18, 'ISO3', df.pop('ISO3'))

df["Population"] = df["Population"].astype(int)
df["Density"] = df["Density"].astype(int)
df["Area"] = df["Area"].astype(int)
df["Water %"] = df["Water %"].astype(float)
df["GDP Total"] = df["GDP Total"].astype(int)
df["GDP Per Capita"] = df["GDP Per Capita"].astype(int)
df["HDI"] = df["HDI"].astype(float)
df["Gini"] = df["Gini"].astype(float)
#-------------------------------------------------------------------------------------------------------------------------

#Write back into the SQL server into a new datatable
engine = create_engine('mysql+pymysql://root:@localhost/geodata')
df.to_sql('geodata_iso', con=engine, if_exists='replace', index=False)





