"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti
project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans) (armor, talismans)
    3. write build to .txt file
"""

import requests
import pandas as pd
import simplejson as json


def API_pull(classes, weapons, armors):
    if classes:
        write_json('classes', 1)

    if weapons:
        write_json("weapons",16)

    if armors:
        write_json('armors',29)
            
def write_json(item, pages):
    data_frame = []
    
    for iter in range(pages):
        url = "https://eldenring.fanapis.com/api/" + item +'?page='+ str(iter)
        response = requests.get(url).text
        data = json.loads(response)
        data_frame.append(data)
    
    with open('eldenring/APIjsons/' + item + '.json', 'w') as json_file:
        json.dump(data_frame, json_file)

def main():
    API_pull(True, True, True)

main()