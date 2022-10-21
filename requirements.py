import simplejson as json
import os

ignored_files = ["stat_modifiers.json"]

formatted_inputs = {"armaments": [[{"name": "Greatsword",
									"is_two_handing": False,
									"is_powerstancing": False},
								   {"name": "Clawmark Seal",
								    "is_two_handing": False,
								    "is_powerstancing": False}],
								  [{"name": "Blasphemous Blade",
								    "is_two_handing": True,
								    "is_powerstancing": False}],
								  [{"name": "Fingerprint Stone Shield",
								    "is_two_handing": False,
								    "is_powerstancing": True}]],
					"armor": [["Veteran's Helm","Erdtree Surcoat","Veteran's Gauntlets","Bull-goat Greaves"]],
					"talismans": [["Crimson Amber Medallion +2","Erdtree's Favor +2","Great-jar's Arsenal", "Radagon Icon"]],
					"spells": [["Elden Stars"]]
				   }

# iterating formatted inputs

# inputs = keys: "armaments","armor","talismans","spells"
for inputs in formatted_inputs:
	# groups = list 1 in key: number of groups in a key
	for groups in formatted_inputs[inputs]:
		# items = list 2 in key: number of items in a group
		for items in groups:
			# items with additional properties are in dictionary form. ie: armaments
			if type(items) == dict:
				print(f"{items['name']}\
					\n\tTwo Handing: {items['is_two_handing']}\
					\n\tPowerstancing: {items['is_powerstancing']}")
			else:
				print(items)




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


#############################
def get_info(item_name: str):

	file = get_file("json", item_name)

	# if the item does exist in a file in json directory, we can get it's required attributes
	if file != None:

		# first we load in the file contents
		with open(file) as f:
			contents = json.load(f)


		# next we locate our item in the file
		for item in range(contents['count']):
			if item_name == contents['data'][item]['name']:

				return contents['data'][item]



all_info = []

for inputs in formatted_inputs:
	for groups in formatted_inputs[inputs]:
		for items in groups:
			if type(items) == dict:
				all_info.append(get_info(items['name']))
			else:
				all_info.append(get_info(items))


print(*all_info, sep = "\n\n")


"""	
				# requirements vary by item type

				# ARMOR REQUIREMENTS
				if file == "json/armors.json":

					armor_weight = contents['data'][item]['weight']
					#armor_poise = contents['data'][item][]

					return armor_weight

				# WEAPON REQUIREMENTS
				elif file == "json/weapons.json" or file == "json/shields.json":

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


				# SPELLS
				elif file == "json/sorceries.json" or file == "json/incantations.json":

					req_intelligence = 0
					req_faith = 0
					req_arcane = 0

					requiredAttributes = contents['data'][item]['requires']

					for attribute in requiredAttributes:

						if attribute.get('name') == "Intelligence":
							req_intelligence = attribute.get('amount')
						if attribute.get('name') == "Faith":
							req_faith = attribute.get('amount')
						if attribute.get('name') == "Arcane":
							req_arcane = attribute.get('amount')	

					req_stats = [0,0,0,0,0,
					req_intelligence,req_faith,req_arcane]

					return req_stats


##########################################
def optimize_reqs(formatted_inputs: dict):

	armor_weight = 0

	armament_weight_list = []

	req_stats_list = []
	total_req_stats = [0,0,0,0,0,0,0,0]

	armor = formatted_inputs.get("armor")
	armaments = formatted_inputs.get("armaments")
	#talismans = formatted_inputs.get("talismans")
	spells = formatted_inputs.get("spells")

	#############################################
	#first lets get the weight of armor as a base
	for i in range(len(armor)):

		armor_weight += get_reqs(armor[i])

	print(armor_weight)

	##################################################################################
	# now lets get the weight of each armament group, and armament required attributes
	for i in range(len(armaments)):

		group = armaments[i]
		group_weights_list = []

		for g in group:

			armament_req_stats, armament_weight = get_reqs(g)
			req_stats_list.append(armament_req_stats)

			#if powerstancing append armament_weight*2
			#if two_handing append math.ceil(armament_weight*2/3)
			group_weights_list.append(armament_weight)		

		# sum weights for armaments equipped together
		armament_weight_list.append(sum(group_weights_list))

	##############################################
	# next lets get required attributes for spells
	for i in range(len(spells)):

		spell_req_stats = get_reqs(spells[i])
		req_stats_list.append(spell_req_stats)

	for i in range(len(talismans)):

		talisman_weight += get_reqs(talismans)


	##########################################################################
	# we only need the highest value for each stat across all armaments/spells
	for i in range(len(req_stats_list)):
		for stat in range(8):
			if req_stats_list[i][stat] > total_req_stats[stat]:
				total_req_stats[stat] = req_stats_list[i][stat]

	print(total_req_stats, armament_weight_list)

optimize_reqs(formatted_inputs)
"""