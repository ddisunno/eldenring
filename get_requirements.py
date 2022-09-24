import simplejson as json
import csv


global roll_type, items_list

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}


# IMITATES PICKING ARMAMENTS / SPELLS FROM THE FRONT END (EVERYTHING IN ITEMS_LIST IS CONSIDERED EQUIPPED)
items_list = [{"name": "Greatsword",
			   "file": "weapons.json"},
			  {"name": "Blasphemous Blade",
			   "file": "weapons.json"},
			  {"name": "Elden Stars",
			   "file": "incantations.json"}]


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
    
    for i in range(data['count']):

        #if item matches name
        if item == data['data'][i]['name']:
            item_index = i


    item_info = data['data'][item_index]   
    return item_info


def vigor_calc(desired_health):
	"""Function vigor_calc parses vigor.csv; match HP to vigor level,
	account for talismans

	inputs:
		desired_health - amount of health you would like to have

	outputs:
		level of vigor required to have desired health

	"""
	with open('vigor.csv') as f:
		vigor_scaling = csv.reader(f)

		next(vigor_scaling) #skip header

		for level in vigor_scaling:

			HP = level[1]

			#print(f"{level[0]}: {HP}")

			if int(HP) >= desired_health:
				return int(level[0])


def mind_calc(fp_cost):
	"""Function vigor_calc parses vigor.csv; match HP to vigor level,
	account for talismans

	inputs:
		fp_cost - fp cost of spell/ash/etc

	outputs:
		level of mind required to use spell/ash/etc

	"""
	with open('mind.csv') as f:
		mind_scaling = csv.reader(f)

		next(mind_scaling) #skip header

		for level in mind_scaling:

			FP = level[1]

			#print(f"{level[0]}: {HP}")

			if int(FP) >= fp_cost:
				return int(level[0])
			

def endurance_calc(weight,roll_type):
	"""Function endurance_calc parses endurance.csv; match equip load to endurance level,
	account for talismans
	then returns required endurance to use items at a specified weight with specified roll type

	inputs:
		weight - weight of an item/character
		roll_type - ideal roll_type from dictionary ['light']['med']['fat']['']
		talismans - [list of talismans] if ___ in talismans:

	returns:
		level of endurance required to have an equip load that can manage inputted weight
		at desired roll type

	"""
	
	with open('endurance.csv','r') as f:
		endurance_scaling = csv.reader(f)

		next(endurance_scaling) #skip header

		for level in endurance_scaling: #iterate each level

			equip_load = level[1] #column 2: equip load
			equip_load_req = float(equip_load) * float(roll_type) #account for roll type

			#print(f"Endurance: {level[0]} {weight}/{equip_load} ({float(weight)/float(equip_load)*100}%)")
			
			if weight <= equip_load_req: # if weight is less than equip load requirement
				return int(level[0]) #column 1: endurance level


####################################################
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
		
		# get info of the current item
		item_info = fetch_from_json(item_name,item_file)

		# get weight and fp requirements
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


		if item_file == 'weapons.json' or item_file == 'shields.json':

			for stats in item_info['requiredAttributes']:
				
				if stats['name'] == "Str":
					strength_req = stats['amount']

				if stats['name'] == "Dex":
					dexterity_req = stats['amount']

				if stats['name'] == "Int":
					intelligence_req = stats['amount']

				if stats['name'] == "Fai":
					faith_req = stats['amount']

				if stats['name'] == "Arc":
					arcane_req = stats['amount']

		elif item_file == 'armors.json':
			pass

		elif item_file == 'incantations.json' or file == 'sorceries.json':

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

	return req_stats


get_requirements(items_list, 1900, roll_type['med'])