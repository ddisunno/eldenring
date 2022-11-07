import simplejson as json
from tqdm import tqdm

# ELDEN RING ARMOR OPTIMIZER

# INPUTS

remaining_weight = 31.05
preferences = [['Poi.']]
omitted = []

# STEPS:

# FIND ALL COMBINATIONS THAT CAN BE USED WITH VAR: remaining_weight

# STORE THOSE COMBINATIONS WITH KEYS:
#	ARMOR IN SET:	HELM, CHEST, ARMS, LEGS (NAMES)
#	SET DATA:		SUM OF DATA IN SET
#			EX: 	SET POISE = (SUM OF POISE FOR ALL ARMOR IN SET)
#	

"""
armor_set_dict = {}

armor_set_dict['Phy'] = sum([helm['Phy'], chest['Phy'], arm['Phy'], leg['Phy']])
armor_set_dict['VS Str'] = sum([helm['VS Str'], chest['VS Str'], arm['VS Str'], leg['VS Str']])
armor_set_dict['VS Sla'] = sum([helm['VS Sla'], chest['VS Sla'], arm['VS Sla'], leg['VS Sla']])
armor_set_dict['VS Pie'] = sum([helm['VS Pie'], chest['VS Pie'], arm['VS Pie'], leg['VS Pie']])
armor_set_dict['Mag'] = sum([helm['Mag'], chest['Mag'], arm['Mag'], leg['Mag']])
armor_set_dict['Fir'] = sum([helm['Fir'], chest['Fir'], arm['Fir'], leg['Fir']])
armor_set_dict['Lit'] = sum([helm['Lit'], chest['Lit'], arm['Lit'], leg['Lit']])
armor_set_dict['Hol'] = sum([helm['Hol'], chest['Hol'], arm['Hol'], leg['Hol']])
armor_set_dict['Imm.'] = sum([helm['Imm.'], chest['Imm.'], arm['Imm.'], leg['Imm.']])
armor_set_dict['Rob.'] = sum([helm['Rob.'], chest['Rob.'], arm['Rob.'], leg['Rob.']])
armor_set_dict['Foc.'] = sum([helm['Foc.'], chest['Foc.'], arm['Foc.'], leg['Foc.']])
armor_set_dict['Vit.'] = sum([helm['Vit.'], chest['Vit.'], arm['Vit.'], leg['Vit.']])
armor_set_dict['Poi.'] = sum([helm['Poi.'], chest['Poi.'], arm['Poi.'], leg['Poi.']])
armor_set_dict['Wgt.'] = sum([helm['Wgt.'], chest['Wgt.'], arm['Wgt.'], leg['Wgt.']])

armor_sets.append(armor_set_dict)
"""



def split_by_category(file: str, remaining_weight: float, omitted: list):
	"""Function split_by_category takes every armor out of armors.json,
	and puts each piece in it's associated list by armor type,
	while omitting armor that cannot be used on its own,
	OR in conjunction with the lightest pieces in all other categories

	inputs:
		file - the file to split into categories (includes pathing)
		remaining_weight - the amount of weight a user can allocate to equipping armor

	outputs:
		helms, chests, arms, legs - lists of equippable armor grouped into armor type
	"""

	helms = []
	chests = []
	arms = []
	legs = []

	lightest_helm = 99
	lightest_chest = 99
	lightest_arm = 99
	lightest_leg = 99

	##################################
	# READ IN CONTENTS OF ARMOR DATA #

	with open(file) as f:
		contents = json.load(f)

	##########################
	# SEPARATE ARMOR BY TYPE #

	for armor in range(len(contents['data'])):

		armor_data  = contents['data'][armor]

		if armor_data['Category'] == "Helm" and armor_data['Wgt.'] < remaining_weight:
			helms.append(armor_data)

			if armor_data['Wgt.'] < lightest_helm:
				lightest_helm = armor_data['Wgt.']

		elif armor_data['Category'] == "Chest" and armor_data['Wgt.'] < remaining_weight:
			chests.append(armor_data)

			if armor_data['Wgt.'] < lightest_chest:
				lightest_chest = armor_data['Wgt.']

		elif armor_data['Category'] == "Arm" and armor_data['Wgt.'] < remaining_weight:
			arms.append(armor_data)

			if armor_data['Wgt.'] < lightest_arm:
				lightest_arm = armor_data['Wgt.']

		elif armor_data['Category'] == "Leg" and armor_data['Wgt.'] < remaining_weight:
			legs.append(armor_data)

			if armor_data['Wgt.'] < lightest_leg:
				lightest_leg = armor_data['Wgt.']

	# REMOVE ITEMS IF THEY CAN'T BE WORN IN A FULL SET OF LIGHTEST COMBINATIONS

	heaviest_helm = remaining_weight - (lightest_chest + lightest_arm + lightest_leg)
	heaviest_chest = remaining_weight - (lightest_helm + lightest_arm + lightest_leg)
	heaviest_arm = remaining_weight - (lightest_helm + lightest_chest + lightest_leg)
	heaviest_leg = remaining_weight - (lightest_helm + lightest_chest + lightest_arm)

	for armor in helms:
		if armor['Wgt.'] > heaviest_helm:
			helms.pop(armor)

	for armor in chests:
		if armor['Wgt.'] > heaviest_chest:
			chests.remove(armor)

	for armor in arms:
		if armor['Wgt.'] > heaviest_arm:
			arms.remove(armor)

	for armor in legs:
		if armor['Wgt.'] > heaviest_leg:
			arms.remove(armor)



	return helms, chests, arms, legs



def merge_dicts(cat_1: list, cat_2: list, remaining_weight: float):

	merged = []

	print(f"Testing all combinations of: ()")
	for iter_1 in tqdm(cat_1):
		for iter_2 in cat_2:

			armor_set_dict = {}
			names = {}

			# TURN NAME INTO DICT FOR SET: {'Name' : {'Helm: (name), 'Chest': (name)}

			if type(iter_1['Name']) != dict and type(iter_2['Name']) != dict:

				names[iter_1['Category']] = iter_1['Name']
				names[iter_2['Category']] = iter_2['Name']

				armor_set_dict['Name'] = names

			elif type(iter_1['Name']) == dict and type(iter_2['Name']) != dict:

				for category in iter_1['Name']:
					names[category] = iter_1['Name'][category]

				names[iter_2['Category']] = iter_2['Name']

				armor_set_dict['Name'] = names

				#print(armor_set_dict['Name'])


			"""
			if 'Name' in iter_1.keys():
				armor_set_dict[iter_1['Category']] = iter_1['Name']

			if 'Name' in iter_2.keys():
				armor_set_dict[iter_2['Category']] = iter_2['Name']
			"""

			for key in iter_1.keys():

				if key in ['In-Game Section', 'Category', 'Name', 'Helm', 'Chest', 'Arm', 'Leg', 'Rank']:
					pass

				else:
					armor_set_dict[key] = sum([iter_1[key], iter_2[key]])

			# conditional; if item is worse: pass (weight > heaviest_inset and pref < heaviest_inset)

			if armor_set_dict['Wgt.'] <= remaining_weight:
				merged.append(armor_set_dict)

	return merged


def optimize_set(armor_set: list, preferences: list, percentile: int):
	"""Function clean_data culls unwanted values from list of armor dictionaries
	before further iterating further combinations.
	inputs:
		armor_set: list of armor
		preferences: list of preferences (grouped by category)
		percentile: all values above (x)% where percentile is to be x


	All possible combinations of armor in eldenring total to 355,147,416,
	and generating a list of 355 million dictionaries would overload my CPU.
	Furthermore, run time needs to be reduced to ~10 seconds"""

	armor_vals = []

	for armor in armor_set:

		pref_total = 0

		for group in preferences:
			group_total = 0

			for pref in group:
				group_total += armor[pref]

			group_avg = group_total / len(group)
			pref_total += group_avg

		pref_avg = pref_total / len(preferences)

		armor['Rank'] = pref_avg


	ranked_sets = sorted(armor_set, key=lambda d: d['Rank'], reverse = True)

	"""
	percentile = (100-percentile)/100
	above_percentile = ranked_sets[0:round(len(ranked_sets)*percentile)]
	"""

	# create a list of unique armor values (1 for each that exists)

	for armor in ranked_sets:
		if armor['Rank'] not in armor_vals:
			armor_vals.append(armor['Rank'])


	best_per_val = []

	for val in armor_vals:
		val_lightest = 99

		for armor in ranked_sets:
			if armor['Rank'] == val and armor['Wgt.'] < val_lightest:
				val_lightest = armor['Wgt.']
				best_armor = armor

		best_per_val.append(best_armor)


	return best_per_val

def armor_opt(remaining_weight: float, preferences: list, omitted: list):

	helms, chests, arms, legs = split_by_category('json/armors.json', remaining_weight, omitted)

	chests_legs = merge_dicts(chests, legs, remaining_weight)
	chests_legs_opt = optimize_set(chests_legs, preferences, 85) # add another function to clean data before further iterations

	chests_legs_helms = merge_dicts(chests_legs_opt, helms, remaining_weight)
	chests_legs_helms_opt = optimize_set(chests_legs_helms, preferences, 85)

	armor_sets = merge_dicts(chests_legs_helms_opt, arms, remaining_weight)
	armor_sets_opt = optimize_set(armor_sets, preferences, 85)

	return armor_sets_opt[0]


print(armor_opt(remaining_weight, preferences, omitted))


