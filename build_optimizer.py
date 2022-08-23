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

def API_pull(url_ext):
    data_frame = []
    response = requests.get("https://eldenring.fanapis.com/api" + str(url_ext)).text
    data = json.loads(response)
    data_frame.append(data)
    return data_frame

def write_json(classes = True, weapons = False):
    data_frame = []

    if classes:
        data_frame = API_pull("classes")

    if weapons:
        for page in range(16):
            data_frame += API_pull("weapons?page="+str(page))

    print(data_frame)

    for iter in range(pulls)
    with open('classes.json', 'w') as json_file:
        json.dump(data_frame, json_file)

def main():
    write_json()

main()
