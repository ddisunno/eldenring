# iterate through a list of values,
# and save one item in a dictionary with the least weight for each value

vals_list = [1,2,3,4,5]

items = [{"Title": "A", "Rank": 1, "Wgt.": 5},
		 {"Title": "B", "Rank": 1, "Wgt.": 3},
		 {"Title": "C", "Rank": 2, "Wgt.": 1},
		 {"Title": "D", "Rank": 2, "Wgt.": 3},
		 {"Title": "E", "Rank": 2, "Wgt.": 1},
		 {"Title": "F", "Rank": 3, "Wgt.": 2},
		 {"Title": "G", "Rank": 4, "Wgt.": 1},
		 {"Title": "H", "Rank": 4, "Wgt.": 5},
		 {"Title": "I", "Rank": 5, "Wgt.": 3},
		 {"Title": "J", "Rank": 5, "Wgt.": 4},
		 {"Title": "K", "Rank": 1, "Wgt.": 1}]

""" Winners:
RANK 1: B
RANK 2: C/E
RANK 3: F
RANK 4: G
RANK 5: I
"""


best_items = []

for val in vals_list:
	val_lightest = 99
	for item in items:
		if item['Rank'] == val and item['Wgt.'] < val_lightest:
			best_item = item
			val_lightest = item['Wgt.']

	best_items.append(best_item)

for item in best_items:
	print(item)




