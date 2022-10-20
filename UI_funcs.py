import simplejson as json
import os
import requests
import time
import math
from tqdm import tqdm

# MacOS creates a hidden .DS_Store file that cannot be parsed by this code
# https://stackoverflow.com/questions/107701/how-can-i-remove-ds-store-files-from-a-git-repository

url_list = ["https://eldenring.fanapis.com/api/classes",
			"https://eldenring.fanapis.com/api/weapons",
			"https://eldenring.fanapis.com/api/shields",
			"https://eldenring.fanapis.com/api/ashes",
			"https://eldenring.fanapis.com/api/armors",
			"https://eldenring.fanapis.com/api/talismans",
			"https://eldenring.fanapis.com/api/incantations",
			"https://eldenring.fanapis.com/api/sorceries"]

ignored_files = ["stat_modifiers.json"]

########################
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

		for current in range(len(url_list)): #iterate every url

			response = requests.get(url[current]) # initial response limit=20
			#print(response) # did it work? (200)

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

				time.sleep(0.1) # don't spam

			data['count'] = len(data['data']) #change count from page total to file total

			with open(f'{domain_path}.json', 'w') as f:
				json.dump(data,f, indent=2)

			
			time.sleep(0.3)

########################################
def get_file(directory: str, item: str):
	"""Function get_file searches for an item in a directory of files
	and returns a file that contains the item (if such a file exists).

	inputs:
		directory - directory to parse: directories named for file extensions
		item - search parameters
	outputs:
		file - file containing item

		*if item is not found, function returns None
	"""

	for json_file in os.listdir(directory):
		file = os.path.join(directory, json_file)

		if json_file in ignored_files:
			#print(f"skipping {json_file}")
			continue
		
		with open(file) as f:
			contents = json.load(f)

		#print(f"searching {json_file} for {item}...")
		for i in range(contents['count']):

			if contents['data'][i]['name'] == item:

				#print(f"Found {item} in file: {file}")
				return file

	print(f"{item} not found")
	return None

#################################
def format_inputs(accept_inputs):
	"""Function format_inputs formats inputs into a list of items
	inputs:
		accept_inputs - conditional statement, 
						function collects new entries while True
	outputs:
		items_list - formatted list of items where
					 each item has keys: name, file
				
		example:			 
		items_list = [{name: Greatsword,
	 				   file: json/weapons.json},...]
	"""
	items_list = [] #initialize items_list

	print("Formatting Inputs, (enter 'quit' to exit)")
	while accept_inputs == True:
		
		new_entry = input(f"Add equipment:\t")

		if new_entry == "quit" or None:
			break

		file = get_file("json", new_entry)
		if file != None:
			items_list.append({"name": new_entry,
							   "file": file})

	return items_list