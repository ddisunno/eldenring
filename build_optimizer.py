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

        for current in tqdm(range(len(url))): #iterate every url

            response = requests.get(url[current]) # initial response limit=20

            limit = response.json()['total'] # total number of entries
            domain_path = url[current][34:] # https://eldenring.fanapis.com/api/...

            full_response = requests.get(f"{url[current]}?limit={limit}") # set response limit=limit
            data = full_response.json() # all the data


            with open(f'{domain_path}.json', 'w') as f:
                json.dump(data,f)

            
            time.sleep(0.3)


get_data(url_list, pull = False)