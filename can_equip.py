import json
from get_requirements import get_requirements
from optimize_class import optimize_class
#import simplejson as json

'''
roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}


##### BEGIN: UI INPUTS #####
items_list = [{"name": "Greatsword",
			   "file": 'json/weapons.json'},
			  {"name": "Clawmark Seal",
			   "file": 'json/weapons.json'},
			  {"name": "Elden Stars",
			   "file": "json/incantations.json"},
			  {"name": "Veteran's Helm",
			   "file": "json/armors.json"},
			  {"name": "Erdtree Surcoat",
			   "file": "json/armors.json"},
			  {"name": "Veteran's Gauntlets",
			   "file": "json/armors.json"},
			  {"name": "Bull-goat Greaves",
			   "file": "json/armors.json"},
			  {"name": "Crimson Amber Medallion +2",
			   "file": "json/talismans.json"},
			  {"name": "Erdtree's Favor +2",
			   "file": "json/talismans.json"},
			  {"name": "Great-jar's Arsenal",
			   "file": "json/talismans.json"},
			  {"name": "Radagon Icon",
			   "file": "json/talismans.json"}]


desired_health = 1900

current_roll_type = roll_type['med']

file = 'json/weapons.json'


req_stats = get_requirements(items_list, desired_health, current_roll_type)
best_class, lowest_level, best_stats = optimize_class(req_stats)
##### END: UI INPUTS #####

'''
#### begin code ####
def can_equip(character_stats, current_roll_type, file):
	"""Function can_equip takes character stats and returns all items that
	can be equipped (required stats <= current stats)
	inputs:
		character_stats - stats of character
		file			- file to parse
	outputs:
		can_use 		- list of usable item names
	"""

	can_use = []

	with open(file) as f:
		data = json.load(f)

	for item in range(data['count']):

		item_name = data['data'][item]['name']
		items_list = [{"name" : item_name,
					   "file" : file}]

		item_reqs = get_requirements(items_list, 0, current_roll_type)
		#print(item_reqs) #testing

		for stat in range(len(character_stats)):
			if item_reqs[stat] > character_stats[stat]:
				requirements_met = False
				break
			else:
				requirements_met = True

		if requirements_met:
			can_use.append(data['data'][item]['name'])

		#print(data['data'][item]['name'], requirements_met) #testing

	return can_use


#can_equip = can_equip(best_stats, file)
#print(can_equip)