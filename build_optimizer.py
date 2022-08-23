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

weapons_url = "https://eldenring.fanapis.com/api/weapons"

response = requests.get(weapons_url)
print(response)

weapon_data = json.loads(response.json)
data_frame = pd.DataFrame.from_dict(weapon_data)
print(data_frame)




"""with open('weapons.json', 'w') as json_file:
    json.dump(response, json_file)"""
