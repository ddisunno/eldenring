'''
Author: Rudy DeSanti
Last Modified: September 29, 2022
Description: This file hold helper methods for the web server. This consists of getting information from json/csv files and python files.
'''
import json
import weaponOptimizer 
import calcWeaponAR
#import build_optimizer

#Get if a weapon can have affinities based off of type. *move to CALCweaponAR.py*
def canHaveAffinities(weaponName):
    somber = weaponOptimizer.isSomber(weaponName)
    type = calcWeaponAR.getWeaponType(weaponName) 

    if(somber or type == 'Bow' or type == 'Light Bow' or type == 'Greatbow' or type == 'Glintstone Staff' or type == 'Sacred Seal' or type == 'Crossbow'):
        return False
    else:
        return True

#Return a list of strings of each weapon name in the weapons.json file and if the weapon is somber. 
def getWeapons():
    standard = []
    somber = []
    with open('json/weapons.json','r') as f:
        data = json.load(f)
        for weapon in data['data']:
            somberBool = not canHaveAffinities(weapon['name'])
            if(somberBool):
                somber.append({'name':weapon['name'], 'somber':True, 'affinity':"", 'pngUrl':weapon['image'], 'isPow':False})
            else:
                standard.append({'name':weapon['name'], 'somber':False, 'affinity':"", 'pngUrl':weapon['image'], 'isPow':False})
    somber.sort(key=lambda x: x['name'])
    standard.sort(key=lambda x: x['name'])
    return json.dumps({'standard':standard, 'somber':somber})

def getArmor(category):
    armors = []
    with open('json/armors.json','r') as f:
        data = json.load(f)
        for armor in data['data']:
            if(armor['category'] == category):
                armors.append({'name':armor['name'], 'poise':armor['resistance'][4]['amount'], 'weight':armor['weight'], 'pngUrl':armor['image']})

    armors.sort(key=lambda x: x['name'])
    return json.dumps(armors)

def getTalismans():
    names = []
    with open('json/talismans.json','r') as f:
        data = json.load(f)
        for talisman in data['data']:
            names.append({'name':talisman['name'], 'pngUrl':talisman['image'], 'effect':talisman['effect']})

    names.sort(key=lambda x: x['name'])
    return json.dumps(names)

def getSpells():
    names = []
    with open('json/spells.json','r') as f:
        data = json.load(f)
        for talisman in data['data']:
            names.append({'name':talisman['name'], 'pngUrl':talisman['image'], 'type':talisman['type'], 'effect':talisman['effects'], 'cost':talisman['cost'], 'slots':talisman['slots']})

    names.sort(key=lambda x: x['name'])
    return json.dumps(names)

def getBuild(build):
    return "hi"
    #return json.loads(build_optimizer.optimize_build(build))

#Main Function- Based on the json from the server, handle the GET/POST request and call the appropriate methods.
def handleType(data):
    if(data['type'] == 'getWeaponNames'):
        return getWeapons()
    elif(data['type'] == 'getArmor'):
        return getArmor(data['category'])
    elif(data['type'] == 'getTalismans'):
        return getTalismans()
    elif(data['type'] == 'getSpells'):
        return getSpells()
    elif(data['type'] == 'getBuild'):
        print(str(data['build']))
        return json.dumps({'hi':"Hello"})
        #return getBuild(data['build'])
    else:
        return None

