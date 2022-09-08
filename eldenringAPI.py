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
import math
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

		for current in range(len(url)): #iterate every url

			response = requests.get(url[current]) # initial response limit=20
			print(response) # did it work? (200)

			pages = math.ceil(response.json()['total']/20) # total number of pages

			domain_path = url[current][34:] # https://eldenring.fanapis.com/api/...
			print(f"Downloading {pages} pages of {domain_path}")

			for page in tqdm(range(pages)):
				if page == 0: #For First Page include metadata
					page_response = requests.get(f"{url[current]}?page={page}")
					data = page_response.json()
				else: # For all concurrent pages omit metadata
					page_response = requests.get(f"{url[current]}?page={page}")
					data['data'].extend(page_response.json()['data'])

				time.sleep(0.1)

			with open(f'{domain_path}.json', 'w') as f:
				json.dump(data,f, indent=2)

			
			time.sleep(0.3)



get_data(url_list, pull = False)

with open('weapons.json') as f:
	weapons = json.load(f)

print(len(weapons['data']))
print(f"{weapons['count']}/{weapons['total']}")


