'''
Author: Rudy DeSanti
Last Modified: September 29, 2022
Description: This file hold helper methods for the web server. This consists of getting information from json/csv files and python files.
'''
import json
import weaponOptimizer 
import calcWeaponAR

#Get if a weapon can have affinities based off of type. *move to CALCweaponAR.py*
def canHaveAffinities(weaponName):
    somber = weaponOptimizer.isSomber(weaponName)
    type = calcWeaponAR.getWeaponType(weaponName) 

    if(somber or type == 'Bow' or type == 'Light Bow' or type == 'Greatbow' or type == 'Glintstone Staff' or type == 'Sacred Seal' or type == 'Crossbow'):
        return False
    else:
        return True

#Return a list of strings of each weapon name in the weapons.json file and if the weapon is somber. 
def getWeaponNames():
    weaponNames = []
    with open('json/weapons.json','r') as f:
        data = json.load(f)
        for weapon in data['data']:
            somber = not canHaveAffinities(weapon['name'])
            weaponNames.append({'name':weapon['name'], 'somber':somber, 'affinity':""})

    weaponNames.sort(key=lambda x: x['name'])
    return json.dumps(weaponNames)

#Main Function- Based on the json from the server, handle the GET/POST request and call the appropriate methods.
def handleType(data):
    if(data['type'] == 'getWeaponNames'):
        return getWeaponNames()
    else:
        return None
