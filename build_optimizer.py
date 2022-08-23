"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti

project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans)
    3. write build to .txt file
"""

import requests
import pandas as pd
import simplejson as json

def API_pull(classes = True, weapons = False):
    data_frame = []

    if classes:
        classes_url = "https://eldenring.fanapis.com/api/classes"
        response = requests.get(classes_url).text
        classes_data = json.loads(response)
        data_frame.append(classes_data)

    if weapons:
        for iter in range(16):
            weapons_url = "https://eldenring.fanapis.com/api/weapons?page="+str(iter)
            response = requests.get(weapons_url).text
            weapon_data = json.loads(response)
            data_frame.append(weapon_data)

    print(data_frame)

    with open('classes.json', 'w') as json_file:
        json.dump(data_frame, json_file)

def main():
    API_pull()

main()
