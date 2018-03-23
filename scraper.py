from googleapiclient.discovery import build
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from termcolor import colored
import requests
import urllib.request
from io import StringIO
import numpy as np
import re

TABLES = False

my_api_key = "AIzaSyD52SO280Xt6xqd6Z1fYUiAfCDOsjrZku8" #KEY EXPIRED Lol m8s
my_cse_id = "013234493367067861201:e_sqh9dvrhy"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def statRetrieval(player):
	TABLES = False

	try:
		results = google_search(player, my_api_key, my_cse_id, num=1)
		prelim_url = results[0]["formattedUrl"]

		# print("RESULTS")
		# print(results[0]["formattedUrl"])
		url = ""
		if "https://" not in prelim_url: 
			url = "https://"+results[0]["formattedUrl"]
		else:
			url = prelim_url

		print("Accessing",url)

		# url = ""
		player_feature_tensor = []

		with urllib.request.urlopen(url) as response:
			# UTF-8 doesn't support some initial character on the websites for some reason!
			r = response.read().decode('latin-1')   		

		content = re.sub(r'(?m)^\<!--.*\n?', '', r)
		content = re.sub(r'(?m)^\-->.*\n?', '', content)

		soup = BeautifulSoup(content, 'html.parser')
		tables = soup.findAll('table')
		# print(tables)


		#Per Game Regular Stats
		reg_table_rows = tables[0].findAll('tr')
		reg_data = reg_table_rows[len(reg_table_rows)-2].findAll('td')

		found_reg_data = False

		for d in range(len(reg_table_rows)-1):
			try:
				if(found_reg_data != True):
					reg_data = reg_table_rows[d].findAll('td')
					reg_data_next = reg_table_rows[d+1].findAll('td')

					if(reg_data_next[0].text == ''):
						found_reg_data = True
						break
			except:
				pass

		reg_stats = []
		reg_stats = np.asarray(reg_stats)


		#Advanced Stats
		adv_table_rows = tables[4].findAll('tr')
		adv_data = adv_table_rows[len(adv_table_rows)-2].findAll('td')


		found_adv_data = False

		for d in range(len(adv_table_rows)-1):
			try:
				if(found_adv_data != True):
					adv_data = adv_table_rows[d].findAll('td')
					adv_data_next = adv_table_rows[d+1].findAll('td')
					if(adv_data_next[0].text == ''):
						found_adv_data = True
						break
			except:
				pass

		adv_stats = []
		adv_stats = np.asarray(adv_stats)
		TABLES = True
		

	except(IndexError, ValueError, KeyError):
		print(colored("No stats exist for this player. He better get on the court!",'red'))

	if(TABLES == True):
		for d in range(len(adv_data)):
			if(d>=4):
				stat = adv_data[d].text
				try:
					adv_stats = np.append(adv_stats,float(stat))
					# print(float(stat))
				except(ValueError):
					adv_stats = np.append(adv_stats, float(0))
					pass

		for d in range(len(reg_data)):
			if(d>=5):
				stat = reg_data[d].text
				try:
					reg_stats = np.append(reg_stats, float(stat))
					# print(float(stat))
				except(ValueError):
					reg_stats = np.append(reg_stats, float(0))
					pass

		# print(reg_stats)
		# print()
		# print(adv_stats)
		player_feature_tensor.append(reg_stats)
		player_feature_tensor.append(adv_stats)

		# print("PFT:")
		# print(np.asarray(player_feature_tensor))

		print(colored("STATS FETCHED", 'green'))
		return player_feature_tensor
	else:
		return False

#testing section
if __name__ == "__main__":

	# try:
	data = statRetrieval("Kevin Durant")
	print()
	print(data)
	# except:
	# 	print("We couldn't get the data on this player!")
