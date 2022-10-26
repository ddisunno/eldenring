import simplejson as json
import os

ignored_files = ["stat_modifiers.json", "reformat_json.py"]


"""
# SIR CAINE BUILD
formatted_inputs = {"armaments": [[{"name": "Greatsword",
									"is_two_handing": False,
									"is_powerstancing": False},
								   {"name": "Clawmark Seal",
								    "is_two_handing": False,
								    "is_powerstancing": False}],
								  [{"name": "Blasphemous Blade",
								    "is_two_handing": True,
								    "is_powerstancing": False}]],
					"armor": [["Veteran's Helm","Erdtree Surcoat","Veteran's Gauntlets","Bull-goat Greaves"]],
					"talismans": [["Crimson Amber Medallion +2","Erdtree's Favor +2","Great-jar's Arsenal", "Radagon Icon"]],
					"spells": [["Elden Stars"]]
				   }
"""
# JAINA PROUDMOORE BUILD
formatted_inputs = {"armaments": [[{"name": "Moonveil", "is_two_handing": False, "is_powerstancing": False},
								   {"name": "Academy Glintstone Staff", "is_two_handing": False, "is_powerstancing": False}]],
					"armor": [["Navy Hood","Noble's Traveling Garb","Noble's Gloves","Noble's Trousers"]],
					"talismans": [["Crimson Amber Medallion +2","Erdtree's Favor +2","Shard Of Alexander", "Radagon Icon"]],
					"spells": [["Carian Slicer", "Gavel Of Haima", "Carian Piercer", "Swift Glintstone Shard", "Adula's Moonblade", "Shard Spiral",
								"Comet", "Glintblade Phalanx", "Glintstone Arc", "Magic Glintblade"]]}

"""
#### iterating through formatted inputs ####

# keys = keys: "armaments","armor","talismans","spells"
for keys in formatted_inputs:
	print(f"\n{'-'*20} {keys.upper()} {'-'*20}\n")
	# groups = list 1 in key: number of groups in a key
	for groups in formatted_inputs[keys]:
		# items = list 2 in key: number of items in a group
		for items in groups:
			# items with additional properties are in dictionary form. ie: armaments
			if type(items) == dict:
				print(f"{items['name']}\
					\n\tTwo Handing: {items['is_two_handing']}\
					\n\tPowerstancing: {items['is_powerstancing']}")
			else:
				print(items)
"""


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
	""" Function get_info takes an item name,
	and returns relevant info from json repository

	inputs:
		item_name - item to parse for

	outputs:
		item_info (contents['data'][item]) - all local information pertaining to the given item
	"""

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


###############################################
def get_reqs(item_name: str, items_info: dict):
	""" Function get_reqs takes an item and returns wielding requirements

	inputs: 
		item_name - item to get requirements of
		items_info - dictionary of all local information pertaining to all formatted inputs

	outputs:
		weight - weight of an item (0 if None)
		req_stats - list of required stats to use an item ([0,0,0,0,0] if None)

	"""

	weight = items_info[item_name].get('weight', 0)


	if 'requiredAttributes' in items_info[item_name].keys():
		strength = items_info[item_name]['requiredAttributes'].get('strength', 0)
		dexterity = items_info[item_name]['requiredAttributes'].get('dexterity', 0)
		intelligence = items_info[item_name]['requiredAttributes'].get('intelligence', 0)
		faith = items_info[item_name]['requiredAttributes'].get('faith', 0)
		arcane = items_info[item_name]['requiredAttributes'].get('arcane', 0)

	else:
		strength, dexterity, intelligence, faith, arcane = 0,0,0,0,0

	req_stats = [strength, dexterity, intelligence, faith, arcane]

	
	"""
	print(item_name, weight)
	print(f"\tStr: {strength}\
	  \n\tDex: {dexterity}\
	  \n\tInt: {intelligence}\
	  \n\tFai: {faith}\
	  \n\tArc: {arcane}")
	"""

	return weight, req_stats


def optimize_reqs(formatted_inputs: dict):

	items_info = {}
	cumulative_weight = 0
	highest_stats = [0,0,0,0,0]

	for keys in formatted_inputs:
		for groups in formatted_inputs[keys]:
			for items in groups:
				if type(items) == dict:
					# get_info - adds an items to items_info dictionary
					items_info[items['name']] = get_info(items['name'])
					#items_info[items['name']].pop('name') # do we need duplicate entries?

					# get_reqs - pulls wielding requirements from items_info
					weight, req_stats = get_reqs(items['name'], items_info)

				else:
					# get_info - adds items to items_info dictionary
					items_info[items] = get_info(items)
					#items_info[items].pop('name') # do we need duplicate entries?

					# get_reqs - pulls wielding requirements from items_info
					weight, req_stats = get_reqs(items, items_info)


				cumulative_weight += weight
				
				for stats in range(len(req_stats)):
					if req_stats[stats] > highest_stats[stats]: # if req_stats is the new highest
						highest_stats[stats] = req_stats[stats] # add req_stats to highest_stats

	#print(items_info.keys())
	#print(*all_info, sep = "\n\n")

	return cumulative_weight, highest_stats
			

req_stats = optimize_reqs(formatted_inputs)
print(req_stats)





"""
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