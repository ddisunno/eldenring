import simplejson as json
import csv

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}

def get_info(item, file):
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
	"""Function vigor_calc parses vigor.csv; match HP to vigor level
	inputs:
		desired_health - amount of health you would like to have
	outputs:
		level of vigor required to have desired health

	"""

	with open('vigor.csv') as f:
		vigor_scaling = csv.reader(f)

		next(vigor_scaling) #skip header

		for level in vigor_scaling:

			HP = float(level[1])

			if int(HP) >= desired_health:
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


# NEW CODE BEGINS UNDER LINE

#####################################
stats = [60, 4, 43, 31, 12, 0, 50, 0]

items_list = [{"name": "Greatsword",
			   "file": "weapons.json"},
			  {"name": "Clawmark Seal",
			   "file": "weapons.json"},
			  {"name": "Elden Stars",
			   "file": "incantations.json"},
			  {"name": "Veteran's Helm",
			   "file": "armors.json"},
			  {"name": "Erdtree Surcoat",
			   "file": "armors.json"},
			  {"name": "Veteran's Gauntlets",
			   "file": "armors.json"},
			  {"name": "Bull-goat Greaves",
			   "file": "armors.json"},
			  {"name": "Crimson Amber Medallion +2",
			   "file": "talismans.json"},
			  {"name": "Erdtree's Favor +2",
			   "file": "talismans.json"}]




def modify_stats(item_name, stat, stat_value, stat_limiter):

	with open('stat_modifiers.json') as f:
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


def apply_modifiers(stats, HP_req, weight_req):


	# CALCULATE STAT_LIMITERS FIRST
	for item in range(len(items_list)):

		item_name = items_list[item]['name']

		#print(item_info)

		HP_req = modify_stats(item_name, 'HP', stats[0], HP_req)
		stats[0] = vigor_calc(HP_req)

		weight_req = modify_stats(item_name, 'EQUIP LOAD', stats[2], weight_req)
		stats[2] = endurance_calc(weight_req, roll_type['med'])

	# CALCULATE STAT_VALUES LAST
	for item in range(len(items_list)):

		item_name = items_list[item]['name']

		stats[0] = modify_stats(item_name, 'vigor', stats[0], None)
		stats[1] = modify_stats(item_name, 'mind', stats[1], None)
		stats[2] = modify_stats(item_name, 'endurance', stats[2], None)
		stats[3] = modify_stats(item_name, 'strength', stats[3], None)
		stats[4] = modify_stats(item_name, 'dexterity', stats[4], None)
		stats[5] = modify_stats(item_name, 'intelligence', stats[5], None)
		stats[6] = modify_stats(item_name, 'faith', stats[6], None)
		stats[7] = modify_stats(item_name, 'arcane', stats[7], None)

	return stats


print(apply_modifiers(stats, 1900, 69.9))
