import simplejson as json
import csv


global roll_type, items_list

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}


# IMITATES PICKING ARMAMENTS / SPELLS FROM THE FRONT END
items_list = [{"name": "Greatsword",
			   "file": "weapons.json"},
			  {"name": "Blasphemous Blade",
			   "file": "weapons.json"},
			  {"name": "Elden Stars",
			   "file": "incantations.json"}]

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

	weight  = item_info.get('weight') or 0
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
	

	if file == 'weapons.json' or file == 'shields.json':

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


def get_base_stats(classes_index):
	"""Function get_base_stats
	inputs:
		classes_index - index of class to pull

	outputs:
		class_name - name of the class at given index
		base_level - level of the class at given index
		base_stats - list[vigor,mind,endurance,strength,dexterity,intelligence,faith,arcane]


	"""
	with open('classes.json') as f:
		classes = json.load(f)

	#INITIALIZE NAME
	class_name		  = classes['data'][classes_index]['name']
	#INITIALIZE BASE STATS
	base_level		  = int(classes['data'][classes_index]['stats']['level'])
	base_vigor		  = int(classes['data'][classes_index]['stats']['vigor'])
	base_mind		  = int(classes['data'][classes_index]['stats']['mind'])
	base_endurance	  = int(classes['data'][classes_index]['stats']['endurance'])
	base_strength	  = int(classes['data'][classes_index]['stats']['strength'])
	base_dexterity	  = int(classes['data'][classes_index]['stats']['dexterity'])
	base_intelligence = int(classes['data'][classes_index]['stats']['intelligence'])
	base_faith		  = int(classes['data'][classes_index]['stats']['faith'])
	base_arcane		  = int(classes['data'][classes_index]['stats']['arcane'])


	base_stats = [base_vigor, base_mind, base_endurance,
	base_strength, base_dexterity, base_intelligence, base_faith, base_arcane]
	
	return class_name, base_level, base_stats


def optimize_class(items_list, roll_type, desired_health):
	"""Function optimize_class takes a list of items and picks the lowest class that
	can use ALL of them INDIVIDUALLY with desired roll_type and HP

	inputs:
		items_list - list of items in dictionary form containing ['name'] - name of the item
																 ['file'] - file the item can be found in
		roll_type - desired roll type from dictionary (multiplier for total equip load)
		desired_health - amount of health to exceed on character

	outputs:
		best_class - name of the best class (able to use everything with the lowest level)
		lowest_level - level of the best class
		best_stats - list of stats of the best class [vig,min,end,str,dex,int,fai,arc]

	"""

	#LIST FORM
	item_reqs = []
	needed_stats = [0,0,0,0,0,0,0,0] #NEEDED STATS = REQUIRED STATS - BASE STATS
	current_stats = [0,0,0,0,0,0,0,0] #CURRENT STATS = BASE STATS + NEEDED STATS
	req_stats = [0,0,0,0,0,0,0,0] # REQUIRED STATS = HIGHEST OF EACH STAT FOR A LIST OF ITEMS

	#TO PICK WINNER
	lowest_level = 999
	best_class = ""
	best_stats = []

	# GET A LIST OF ITEMS
	for item in range(len(items_list)):
		item_reqs.append(get_reqs(items_list[item]['name'], items_list[item]['file'],roll_type,desired_health))

		# KEEP ONLY THE HIGHEST FOR EACH INDEX
		for stat in range(8):
			if item_reqs[item][stat] > req_stats[stat]:
				req_stats[stat] = item_reqs[item][stat]


	for classes_index in range(11): # 11 classes
		class_name, base_level, base_stats = get_base_stats(classes_index)

		for stat in range((len(needed_stats))): #subtract each stat (required - base) not less than 0
			needed_stats[stat] = max(req_stats[stat] - base_stats[stat], 0)

			if needed_stats[stat] != 0: #base is lower than required save required stats
				current_stats[stat] = req_stats[stat]
				#print(f"\tfrom requirements: {current_stats[stat]}") #for testing

			else: #base is higher than required save base stats
				current_stats[stat] = base_stats[stat]
				#print(f"\tfrom base: {class_name} {current_stats[stat]}") #for testing
		
		

		current_level = sum(needed_stats) + base_level

		# store the lowest level class

		if current_level < lowest_level: # new winner

			best_class = class_name
			lowest_level = current_level
			best_stats = current_stats.copy()
			

	print(f"best class is:\
		\n\t{best_class}: {lowest_level}\
		\n\t{best_stats}")

	return best_class, lowest_level, best_stats


def can_equip(character_stats, file):
	"""Function can_use_with_stats takes character stats and returns all items that
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

		item_reqs = get_reqs(data['data'][item]['name'],file,roll_type['med'],0)

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


best_class, lowest_level, best_stats = optimize_class(items_list, roll_type['med'], 1900)

print(can_equip(best_stats, 'weapons.json'))

