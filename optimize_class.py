##### INITIALIZE LIBRARIES / DATA #####
import json
from get_requirements import get_requirements as get_reqs
#import simplejson as json

"""
roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}
##### BEGIN: UI INPUTS #####
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
			   "file": "talismans.json"},
			  {"name": "Great-jar's Arsenal",
			   "file": "talismans.json"},
			  {"name": "Radagon Icon",
			   "file": "talismans.json"}]
desired_health = 0
current_roll_type = roll_type['med']
##### END: UI INPUTS #####
print(req_stats)
req_stats = get_reqs(items_list, desired_health, current_roll_type)
"""

##### begin code #####
def get_base_stats(classes_index):
	"""Function get_base_stats
	inputs:
		classes_index - index of class to pull
	outputs:
		class_name - name of the class at given index
		base_level - level of the class at given index
		base_stats - list[vigor,mind,endurance,strength,dexterity,intelligence,faith,arcane]
	"""
	with open('json/classes.json') as f:
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
	"""Function optimize_class takes a list of items and picks the lowest class that
	can use ALL of them INDIVIDUALLY with desired roll_type and HP
	inputs:
		items_list - list of items in dictionary form containing ['name'] - name of the item
																 ['file'] - file the item can be found in
		desired_health - amount of health to exceed on character
		roll_type - desired roll type from dictionary (multiplier for total equip load)
	outputs:
		best_class - name of the best class (able to use everything with the lowest level)
		lowest_level - level of the best class
		best_stats - list of stats of the best class [vig,min,end,str,dex,int,fai,arc]
	"""

	#LIST FORM
	item_reqs = []

	needed_stats = [0,0,0,0,0,0,0,0] #NEEDED STATS = REQUIRED STATS - BASE STATS
	current_stats = [0,0,0,0,0,0,0,0] #CURRENT STATS = BASE STATS + NEEDED STATS

	#TO PICK WINNER
	lowest_level = 713 # max level is 713
	best_class = ""
	best_stats = []


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
			
	"""
	print(f"best class is:\
		\n\t{best_class}: {lowest_level}\
		\n\t{best_stats}")
	"""

	return best_class, lowest_level, best_stats


#optimize_class(req_stats)