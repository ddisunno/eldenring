## Optimize Armor
import simplejson as json


# category: Helm, Chest Armor, Gauntlets, Leg Armor


def rank_armor(optimize_for):
	""" Function optimize_armor

	"""

	with open('json/armors.json') as f:
		contents = json.load(f)


	helms = {}
	helms_ranked = {}

	chests = {}
	chests_ranked = {}

	arms = {}
	arms_ranked = {}

	legs = {}
	legs_ranked = {}



	for armor in range(len(contents['data'])):

		value_mod = 0

		name = contents['data'][armor]['Name']

		physical = contents['data'][armor]['Phy']
		strike = contents['data'][armor]['VS Str']
		slash = contents['data'][armor]['VS Sla']
		pierce = contents['data'][armor]['VS Pie']
		dmgNegation = [physical, strike, slash, pierce]

		magic = contents['data'][armor]['Mag']
		fire = contents['data'][armor]['Fir']
		lightning = contents['data'][armor]['Lit']
		holy = contents['data'][armor]['Hol']
		eleNegation = (magic + fire + lightning + holy) / 4

		immunity = contents['data'][armor]['Imm.']
		robustness = contents['data'][armor]['Rob.']
		focus = contents['data'][armor]['Foc.']
		vitality = contents['data'][armor]['Vit.']
		resistance = (immunity + robustness + focus + vitality) / 4

		poise = contents['data'][armor]['Poi.']

		weight = contents['data'][armor]['Wgt.']




		# var_dict to optimize off vars in optimize_for

		var_dict = {'Phy': physical,
				'VS Str': strike,
				'VS Sla': slash,
				'VS Pie': pierce,
				'dmgNegation': dmgNegation,
				'Mag': magic,
				'Fir': fire,
				'Lit': lightning,
				'Hol': holy,
				'eleNegation': eleNegation,
				'Imm.': immunity,
				'Rob.': robustness,
				'Foc.': focus,
				'Vit.': vitality,
				'resistance': resistance,
				'Poi.': poise}	

		dmgNegation_tally = 0
		eleNegation_tally = 0
		resistance_tally = 0

		for var in optimize_for:

			if var in dmgNegation:
				dmgNegation_tally += 1
				value_mod += var_dict[var]

			elif var == 'dmgNegation':


			value_mod += var_dict[var]
		
		value = value_mod/(weight*len(optimize_for))


		# create categories for armor type: unsorted dict {'armor_name': value}

		if contents['data'][armor]['Category'] == "Helm":
			helms[name] = value

		elif contents['data'][armor]['Category'] == "Chest":
			chests[name] = value

		elif contents['data'][armor]['Category'] == "Arm":
			arms[name] = value

		elif contents['data'][armor]['Category'] == "Leg":
			legs[name] = value


	# sort dictionary values; high - low

	helm_values = sorted(helms, key=helms.get, reverse=True)
	chest_values = sorted(chests, key=chests.get, reverse=True)
	arm_values = sorted(arms, key=arms.get, reverse=True)
	leg_values = sorted(legs, key=legs.get, reverse=True)


	# create new dictionaries with {armor_name: sorted_values}

	for armor in range(len(helm_values)):
		helms_ranked[helm_values[armor]] = helms[helm_values[armor]]

	for armor in range(len(chest_values)):
		chests_ranked[chest_values[armor]] = chests[chest_values[armor]]

	for armor in range(len(arm_values)):
		arms_ranked[arm_values[armor]] = arms[arm_values[armor]]

	for armor in range(len(leg_values)):
		legs_ranked[leg_values[armor]] = legs[leg_values[armor]]




	return helms_ranked, chests_ranked, arms_ranked, legs_ranked
	

helms_ranked, chests_ranked, arms_ranked, legs_ranked = (rank_armor(optimize_for = ['Poi.', 'dmgNegation', 'eleNegation', 'resistance']))



