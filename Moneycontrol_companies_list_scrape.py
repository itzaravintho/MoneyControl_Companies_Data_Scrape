import requests

import csv

from bs4 import BeautifulSoup

#get all the sectors available in moneycontrol

base_url = 'https://www.moneycontrol.com/india/stockpricequote'

hdr = {'User-Agent': 'Mozilla 5.0'}

alphabets_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','others']

def get_content(url,hdr):

	#using requests to get the data from website (input - url of the website, headers)
	resp = requests.get(url,hdr)

	return resp.text



def content_html_parse(content_input):
	soup = BeautifulSoup(content_input,'html.parser')

	return soup


# url = base_url +'/'+ 'A'




def get_href(ip):
	temp = ip.split('"')
	url = ''
	for i in temp:
		if i[0:4] == 'http':
			url = i
			break
	return url 

def get_url_prop(url):
	temp = url.split('/')
	index_ = ''

	for i in temp:
		if i == 'stockpricequote':
			index_ = temp.index(i)
			break

	return [temp[index_+1],temp[index_+2]]


def get_comp_details(html_split_data):
	
	int_list = []

	for line in html_split_data.find_all('td'):

	# print (line)

		if len(line.text) != 0:

			url1 = get_href(str(line))

			a = get_url_prop(url1)

			int_list.append({'Company_Name': a[1] , 'Category' : a[0], 'M_Name' : line.text ,'URL' : url1})

	return int_list

final_list = []

for alp1 in alphabets_order:

	url = base_url + '/' + alp1

	sectors_raw = get_content(url,hdr)

	sectors_content = content_html_parse(sectors_raw).find('div',class_ = 'PT15')

	sectors_table = sectors_content.find('table')

	for i in get_comp_details(sectors_table):
		final_list.append(i)

	# final_list.append(get_comp_details(sectors_table))

	print ('Completed ','\t', alp1)

with open ('moneycontrol_companies_DB.csv','w') as f:

	fieldnames = ['Company_Name', 'Category', 'M_Name', 'URL']
	
	csv_writer = csv.DictWriter(f,fieldnames = fieldnames)

	csv_writer.writeheader()

	for line in final_list:

		print (line)

		csv_writer.writerow(line)

# for i in final_list:
# 	print (i)
# 	print ()



