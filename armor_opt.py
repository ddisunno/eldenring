import simplejson as json
from tqdm import tqdm

# ELDEN RING ARMOR OPTIMIZER

# INPUTS

remaining_weight = 31.05
preferences = [['Poi.']]

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



def split_by_category(file: str, remaining_weight: float):

	helms = []
	chests = []
	arms = []
	legs = []

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
		elif armor_data['Category'] == "Chest" and armor_data['Wgt.'] < remaining_weight:
			chests.append(armor_data)
		elif armor_data['Category'] == "Arm" and armor_data['Wgt.'] < remaining_weight:
			arms.append(armor_data)
		elif armor_data['Category'] == "Leg" and armor_data['Wgt.'] < remaining_weight:
			legs.append(armor_data)

	return helms, chests, arms, legs



def merge_dicts(cat_1: list, cat_2: list, preferences: list, remaining_weight: float):

	merged = []

	print(f"Testing all combinations of: ()")
	for iter_1 in tqdm(cat_1):
		for iter_2 in cat_2:

			armor_set_dict = {}

			if 'Name' in iter_1.keys():
				armor_set_dict[iter_1['Category']] = iter_1['Name']

			if 'Name' in iter_2.keys():
				armor_set_dict[iter_2['Category']] = iter_2['Name']

			for key in iter_1.keys():

				if key in ['In-Game Section', 'Category', 'Name', 'Helm', 'Chest', 'Arm', 'Leg']:
					pass

				else:
					armor_set_dict[key] = sum([iter_1[key], iter_2[key]])

			if armor_set_dict['Wgt.'] <= remaining_weight:
				merged.append(armor_set_dict)

	return merged


helms, chests, arms, legs = split_by_category('json/armors.json', remaining_weight)


chests_legs = merge_dicts(chests, legs, preferences, remaining_weight)
chests_legs_helms = merge_dicts(chests_legs, helms, preferences, remaining_weight)
armor_sets = merge_dicts(chests_legs_helms, arms, preferences, remaining_weight)

print(f"{sum([len(helms),len(chests),len(arms),len(legs)])}/578")
print(f"{len(chests_legs)}/22,356")
print(f"{len(chests_legs_helms)}/3,778,164")
print(f"{len(armor_sets)}/355,147,416")

"""
pref_total = 0

for group in preferences:
	group_total = 0

	for pref in group:
		group_total += armor_data[pref]

	group_avg = group_total / len(group)
	pref_total += group_avg

pref_avg = pref_total / len(preferences)
"""




