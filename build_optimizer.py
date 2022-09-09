"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti
project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans)
    3. write build to .txt file
"""

import random

import requests
import time
import math
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

            response = requests.get(url[current]) # initial response; limit=20

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

                time.sleep(0.1) # don't spam

            data['count'] = len(data['data']) #change count from page total to file total

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


def get_random_weapon():
    with open('weapons.json') as f:
        data = json.load(f)

    weapon_index = random.randint(0,data['count'])

    weapon_name = data['data'][weapon_index]['name']

    return weapon_name


def optimal_class(weapon):
    """Function optimal_class finds the class that reaches weapon requirements earliest
    """

    with open('classes.json') as f:
        classes = json.load(f)
    
    if int(len(classes['data']) > 10):
        del classes['data'][13]
        del classes['data'][12]
        del classes['data'][11]
    
    # declare variables
    strength_diff = 0
    dexterity_diff = 0
    intelligence_diff = 0
    faith_diff = 0
    arcane_diff = 0
    current_lowest_level = 999
    best_class = []

    weapon_stats = dict()
    stat_names = {'Str':'strength',
                  'Dex':'dexterity',
                  'Int':'intelligence',
                  'Fai':'faith',
                  'Arc':'arcane'}

    for i in range(len(weapon['requiredAttributes'])): #for every req stat

        name   = stat_names[weapon['requiredAttributes'][i]['name']]
        amount = weapon['requiredAttributes'][i]['amount']
        weapon_stats[name] = amount # reformat weapon keys to match classes

    
    for i in range(classes['count']-3): # calculate best class

        if 'strength' in weapon_stats.keys():
            if int(weapon_stats['strength']) > int(classes['data'][i]['stats']['strength']):
                strength_diff = int(weapon_stats['strength']) - int(classes['data'][i]['stats']['strength'])
        if 'dexterity' in weapon_stats.keys():
            if int(weapon_stats['dexterity']) > int(classes['data'][i]['stats']['dexterity']):
                dexterity_diff = int(weapon_stats['dexterity']) - int(classes['data'][i]['stats']['dexterity'])
        if 'intelligence' in weapon_stats.keys():
            if int(weapon_stats['intelligence']) > int(classes['data'][i]['stats']['intelligence']):
                intelligence_diff = int(weapon_stats['intelligence']) - int(classes['data'][i]['stats']['intelligence'])
        if 'faith' in weapon_stats.keys():
            if int(weapon_stats['faith']) > int(classes['data'][i]['stats']['faith']):
                faith_diff = int(weapon_stats['faith']) - int(classes['data'][i]['stats']['faith'])
        if 'arcane' in weapon_stats.keys():
            if int(weapon_stats['arcane']) > int(classes['data'][i]['stats']['arcane']):
                arcane_diff = int(weapon_stats['arcane']) - int(classes['data'][i]['stats']['arcane'])

        class_level = strength_diff + dexterity_diff + intelligence_diff + faith_diff + arcane_diff + int(classes['data'][i]['stats']['level'])
        
        if class_level < current_lowest_level: # save the lowest level
            current_lowest_level = class_level
            best_class.append(classes['data'][i]['name'])

    
    print(f"\nOptimal Class(es) for {weapon['name']} is {best_class} at level: {current_lowest_level}\n")



get_data(url_list, pull = False)

optimal_class(fetch_from_json(f'{get_random_weapon()}','weapons.json'))

#optimal_class(fetch_from_json("Rivers Of Blood",'weapons.json'))

#rivers_of_blood = fetch_from_json('Rivers Of Blood','weapons.json')
#print(rivers_of_blood)
#optimal_class(rivers_of_blood)