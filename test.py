# challenge: 
# find the mean from a selection of averages from one pool of data

# DATA
import simplejson as json

with open('json/armors.json') as f:
	contents = json.load(f)

# INSTRUCTIONS:

# WRITE A FUNCTION THAT CALCULATES THE MEAN OF CALCULATED MEANS

# IE:
# GROUPS:

# A: ['Poi.']
# B: ['Phy', 'VS Str', 'VS Sla', 'VS Pie']
# C: ['Hol', 'Fir', 'Lit', 'Mag']
# D: ['Imm.', 'Rob.', 'Foc', 'Vit.']

# The function should calculate the average of a group,
# (ex: ('Phy' + 'VS Str') / 2)

# then calculate the average of the group averages.
# (ex: ([{'Phy' + 'VS Str'}/2] + [{'Poi.'}/1)])/2)

###### CODE BEGINS HERE ######
def avg_from_selection(preferences: list):

	pref_total = 0

	for group in preferences:
		group_total = 0

		for pref in group:
			group_total += armor_data[pref]

		group_avg = group_total / len(group)
		pref_total += group_avg

	pref_avg = pref_total / len(preferences)

	return pref_avg


######### UNCOMMENT FOR TESTING ##########
for armor in range(len(contents['data'])):
	armor_data = contents['data'][armor]

	# test 
	print(f"{armor_data['Name']}: {armor_data['Poi.']}/{avg_from_selection([['Poi.']])}")
	print(f"{armor_data['Name']}: {(armor_data['Poi.'] + armor_data['Phy'])/2}/{avg_from_selection([['Poi.'],['Phy']])}")
	print(f"{armor_data['Name']}: {((armor_data['Poi.']/1) + ((armor_data['Phy'] + armor_data['VS Sla'])/2))/2 }/{avg_from_selection([['Poi.'],['Phy','VS Sla']])}")
