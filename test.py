# challenge: 
# find the mean from a selection of averages from one pool of data

one = 1
two = 2
three = 3
a = 10
b = 20
c = 30
do = 100
re = 200
mi = 300

denom = 6

# GIVEN data:
data = {'one': one,
		'two': two,
		'three': three,
		'a': a,
		'b': b,
		'c': c,
		'do': do,
		're': re,
		'mi': mi,
		'denom': denom}

# write a function that allows users to find an average from a selection
# such that the selection is of groups (a,b,c)(one,two,three)(do,re,mi)

oneTwoThree = ['one','two','three']
abc = ['a','b','c']
doReMi = ['do','re','mi']

# ex:
# ((one+two)/2) / denom
# ((one+two+three)/3) / denom
# (((one+two+three)/3) + ((a+b)/2) + ((do)/1) / denom)


###### CODE BEGINS HERE ######
def avg_from_selection(selection: list):

	oneTwoThree_counter = 0
	oneTwoThree_mod = 0

	abc_counter = 0
	abc_mod = 0

	doReMi_counter = 0
	doReMi_mod = 0

	for var in selection:

		if var in oneTwoThree:
			oneTwoThree_counter += 1
			oneTwoThree_mod += data[var]
			
		if var in abc:
			abc_counter += 1
			abc_mod += data[var]
			
		if var in doReMi:
			doReMi_counter += 1
			doReMi_mod += data[var]

	if oneTwoThree_counter != 0:
		avg_oneTwoThree = oneTwoThree_mod / oneTwoThree_counter
	else:
		avg_oneTwoThree = 0
	if abc_counter != 0:
		avg_abc = abc_mod / abc_counter
	else:
		avg_abc = 0
	if doReMi_counter != 0:
		avg_doReMi = doReMi_mod / doReMi_counter
	else: avg_abc = 0


avg_from_selection(['one','two','a','b','c'])

