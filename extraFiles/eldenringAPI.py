"""
eldenringAPI.py
1. pull API from website
2. save it locally with .json extension
references:
Pertaining to API:
	https://jonathansoma.com/lede/foundations-2018/classes/apis/multiple-pages-of-data-from-apis/
	https://developer.atlassian.com/server/confluence/pagination-in-the-rest-api/
Pertaining to JSON
	https://www.youtube.com/watch?v=9N6a-VLBa2I&t=383s
"""

import requests
import time
import simplejson as json
from tqdm import tqdm


url_list = ["https://eldenring.fanapis.com/api/classes",
			"https://eldenring.fanapis.com/api/weapons",
			"https://eldenring.fanapis.com/api/armors",
			"https://eldenring.fanapis.com/api/ashes"]



def get_data(url, pull):
	"""Function get_data pulls data down from the API to local saves with .json extension
	-----
		inputs:
			url 	- a list of urls for API calls
			pull	- a boolean condition determines if the function should execute
		outputs:
			generates/updates json files for each inputted url
	"""
	if pull:

		print(f"Creating json files from eldenring.fanapis.com/api/")

		for current in tqdm(range(len(url))): #iterate every url

			response = requests.get(url[current]) # initial response limit=20
			#print(response) # did it work? (200)

			limit = response.json()['total'] # total number of entries

			domain_path = url[current][34:] # https://eldenring.fanapis.com/api/...
			#print(f"Downloading {limit} {domain_path}") 


			full_response = requests.get(f"{url[current]}?limit={limit}") # set response limit=limit
			data = full_response.json() # all the data


			with open(f'{domain_path}.json', 'w') as f:
				json.dump(data,f)

			time.sleep(0.3)


get_data(['https://eldenring.fanapis.com/api/incantations', 'https://eldenring.fanapis.com/api/sorceries'], pull = True)