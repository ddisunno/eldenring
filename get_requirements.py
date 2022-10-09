import simplejson as json
import csv
import math

"""
roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}
# IMITATES PICKING ARMAMENTS / SPELLS FROM THE FRONT END (EVERYTHING IN ITEMS_LIST IS CONSIDERED EQUIPPED)
items_list = [{"name": "Greatsword",
			   "file": "json/weapons.json",
			   "is_two_handing": False,
			   "is_powerstancing": False},
			  {"name": "Clawmark Seal",
			   "file": "json/weapons.json",
			   "is_two_handing": False,
			   "is_powerstancing": False},
			  {"name": "Elden Stars",
			   "file": "json/incantations.json"},
			  {"name": "Veteran's Helm",
			   "file": "varmors.json"},
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
"""



def fetch_from_json(item, file):
	"""Function fetch_from_data finds an item in a file
	-----
		inputs:
			item    - thing to find
			file    - file to search
		outputs:
			item_info   - all item data from json
	"""
	

	with open(file) as f:
		data = json.load(f)


	#print(data['count'])
	for i in range(data['count']):
		#if item matches name
		if(item == data['data'][i]['name']):
			item_index = i

	item_info = data['data'][item_index]   
	return item_info


def vigor_calc(desired_health):
	"""Function vigor_calc parses vigor.csv; match HP to vigor level,
	inputs:
		desired_health - amount of health you would like to have
	outputs:
		level of vigor required to have desired health
	"""

	with open('csv/vigor.csv') as f:
		vigor_scaling = csv.reader(f)

		next(vigor_scaling) #skip header

		for level in vigor_scaling:

			HP = float(level[1])

			#print(level[0], HP)

			if int(HP) >= desired_health:
				return int(level[0])


def mind_calc(fp_cost):
	"""Function vigor_calc parses vigor.csv; match HP to vigor level,
	inputs:
		fp_cost - fp cost of spell/ash/etc
	outputs:
		level of mind required to use spell/ash/etc
	"""
	with open('csv/mind.csv') as f:
		mind_scaling = csv.reader(f)

		next(mind_scaling) #skip header

		for level in mind_scaling:

			FP = level[1]

			if int(FP) >= fp_cost:
				return int(level[0])
			

def endurance_calc(weight,roll_type):
	"""Function endurance_calc parses endurance.csv; match equip load to endurance level,
	then returns required endurance to use items at a specified weight with specified roll type
	inputs:
		weight - weight of an item/character
		roll_type - ideal roll_type from dictionary ['light']['med']['fat']['']
	returns:
		level of endurance required to have an equip load that can manage inputted weight
		at desired roll type
	"""
	
	with open('csv/endurance.csv','r') as f:
		endurance_scaling = csv.reader(f)

		next(endurance_scaling) #skip header

		for level in endurance_scaling: #iterate each level

			equip_load = level[1] #column 2: equip load
			equip_load_req = float(equip_load) * float(roll_type) #account for roll type

			#print(f"Endurance: {level[0]} {weight}/{equip_load} ({float(weight)/float(equip_load)*100}%)")
			
			if weight <= equip_load_req: # if weight is less than equip load requirement
				return int(level[0]) #column 1: endurance level


####################################################
def modify_stats(item_name, stat, stat_value, stat_limiter):

	with open('json/stat_modifiers.json') as f:
		data = json.load(f)

	for item in range(len(data[stat])):
		
		if data[stat][item]['name'] == item_name:

			# because we are lowering a requirement, operations will be reversed
			if data[stat][item]['operation'] == "addition":
				new_stat_value = max(stat_value - data[stat][item]['modifier'], 0)
				return new_stat_value

			elif data[stat][item]['operation'] == "subtraction":
				new_stat_value = stat_value + data[stat][item]['modifier']
				return new_stat_value

			elif data[stat][item]['operation'] == "multiplication":
				if stat_limiter:
					new_stat_limiter = stat_limiter / data[stat][item]['modifier']	
					return new_stat_limiter
				else:
					return stat_limiter

			elif data[stat][item]['operation'] == "division":
				if stat_limiter:
					new_stat_limiter = stat_limiter * data[stat][item]['modifier']
					return new_stat_limiter
				else:
					return stat_limiter


	# if item does not modify stat: return the original value
	if stat_limiter != None:
		return stat_limiter	
	else:
		return stat_value



def get_requirements(items_list, desired_health, roll_type):
	"""Function get_requirements
	"""

	weight = 0
	item_reqs = []
	req_stats = [0,0,0,0,0,0,0,0]

	for item in range(len(items_list)): # Let's iterate to get requirements for each item in the list

		# take item_name and item_file out of items_list
		item_name = items_list[item]['name']
		item_file = items_list[item]['file']

		is_two_handing = items_list[item].get('is_two_handing', None)
		is_powerstancing = items_list[item].get('is_powerstancing', None)

		"""
		print(f"item_name: {item_name}\
			  \nis_two_handing: {is_two_handing}\
			  \nis_powerstancing: {is_powerstancing}")
		"""
		
		# get info of the current item
		item_info = fetch_from_json(item_name,item_file)

		# get weight and fp requirements
		if is_powerstancing:
			weight += item_info.get('weight')*2 or 0 # if powerstancing, weight accounts for both
		else:
			weight += item_info.get('weight') or 0 # weight is cumulative
		fp_cost = item_info.get('cost') or 0 # fp cost is static (does not work for weapons (AoW))

		# UNIVERSAL REQUIREMENTS
		vigor_req 	  = vigor_calc(desired_health)
		mind_req 	  = mind_calc(fp_cost)
		endurance_req = endurance_calc(weight,roll_type)

		# SCALAR REQUIREMENTS
		strength_req 		= 0
		dexterity_req 		= 0
		intelligence_req 	= 0
		faith_req 			= 0
		arcane_req 			= 0


		if item_file == 'json/weapons.json' or item_file == 'json/shields.json':

			for stats in item_info['requiredAttributes']:
				
				if stats['name'] == "Str":
					if is_two_handing == True:
						strength_req = math.ceil(stats['amount']*2/3)
					else:
						strength_req = stats['amount']

				if stats['name'] == "Dex":
					dexterity_req = stats['amount']

				if stats['name'] == "Int":
					intelligence_req = stats['amount']

				if stats['name'] == "Fai":
					faith_req = stats['amount']

				if stats['name'] == "Arc":
					arcane_req = stats['amount']

		elif item_file == 'json/armors.json' or item_file == 'json/talismans.json':
			pass

		elif item_file == 'json/incantations.json' or item_file == 'json/sorceries.json':

			for stats in item_info['requires']:

				if stats['name'] == "Intelligence":
					intelligence_req = stats['amount']

				if stats['name'] == "Faith":
					faith_req = stats['amount']

				if stats['name'] == "Arcane":
					arcane_req = stats['amount']



		# KEEP ONLY THE HIGHEST FOR EACH INDEX
		item_reqs.append([vigor_req, mind_req, endurance_req, 
		strength_req, dexterity_req, intelligence_req, faith_req, arcane_req])

		
		for stat in range(8):
			if item_reqs[item][stat] > req_stats[stat]:
				req_stats[stat] = item_reqs[item][stat]


	# time to apply modifiers
	# CALCULATE STAT_LIMITERS FIRST
	for item in range(len(items_list)):

		item_name = items_list[item]['name']

		#print(item_info)

		desired_health = modify_stats(item_name, 'HP', req_stats[0], desired_health)
		req_stats[0] = vigor_calc(desired_health)

		weight = modify_stats(item_name, 'EQUIP LOAD', req_stats[2], weight)
		req_stats[2] = endurance_calc(weight, roll_type)

	# CALCULATE STAT_VALUES LAST
	for item in range(len(items_list)):

		item_name = items_list[item]['name']

		req_stats[0] = modify_stats(item_name, 'vigor', req_stats[0], None)
		req_stats[1] = modify_stats(item_name, 'mind', req_stats[1], None)
		req_stats[2] = modify_stats(item_name, 'endurance', req_stats[2], None)
		req_stats[3] = modify_stats(item_name, 'strength', req_stats[3], None)
		req_stats[4] = modify_stats(item_name, 'dexterity', req_stats[4], None)
		req_stats[5] = modify_stats(item_name, 'intelligence', req_stats[5], None)
		req_stats[6] = modify_stats(item_name, 'faith', req_stats[6], None)
		req_stats[7] = modify_stats(item_name, 'arcane', req_stats[7], None)

	return req_stats

"""
req_stats = get_requirements(items_list, 1900, roll_type['med'])
print(req_stats)
"""