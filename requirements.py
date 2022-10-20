import simplejson as json
import os

ignored_files = ["stat_modifiers.json"]

formatted_inputs = {"armaments": [["Greatsword","Clawmark Seal"],["Blasphemous Blade"]],
					 "armor": ["Veteran's Helm","Erdtree Surcoat","Veteran's Gauntlets","Bull-goat Greaves"],
					 "talismans": ["Crimson Amber Medallion +2","Erdtree's Favor +2","Great-jar's Arsenal", "Radagon Icon"],
					 "spells": []
				   }


def init():
	armor_weight = 0,

	req_strength = 0,
	req_dexterity = 0,
	req_intelligence = 0,
	req_faith = 0,
	req_arcane = 0



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


def get_reqs(item_name: str):

	file = get_file("json", item_name)

	# if the item does exist in a file in json directory, we can get it's required attributes
	if file != None:

		# first we load in the file contents
		with open(file) as f:
			contents = json.load(f)


		# next we locate our item in the file
		for item in range(contents['count']):
			if item_name == contents['data'][item]['name']:
				print(f"{item_name} found!")

	
				# requirements vary by item type

				# ARMOR REQUIREMENTS
				if file == "json/armors.json":

					armor_weight = contents['data'][item]['weight']
					#armor_poise = contents['data'][item][]

					return armor_weight

				# WEAPON REQUIREMENTS
				elif file == "json/weapons.json":

					req_strength = 0
					req_dexterity = 0
					req_intelligence = 0
					req_faith = 0
					req_arcane = 0

					requiredAttributes = contents['data'][item]['requiredAttributes']

					for attribute in requiredAttributes:

						if attribute.get('name') == "Str":
							req_strength = attribute.get('amount')
						if attribute.get('name') == "Dex":
							req_dexterity = attribute.get('amount')
						if attribute.get('name') == "Int":
							req_intelligence = attribute.get('amount')
						if attribute.get('name') == "Fai":
							req_faith = attribute.get('amount')
						if attribute.get('name') == "Arc":
							req_arcane = attribute.get('amount')	

					req_stats = [0,0,0,req_strength,req_dexterity,
					req_intelligence,req_faith,req_arcane]

					armament_weight = contents['data'][item]['weight']

					return req_stats, armament_weight




def optimize_reqs(formatted_inputs: dict):

	armor_weight = 0

	armor = formatted_inputs.get("armor")
	armaments = formatted_inputs.get("armaments")
	#talismans = formatted_inputs.get("talismans")
	#spells = formatted_inputs.get("spells")

	for i in range(len(armor)):

		armor_weight += get_reqs(armor[i])

	print(armor_weight)

	for i in range(len(armaments)):

		group = armaments[i]

		for g in group:

			req_stats, armament_weight = get_reqs(g)
			print(req_stats)

		






optimize_reqs(formatted_inputs)