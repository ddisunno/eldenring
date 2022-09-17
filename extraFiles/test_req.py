import simplejson as json
import csv


global roll_type

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}

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
	
	with open('eldenring/.csv/endurance.csv','r') as f:
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
	with open('eldenring/.csv/vigor.csv') as f:
		vigor_scaling = csv.reader(f)

		next(vigor_scaling) #skip header

		for level in vigor_scaling:

			HP = level[1]

			#print(f"{level[0]}: {HP}")

			if int(HP) >= desired_health:
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

	weight = item_info.get('weight')

	# UNIVERSAL REQUIREMENTS
	vigor_req 	  = vigor_calc(desired_health)
	mind_req 	  = 1
	endurance_req = endurance_calc(weight,roll_type)

	# WEAPON REQUIREMENTS
	strength_req 		= 0
	dexterity_req 		= 0
	intelligence_req 	= 0
	faith_req 			= 0
	arcane_req 			= 0
	

	if file == 'eldenring/.json/weapons.json':

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

	elif file == 'eldenring/.json/armors.json':
		pass

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
	with open('eldenring/.json/classes.json') as f:
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


def optimize_class(req_stats):


	#LIST FORM
	needed_stats = [0,0,0,0,0,0,0,0] #INITIALIZE NEEDED STATS

	current_stats = [0,0,0,0,0,0,0,0] #INITIALIZE CURRENT STATS

	#TO PICK WINNER
	lowest_level = 999
	best_class = ""
	best_stats = []


	for classes_index in range(11): # 11 classes
		class_name, base_level, base_stats = get_base_stats(classes_index)

		#print(class_name) #for testing

		for stat in range((len(needed_stats))): #subtract each stat (required - base) not less than 0
			needed_stats[stat] = max(req_stats[stat] - base_stats[stat], 0)

			if needed_stats[stat] != 0: #base is lower than required save required stats
				current_stats[stat] = req_stats[stat]
				#print(f"\tfrom requirements: {current_stats[stat]}") #for testing

			else: #base is higher than required save base stats
				current_stats[stat] = base_stats[stat]
				#print(f"\tfrom base: {class_name} {current_stats[stat]}") #for testing
		
		

		current_level = sum(needed_stats) + base_level

		print(f"{class_name}: {current_level}")
		print(f"\t{current_stats}")

		# store the lowest level class

		if current_level < lowest_level: # new winner

			best_class = class_name
			lowest_level = current_level
			best_stats = current_stats.copy()

		#print(best_class, best_current_stats)

			

	print(f"best class is:\
		\n\t{best_class}: {lowest_level}\
		\n\t{best_stats}")




item_req = get_reqs("Greatsword",'eldenring/.json/weapons.json',roll_type['med'], 1900)
#print(item_req)


# RETURNING MIND FOR INTELLIGENCE????

optimize_class(item_req)
