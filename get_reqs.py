import simplejson as json
import csv


global roll_type

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}

def fetch_from_json(item, file):
	
    with open(file) as f:
        data = json.load(f)
    
    for i in range(data['count']):

        #if item matches name
        if(item == data['data'][i]['name']):
            return data['data'][i]   

    return None

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
	
	with open('eldenring/.csv/endurance.csv','r') as f:
		endurance_scaling = csv.reader(f)

		next(endurance_scaling) #skip header

		for level in endurance_scaling: #iterate each level

			equip_load = level[1] #column 2: equip load
			equip_load_req = float(equip_load) * float(roll_type) #account for roll type

			#print(f"Endurance: {level[0]} {weight}/{equip_load} ({float(weight)/float(equip_load)*100}%)")
			
			if weight <= equip_load_req: # if weight is less than equip load requirement
				return int(level[0]) #column 1: endurance level
			
def get_reqs(item, file, roll_type):
	"""Function get_reqs uses fetch_from_json to find an item
	and generate a list of required item stats

	inputs:
		item - the item to get stat requirements of
		file - the file that contains the item
		roll_type - the desired roll type with said item equipped

	outputs:
		required stats [vigor,mind,endurance,strength,dexterity,intelligence,faith,arcane]
		to use the specified item. (base equip load End:1 = 45 and can med roll with any item)

	"""

	item_info = fetch_from_json(item, file)

	weight = item_info.get('weight')

	# UNIVERSAL REQUIREMENTS
	vigor_req 	  = 1
	mind_req 	  = 1
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

	return [vigor_req, mind_req, endurance_req, 
	strength_req, dexterity_req, intelligence_req, faith_req, arcane_req]

#print(get_reqs("Rivers Of Blood",'weapons.json',roll_type['med']))
#print(get_reqs("Omen Armor",'armors.json',roll_type['light']))
