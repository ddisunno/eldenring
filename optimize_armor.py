## Optimize Armor
import simplejson as json


# category: Helm, Chest Armor, Gauntlets, Leg Armor


def optimize_armor(remaining_weight, optimize_for):
	""" Function optimize_armor

	"""

	with open('json/armors.json') as f:
		contents = json.load(f)


	helms = {}
	surcoats = {}
	gauntlets = {}
	greaves = {}

	for armor in range(len(contents['data'])):
		name = contents['data'][armor]['Name']
		poise = contents['data'][armor]['Poi.']
		weight = contents['data'][armor]['Wgt.']

		value = poise/weight

		if contents['data'][armor]['Category'] == "Helm":
			helms[name] = value

		elif contents['data'][armor]['Category'] == "Chest":
			surcoats[name] = value

		elif contents['data'][armor]['Category'] == "Arm":
			gauntlets[name] = value

		elif contents['data'][armor]['Category'] == "Leg":
			greaves[name] = value

		#print(f"{contents['data'][armor]['name']}: {value}")

	helms_by_value = sorted(helms, key=helms.get, reverse=True)
	surcoats_by_value = sorted(surcoats, key=surcoats.get, reverse=True)
	gauntlets_by_value = sorted(gauntlets, key=gauntlets.get, reverse=True)
	greaves_by_value = sorted(greaves, key=greaves.get, reverse=True)


	print(f"\n\nHelmets: ")
	for armor in range(len(helms_by_value)):
		print(f"\t{armor}. {helms_by_value[armor]}: {helms[helms_by_value[armor]]}")

	print(f"\n\nSurcoats: ")
	for armor in range(len(surcoats_by_value)):
		print(f"\t{armor}. {surcoats_by_value[armor]}: {surcoats[surcoats_by_value[armor]]}")

	print(f"\n\nGauntlets: ")
	for armor in range(len(gauntlets_by_value)):
		print(f"\t{armor}. {gauntlets_by_value[armor]}: {gauntlets[gauntlets_by_value[armor]]}")

	print(f"\n\nGreaves: ")
	for armor in range(len(greaves_by_value)):
		print(f"\t{armor}. {greaves_by_value[armor]}: {greaves[greaves_by_value[armor]]}")



optimize_armor(remaining_weight = 50, optimize_for = 'poise')