import simplejson as json


def fetch_from_json(item, file):
    """Function fetch_from_data finds an item in a file
    -----
        inputs:
            item    - thing to find
            file    - file to search
        outputs:
            item_info   - all item data from json
    """
    with open(file) as f:
        data = json.load(f)
    
    for i in range(data['count']):

        if item in data['data'][i]['name']:
            item_index = i

        """ PRINTS NAME + REQ ATTRIBUTES FOR ALL DATA
        print(f"{data['data'][i]['name']}\
            \n\t{data['data'][i]['requiredAttributes']}")
        """

    item_info = data['data'][item_index]

    """ PRINTS NAME + REQ ATTRIUBTES FOR SPECIFIC DATA
    print(f"{data['data'][item_index]['name']}\
            \n\t{data['data'][item_index]['requiredAttributes']}")
    """
    
    return item_info

jar_cannon = fetch_from_json('Jar Cannon','weapons.json')
banished_knight_armor = fetch_from_json('Banished Knight Armor','armors.json')

print(jar_cannon)
print(banished_knight_armor)