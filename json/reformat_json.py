# tool for reformatting json files

"""
reformatting weapons.json:

"requiredAttributes": [
        {
          "name": "Str",
          "amount": 9
        },
        {
          "name": "Dex",
          "amount": 8
        }
    ]

"requiredAttributes": {
       	  "strength": 9
        },
        {
          "dexterity": 8
        }
    }

"""


import simplejson as json


############################
def read_in_file(file: str):

	with open(file) as f:
		contents = json.load(f)

	return contents


###########################################
def reformat_attributes(contents, att_key):

	for item in range(contents['count']):

		my_dict = {} # initialize and prevent stats from carrying over

		for attribute in range(len(contents['data'][item][att_key])):

			att_name = contents['data'][item][att_key][attribute]['name']
			att_amount = contents['data'][item][att_key][attribute]['amount']

			if att_name == "Str":
				strength = att_amount
				my_dict["strength"] = strength
			if att_name == "Dex":
				dexterity = att_amount
				my_dict["dexterity"] = dexterity
			if att_name == "Int" or att_name == "Intelligence":
				intelligence = att_amount
				my_dict["intelligence"] = intelligence
			if att_name == "Fai" or att_name == "Faith":
				faith = att_amount
				my_dict["faith"] = faith
			if att_name == "Arc" or att_name == "Arcane":
				arcane = att_amount
				my_dict["arcane"] = arcane
		
		# rename different attribute_keys to unanimous "requiredAttributes"
		contents['data'][item]['requiredAttributes'] = my_dict

		# we don't need duplicates
		if att_key != "requiredAttributes":
			contents['data'][item][att_key].pop()
		
		print(contents['data'][item]['name'], my_dict)

	return contents


###################################
def write_new_json(file, contents):

	## NAMING SCHEME
	numbers = ["1","2","3","4","5","6","7","8","9","10"]
	zero = "0"

	file_name = file[:len(file)-5] # remove the extension
	last_char = file_name[-1] # last character of file [str(char), str(num), str(0)]

	if last_char not in numbers and last_char != zero:
		new_file = file_name + "1.json"

	elif last_char in numbers:
		next_num = numbers[numbers.index(file_name[-1]) + 1]
		new_file = file_name[:len(file_name)-1] + next_num + ".json"

	elif last_char == zero:
		new_file = file_name[:len(file_name)-1] + "1.json"
	##
	
	## WRITE INTO FILE
	with open(new_file, 'w') as f:
		json.dump(contents, f, indent=2)


#####################################
def extract_poise(contents, att_key):

	for item in range(contents['count']):
		item_name = contents['data'][item]['name']
		resistance = contents['data'][item][att_key]
		poise = resistance[len(resistance)-1]

		poise_dict = {"poise": poise['amount']}
		contents['data'][item]['poise'] = poise['amount']
		contents['data'][item][att_key].remove(poise)

	return contents


########################
def main(file, att_key):

	contents = read_in_file(file)

	#ref_contents = reformat_attributes(contents, att_key)
	ref_contents = extract_poise(contents, att_key)

	write_new_json(file, ref_contents)


main('armors.json', 'resistance')
