"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti
project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans)
    3. write build to .txt file
"""

import requests
import time
import simplejson as json
from tqdm import tqdm


url_list = ["https://eldenring.fanapis.com/api/classes",
            "https://eldenring.fanapis.com/api/weapons",
            "https://eldenring.fanapis.com/api/armors",
            "https://eldenring.fanapis.com/api/ashes"]



def get_data(url, pull):
    """Function get_data pulls data down from the API to local saves with .json extension
    -----
        inputs:
            url     - a list of urls for API calls
            pull    - a boolean condition determines if the function should execute
        outputs:
            generates/updates json files for each inputted url
    """
    if pull:

        print(f"Creating json files from eldenring.fanapis.com/api/")

        for current in range(len(url)): #iterate every url

            response = requests.get(url[current]) # initial response limit=20
            print(response) # did it work? (200)

            pages = math.ceil(response.json()['total']/20) # total number of pages

            domain_path = url[current][34:] # https://eldenring.fanapis.com/api/...
            print(f"Downloading {pages} pages of {domain_path}")

            for page in tqdm(range(pages)):
                if page == 0: #For First Page include metadata
                    page_response = requests.get(f"{url[current]}?page={page}")
                    data = page_response.json()
                else: # For all concurrent pages omit metadata
                    page_response = requests.get(f"{url[current]}?page={page}")
                    data['data'].extend(page_response.json()['data'])

                time.sleep(0.1)

            with open(f'{domain_path}.json', 'w') as f:
                json.dump(data,f, indent=2)

            
            time.sleep(0.3)



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

        #if item matches name
        if item in data['data'][i]['name']:
            item_index = i


    item_info = data['data'][item_index]   
    return item_info


def optimal_class(weapon):
    """Function optimal_class finds the class that reaches weapon requirements earliest

    """

    with open('classes.json') as f:
        classes = json.load(f)

    for j in range(len(weapon['requiredAttributes'])):
        print(weapon['requiredAttributes'][j])

        attribute   = weapon['requiredAttributes'][j]['name']
        required    = weapon['requiredAttributes'][j]['amount']

    """
    for i in range(classes['count']):
        print(f"{classes['data'][i]['name']}\
            \n\t{classes['data'][i]['stats']}")
    """




get_data(url_list, pull = False)


jar_cannon = fetch_from_json('Hand Axe','weapons.json')
print(jar_cannon)

optimal_class(jar_cannon)


