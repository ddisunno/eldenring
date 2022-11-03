import simplejson as json

# KNOWN ISSUES:

# IF REMAINING WEIGHT EXCEEDS HIGHEST ARMOR TOTAL (64),
# OPTIMIZER PICKS PUMPKIN HELM OVER BULL-GOAT


# PICKS ARMOR BASED ON PROPORTIONS OF REMAINING WEIGHT (BASED ON WEIGHT = 64):
# WHETHER THESE PROPORTIONS ARE ACCURATE TO ALL REAMINING WEIGHTS IS UNCLEAR

# PROPORTIONS ARE AS FOLLOWS:
# HELM: 18%
# CHEST: 42%
# ARMS: 14%
# LEGS: 26%




########################################################################
def group_preferences(preferences: list, group: list, armor_data: dict):

	instances = 0
	pref_mod = 0

	for pref in preferences:
		if pref in group:
			instances += 1
			pref_mod += armor_data[pref]



	if instances != 0:
		avg_group_mod = pref_mod / instances
		group_count = 1
	else:
		avg_group_mod = 0
		group_count = 0

	return avg_group_mod, group_count


#################
def group_armor(avg_armor_val: float, armor_data: dict, armor_types: list):

	helms = {}
	chests = {}
	arms = {}
	legs = {}

	# create categories for armor type: unsorted dict {'armor_name': avg_armor_val}

	if armor_data['Category'] == "Helm":
		armor_types[0][armor_data['Name']] = avg_armor_val

	elif armor_data['Category'] == "Chest":
		armor_types[1][armor_data['Name']] = avg_armor_val

	elif armor_data['Category'] == "Arm":
		armor_types[2][armor_data['Name']] = avg_armor_val

	elif armor_data['Category'] == "Leg":
		armor_types[3][armor_data['Name']] = avg_armor_val

	return helms, chests, arms, legs


#################################
def rank_armor(armor_type: dict):

	# sort dictionary values; high - low

	armor_type_ranked = {}

	armor_values = sorted(armor_type, key=armor_type.get, reverse=True)

	for armor in range(len(armor_values)):
		armor_type_ranked[armor_values[armor]] = armor_type[armor_values[armor]]

	return armor_type_ranked


#################################################################################
def best_armor(armor_type_ranked: dict, remaining_weight: float, contents: dict):

	best_armor_weight = 0
	best_armor_poise = 0
	best_armor = ""

	ranking = 1

	for armor_type in armor_type_ranked:

		for armor in range(len(contents['data'])):
			armor_data = contents['data'][armor]
			
			if armor_data['Name'] == armor_type:
				print(f"{ranking}. {armor_type} {armor_type_ranked[armor_type]} {armor_data['Wgt.']}")
				ranking+=1

				# FIX THIS STATEMENT
				if armor_data['Wgt.'] <= remaining_weight and armor_data['Wgt.'] > best_armor_weight:

					best_armor = armor_data['Name']
					best_armor_weight = armor_data['Wgt.']
					best_armor_poise = armor_data['Poi.']

	
	return best_armor, best_armor_weight


##################################################################################
def optimize_armor_set(preferences: list, remaining_weight: float, in_set = list):

	armor_set_weight = 0
	armor_set = []

	for armor in in_set:

		if armor == "Helm":
			best_armor, best_armor_weight = optimize_armor(preferences, remaining_weight*0.18, armor)
		elif armor == "Chest":
			best_armor, best_armor_weight = optimize_armor(preferences, remaining_weight*0.42, armor)
		elif armor == "Arms":
			best_armor, best_armor_weight = optimize_armor(preferences, remaining_weight*0.14, armor)
		elif armor == "Legs":
			best_armor, best_armor_weight = optimize_armor(preferences, remaining_weight*0.26, armor)

		armor_set_weight += best_armor_weight
		armor_set.append(best_armor)

		#print(f"\t{armor_set_weight}/{remaining_weight}\t{best_armor}: {best_armor_weight}\n\n")

	print(f"\nOptimized Set:")
	for armor in armor_set:
		print(f"\t{armor}")
	print(f"\nweight: {armor_set_weight}/{remaining_weight}")

	return armor_set, armor_set_weight



################################### OPTIMIZE ARMOR
def optimize_armor(preferences: list, remaining_weight: float, optimize_for_type: str):
	with open('json/armors.json') as f:
		contents = json.load(f)

	groups = [['Phy','VS Str','VS Sla','VS Pie'],
			  ['Mag','Fir','Lit','Hol'],
			  ['Imm.','Rob.','Foc.','Vit.'],
			  ['Poi.']]

	helms = {}
	helms_ranked = {}

	chests = {}
	chests_ranked = {}

	arms = {}
	arms_ranked = {}

	legs = {}
	legs_ranked = {}

	armor_types = [helms, chests, arms, legs]


	for armor in range(len(contents['data'])):

		armor_data = contents['data'][armor]
		armor_val = 0
		instances = 0

		for group in groups:

			avg_group_mod, group_count = group_preferences(preferences, group, armor_data)
			armor_val += avg_group_mod
			instances += group_count

		avg_armor_val = armor_val / (instances * armor_data['Wgt.'])

		group_armor(avg_armor_val, armor_data, armor_types)


	helms_ranked = rank_armor(armor_types[0])
	chests_ranked = rank_armor(armor_types[1])
	arms_ranked = rank_armor(armor_types[2])
	legs_ranked = rank_armor(armor_types[3])

	if optimize_for_type == "Helm":
		best_helm, best_helm_weight = best_armor(helms_ranked, remaining_weight, contents)
		return best_helm, best_helm_weight

	elif optimize_for_type == "Chest":
		best_chest, best_chest_weight = best_armor(chests_ranked, remaining_weight, contents)
		return best_chest, best_chest_weight

	elif optimize_for_type == "Arms":
		best_arms, best_arms_weight = best_armor(arms_ranked, remaining_weight, contents)
		return best_arms, best_arms_weight

	elif optimize_for_type == "Legs":
		best_legs, best_legs_weight = best_armor(legs_ranked, remaining_weight, contents)
		return best_legs, best_legs_weight


#print(optimize_armor(preferences = ['Phy', 'VS Sla', 'Poi.'],remaining_weight = 45.0, optimize_for_type = "Chest"))

optimize_armor_set(['Poi.','Phy', 'VS Sla'], 31.455, ["Chest", "Legs", "Helm", "Arms"])
