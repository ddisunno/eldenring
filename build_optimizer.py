"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti
project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans)
    3. write build to .txt file
"""

#import time
#import progressbar

import requests
import pandas as pd
import simplejson as json

# WRITE JSONS FROM API DATA

def API_pull(classes = True, weapons = True, armors = True):
    if classes:
        write_json('classes', 1)

    if weapons:
        write_json("weapons", 16)

    if armors:
        write_json("armors", 29)

def write_json(item, pages):
    data_frame = []

    for iter in range(pages):
        url = "https://eldenring.fanapis.com/api/" + item +'?page='+ str(iter)
        response = requests.get(url).text
        data = json.loads(response)
        data_frame.append(data)

    with open(item + '.json', 'w') as json_file:
        json.dump(data_frame, json_file)

# WEAPON STATS

def data_test(source):
    with open(source) as f:
        weapons_pool = json.load(f)

    print(type(weapons_pool['data']))
    
    #print(weapons_pool)


def main():
    API_pull()
    data_test("weapons.json")

main()
