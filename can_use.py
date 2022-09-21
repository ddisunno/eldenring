import simplejson as json
import csv

# SAMPLE CHARACTER STATS FROM SIR CAINE PALADIN BUILD
character_stats = [50,10,31,34,13,9,50,7]


import simplejson as json
import csv


global roll_type, items_list

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}

items_list = [{"name": "Greatsword",
			   "file": "weapons.json"},
			  {"name": "Blasphemous Blade",
			   "file": "weapons.json"},
			  {"name": "Elden Stars",
			   "file": "incantations.json"},
			  {"name": "Rock Sling",
			   "file": "sorceries.json"}]

equipped_talismans = []


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
			


def get_reqs(item, file, roll_type, desired_health):
	"""Function get_reqs uses fetch_from_json to find an item
	and generate a list of required item stats

	inputs:
		item - the item to get stat requirements of
		file - the file that contains the item
		roll_type - the desired roll type with said item equipped
		desired_health - the desired health of build

	outputs:
		required stats [vigor,mind,endurance,strength,dexterity,intelligence,faith,arcane]
		to use the specified item. (base equip load End:1 = 45 and can med roll with any item)

	"""

	item_info = fetch_from_json(item, file)

	weight = item_info.get('weight') or 0
	fp_cost = item_info.get('cost') or 0

	# UNIVERSAL REQUIREMENTS
	vigor_req 	  = vigor_calc(desired_health)
	mind_req 	  = mind_calc(fp_cost)
	endurance_req = endurance_calc(weight,roll_type)

	# WEAPON REQUIREMENTS
	strength_req 		= 0
	dexterity_req 		= 0
	intelligence_req 	= 0
	faith_req 			= 0
	arcane_req 			= 0
	

	if file == 'weapons.json':

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

		"""
		print(f"Required stats for {item}\
			\n\tStr: {strength_req}\
			\n\tDex: {dexterity_req}\
			\n\tInt: {intelligence_req}\
			\n\tFai: {faith_req}\
			\n\tArc: {arcane_req}\
			\n\tEnd: {endurance_req}")
		"""

	elif file == 'armors.json':
		pass

	elif file == 'incantations.json' or file == 'sorceries.json':

		for stats in item_info['requires']:

			if stats['name'] == "Intelligence":
				intelligence_req = stats['amount']

			if stats['name'] == "Faith":
				faith_req = stats['amount']

			if stats['name'] == "Arcane":
				arcane_req = stats['amount']



	req_stats = [vigor_req, mind_req, endurance_req, 
	strength_req, dexterity_req, intelligence_req, faith_req, arcane_req]

	return req_stats













################################################################################

def can_use_with_stats(character_stats, file):
	"""Function can_use_with_stats takes character stats and returns all items that
	can be equipped (required stats <= current stats)

	inputs:
		character_stats - stats of character
		file			- file to parse

	outputs: equippable_...
	"""

	can_use = []

	with open(file) as f:
		data = json.load(f)

	for item in range(data['count']):

		"""
		if file == "weapons.json": #different naming conventions for stats by json
			print(data['data'][item]['name'])

			for stat in data['data'][item]['requiredAttributes']:
				print(f"{stat['name']}: {stat['amount']}")
		"""

		item_reqs = get_reqs(data['data'][item]['name'],file,roll_type['med'],0)

		for stat in range(len(character_stats)):
			if item_reqs[stat] > character_stats[stat]:
				requirements_met = False
				break
			else:
				requirements_met = True

		if requirements_met:
			can_use.append(data['data'][item]['name'])

	return can_use


can_use_with_stats(character_stats, 'weapons.json')
can_use_with_stats(character_stats, 'incantations.json')

