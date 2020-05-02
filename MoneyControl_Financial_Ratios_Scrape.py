import requests

import csv

from bs4 import BeautifulSoup

import re

hdr = {'User-Agent': 'Mozilla 5.0'}

def get_content(url,hdr):

	#using requests to get the data from website (input - url of the website, headers)
	resp = requests.get(url,headers = hdr)

	return resp.text

def content_html_parse(content_input):

	#parse the web response 
	soup = BeautifulSoup(content_input,'html.parser')

	return soup

def balance_sheet_URL(URL):
	temp = URL.split('/')
	temp.insert(-1, 'balance-sheetVI')
	return '/'.join(temp)




def link_parse_mc(strings):

	#returns link starting with http: and ending with "/s 


	return re.findall(r'http:.+?(?=")',str(strings))[0]



def mc_URL_find(soup):
	find_URL_soup = content_html_parse(find_URL_resp)

	a = find_URL_soup.find('div', 'hidenav_mobile')

	for i in a.find_all('li'):
		if i.text == "Balance sheet":
			return (link_parse_mc(i))
			break

def mc_URL_find(soup):
	find_URL_soup = content_html_parse(find_URL_resp)

	a = find_URL_soup.find('div', 'hidenav_mobile')

	for i in a.find_all('li'):
		if i.text == "Balance sheet":
			return (link_parse_mc(i))
			break



def BalanceSheet_Scrape(URL):

	# returns Balance sheet in list
	resp = get_content(URL,hdr)
	soup = content_html_parse(resp)
	
	BS_body = soup.find('div', id = 'standalone-new')

	BalanceSheet = []

	try:
		for line in BS_body.find_all('tr'):
			line1 = []
			for i in line.find_all('td'):
				line1.append(i.text)

			BalanceSheet.append(line1)

		

	except AttributeError:
		print ('BalanceSheet not available')
		return []

	else:
		return BalanceSheet



with open('moneycontrol_companies_DB.csv') as f:

	f_read = csv.DictReader(f)


	# URL = 'https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI'

	# URL = next(f_read)

	for line in f_read:

		URL = line['URL']

		print (URL)

		find_URL_resp = get_content(URL,hdr)

		BalanceSheet_link = mc_URL_find(find_URL_resp)

		print (BalanceSheet_link)

		BalanceSheet = BalanceSheet_Scrape(BalanceSheet_link)

		if BalanceSheet != []:

			with open(line['Company_Name'] + '.csv','w') as f_write:

				csv_write = csv.writer(f_write)

				for line1 in BalanceSheet:
					csv_write.writerow(line1)
			print (line['Company_Name'],' is written successfully')

		else:
			print (line['Company_Name'],' is not written')
		

























