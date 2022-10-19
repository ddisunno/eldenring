import simplejson as json
import os


def get_file(directory: str, item: str):

	for json_file in os.listdir(directory):
		file = os.path.join(directory, json_file)
		
		with open(file) as f:
			contents = json.load(f)
		

		print(f"searching {json_file} for {item}...")
		for i in range(contents['count']):

			if contents['data'][i]['name'] == item:

				print(f"Found {item} in file: {file}")
				return file



	print(f"item not found")
	return None


search_param = input("enter an item to find:\t")

get_file("json", str(search_param))