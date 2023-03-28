import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print('__________')

country_list = []

#------------------------------Find list of countries------------------
response = requests.get('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population')
soup = BeautifulSoup(response.content, 'lxml')
wikitable = soup.find('table', class_=["wikitable,","sortable","jquery-tablesorter"])
tbody = wikitable.find('tbody')
row_list = tbody.findAll('tr')
n = 0
for i in tbody:
	n = n + 1
	if i != '\n' and n > 5 :
		country_name = i.a['href']

		#Format country names suitable for links
		formatted_country_name = country_name.replace(
			'/wiki/', '').replace(
			'Demographics_of_', '').replace(
			'Demography_of_','').replace(
			'the_', '').replace(
			'Population_of_','')
		country_list.append(formatted_country_name)


#------------------------------Scrape data from a given country's infobox
def find_information(country):
	url = "https://en.wikipedia.org/wiki/" + country
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'lxml')
	infobo = soup.find('table', class_="infobox ib-country vcard")
	#Exceptions No.1 (first seen for Netherlands) and Exception No.2 (first seen for Western Sahara)
	if infobo == None:
		infobo = soup.find('table', class_="infobox ib-pol-div vcard")
	if infobo == None:
		infobo = soup.find('table', class_="infobox ib-settlement vcard")
	tbody = infobo.find('tbody')


	#Capital
	def find_capital(table):
		#There are countries where writing code for finding "capital" is just too much effort
		exception_capitals = {'Zwitzerland': 'Bern (de facto)', 'Tokelau': 'Each island has its own administrative center',  'Nauru': 'Yaren (de facto)','Singapore': 'Singapore (city-state)'}
		for tr in table:
			if "Capital" in tr.text:
				if country in exception_capitals.keys():
					return exception_capitals[country]
				else:
					td = tr.find('td', class_="infobox-data")
					datapoint = td.a.text
					return datapoint
		return 'n/a'


	#Government
	def find_government(table):
		for tr in table:
			if "Government" in tr.text:
				#there are exceptions for fields including Seals
				if "Seal" not in tr.text:
					next_element = tr.next_sibling.next_sibling
					td = next_element.find('td', class_="infobox-data")
					datapoint = td.text
					datapoint = td.text.split("[")[0].split('(')[0]
					if country == "Andorra":
						datapoint = td.text.split("[")[0].split('(')[0].split('\n')[1]
					return datapoint
		return 'n/a'

		#,andorra, puerto_rico (joe biden with d)

	#Population
	def find_population(table):
		for tr in table:
			if tr.text == 'Population':
				next_element = tr.next_sibling
				td = next_element.find('td', class_="infobox-data")
				datapoint = td.text.split("[")[0].split('(')[0].replace(' ',',')
				#datapoint_formatted = re.sub("\[.*$",'', datapoint) #remove eveyrthing after "["
				return datapoint
		

	#Density
	def find_density(table):
		for tr in table:
			if 'Density' in tr.text:
				td = tr.find('td', class_="infobox-data")
				datapoint = td.text.split("(")[0].replace('\xa0',' ')
				#if the first number is mile, convert to km and put commas back in. 
				if "sq" in datapoint:
					datapoint = int(datapoint.split()[0].split('[')[0].replace('/sq','').replace('mi','').replace(',','').replace('.',''))/2.6
					datapoint = '{:,}'.format(datapoint)
					return datapoint
				else:
					datapoint = td.text.split()[0]
					datapoint = re.sub("\[.*$",'', datapoint).replace('/km2','')
					return datapoint
		return 'n/a'
		
	#Area
	def find_area(table):
		for tr in table:
			if tr.text == 'Area ' or tr.text == 'Area':
				next_element = tr.next_sibling
				td = next_element.find('td', class_="infobox-data")
				datapoint = td.text.split("(")[0].replace('\xa0',' ')
				#if the first number is square mile, convert to km and put commas back in. "[" is written becuase of liberia
				if "sq mi" in datapoint:
					datapoint = int(datapoint.split()[0].split('[')[0].replace(',',''))*2.589
					datapoint = '{:,}'.format(datapoint)
					return datapoint
				else:
					datapoint = td.text.split()[0]
					datapoint = re.sub("\[.*$",'', datapoint) 
					return datapoint
	
	#Water
	def find_water(table):
		for tr in table:
			if "Water\xa0(%)" in tr.text:
				td = tr.find('td', class_="infobox-data")
				datapoint = td.text.split()[0]
				datapoint = re.sub("\[.*$",'', datapoint).replace('n','N')
				return datapoint
		return 'n/a'

	#GDP nominal
	def find_gdp(table):
		for tr in table:
			if 'GDP\xa0(PPP)' in tr.text:
				next_element = tr.next_sibling
				td = next_element.find('td', class_="infobox-data")
				datapoint = td.text.split("[")[0].split('(')[0]
				for i in ['.',',','$','€','\n','\n','\t','US','£']:
					datapoint = datapoint.replace(i,'').replace('\xa0',' ').strip(' ')
				return datapoint
		return 'n/a'
	
	#GDP per capita
	def find_gdppc(table):
		for tr in table:
			if 'GDP\xa0(PPP)' in tr.text:
				#There is an exception for Virgin Islands where GPT per capita is the first row
				if country != 'United_States_Virgin_Islands':
					next_element = tr.next_sibling.next_sibling
					td = next_element.find('td', class_="infobox-data")
					datapoint = td.text.split("[")[0].split('(')[0]
					for i in ['.',',','$','€','\n','\n','\t','US','£']:
						datapoint = datapoint.replace(i,'').replace('\xa0',' ').strip(' ')
					return datapoint	
				else:
					next_element = tr.next_sibling
					td = next_element.find('td', class_="infobox-data")
					datapoint = td.text.split("[")[0].split('(')[0]
					for i in ['.',',','$','€','\n','\n','\t','US','£']:
						datapoint = datapoint.replace(i,'').replace('\xa0',' ').strip(' ')
					return datapoint
		return 'n/a'

	#HDI
	def find_hdi(table):
		for tr in table:
			if "HDI" in tr.text:
				td = tr.find('td', class_="infobox-data")
				datapoint = td.text.split()[0]
				datapoint = re.sub("\[.*$",'', datapoint) #remove eveyrthing after "["
				return datapoint
		return 'n/a'

	#Gini
	def find_gini(table):
		for tr in table:
			#There is an exception for Papua New Guinea
			if "Gini" in tr.text and "Niu Gini" not in tr.text:
				td = tr.find('td', class_="infobox-data")
				datapoint = td.text.split()[0]
				datapoint = re.sub("\[.*$",'', datapoint) #remove eveyrthing after "["
				return datapoint
		return 'n/a'

	#Currency
	def find_currency(table):
		for tr in table:
			if "Currency" in tr.text:
				td = tr.find('td', class_="infobox-data")
				datapoint = td.text
				#datapoint = re.sub("\[.*$",'', datapoint) #remove eveyrthing after "["
				return datapoint
		return 'n/a'
	
	def find_top_currency(table):
		#Finds USD EUR CAD ETC in a string
		def top_currency_format(currency_text):
			top_currencies = ['(USD)','(EUR)','(JPY)','(GBP)','(AUD)','(CAD)',('CHF'),'(CNY)']
			for symbol in top_currencies:
				if symbol in currency_text:
					return symbol
			return 'n/a'
		#Finds presence of top currency
		for tr in table:
			if "Currency" in tr.text:
				td = tr.find('td', class_="infobox-data")
				datapoint = td.text
				datapoint = top_currency_format(datapoint)
				return datapoint
		return 'n/a'

	def find_religion(table):
		for tr in table:
			if "Religion" in tr.text:
				if "Nation," not in tr.text:
					td = tr.find('td', class_="infobox-data")
					datapoint = td.text
					return datapoint
		return 'n/a'

	#ISO code ISO 3166 alpha 2 code
	def find_iso(table):
		for tr in table:
			if "ISO 3166 code" in tr.text:
				td = tr.find('td', class_="infobox-data")
				#Sometimes the code lengh is more than 2 so have to remove everything but the last two letters
				if len(td.text) > 2:
					datapoint = td.text.split("-")[1]
				else:
					datapoint = td.text
				return datapoint
		return 'n/a'

	#return results
	return { "ID": country,
			 "Capital": find_capital(tbody),
			 "Government": find_government(tbody),
			 "Population":find_population(tbody), 
	 		 "Density": find_density(tbody),
	 		 "Area":	find_area(tbody),
	 		 "Water %": find_water(tbody),
			 "GDP Total": find_gdp(tbody),
			 "GDP Per Capita": find_gdppc(tbody),
			 "HDI": find_hdi(tbody),
			 "Gini": find_gini(tbody),
			 "Currency": find_currency(tbody),
			 "Top Traded Currency": find_top_currency(tbody),
			 "Religion": find_religion(tbody),
			 "ISO": find_iso(tbody)
			}


#Make a dict of dict for all of the data
data = {}
for i in country_list:
	data[i] = find_information(i)
	print(i, data[i])
	print('_')


#Create a dataframe
df = pd.DataFrame(data).T

# Connect to MySQL using SQLAlchemy and Write DataFrame to MySQL
engine = create_engine('mysql+pymysql://baebbc1dedd03e:18882be2@us-cdbr-east-06.cleardb.net/heroku_50f453d91482063')
df.to_sql('geodata', con=engine, if_exists='replace', index=False)


















