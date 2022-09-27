'''
Given the amount of weight left in a build, Find the set of armor (helm, chest, gauntlets, legs) with the highest physical damage negation or highest poise.
First, call getArmorInfoJson().
Then, use the returned list and the given weight left to call getArmorTier().
Then, use the returned list from getArmorTier() and weight left in calling findOptimalArmor(), which returns a list of the optimiaed armor in the form: 
{'chest':None, 'legs':None, 'gauntlets':None, 'helm': None, 'weight':0, 'neg':0}

To do: 
-return multiple best armor options
'''
from collections import deque
import json
import get_reqs
import math

### Constants ##############################################################################
#Roll thresholds- anything over 99.9% is overencumbered.
lightRollThreshold = 0.299
mediumRollThreshold = 0.699
heavyRollThreshold = 0.999

roll_type = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}

#The rate at which each equip load talisman changes the equip load. (0.19 is a 19% increase).
#Note
arsenalTalismans = {"Great-jar's Arsenal":1.19, 'Arsenal Charm +1':1.17, 'Arsenal Charm':1.15, 'None': 1}
erdtreeTalismans = {"Erdtree's Favor": 1.05, "Erdtree's Favor +1": 1.065, "Erdtree's Favor +2": 1.08, 'None': 1}

#Endurance level to equip load- Endurance level is a value from 1-99. enduranceLevelToEquipLoad[level-1] = correctEquipLoad
enduranceLevelToEquipLoad = [45.0,45.0,45.0,45.0,45.0,45.0,45.0,45.0,46.6,48.2,49.8,51.4,52.9,54.5,56.1,57.7,59.3,60.9,62.5,64.1,65.6,67.2,68.8,70.4,72.0,73.0,74.1,75.2,76.4,77.6,78.9,80.2,81.5,82.8,84.1,85.4,6.8,88.1,89.5,90.9,92.3,93.7,95.1,96.5,97.9,99.4,100.8,102.2,103.7,105.2,106.6,108.1,109.6,111.0,112.5,114.0,115.5,117.0,118.5,120.0,121.0,122.1,123.1,124.1,125.1,126.2,127.2,128.2,129.2,130.3,131.3,132.3,133.3,134.4,135.4,136.4,137.4,138.5,139.5,140.5,141.5,142.6,143.6,144.6,145.6,146.7,147.7,148.7,149.7,150.8,151.8,152.8,153.8,154.9,155.9,156.9,157.9,159.0,160.0]
##############################################################################################

def calcWeightLeft(level, equipLoadIncrease, desiredRollType, usedWeight):
    totalEquipLoad = round(enduranceLevelToEquipLoad[level-1] * equipLoadIncrease,1)

    #With total equip load, can calculate the max weight a player can have for each equip load state.
    maxWeightForRoll = round(totalEquipLoad*mediumRollThreshold,1) if(desiredRollType == 'med') else round(totalEquipLoad*lightRollThreshold,1)
    weightLeft = round(maxWeightForRoll - usedWeight -0.1 ,1)
    return weightLeft

def calcUsedWeight(weapon, talismans):
    weight = 0

    weaponInfo = get_reqs.fetch_from_json(weapon, 'json/weapons.json')
    weight += weaponInfo['weight']

    for talisman in talismans:
        talismanInfo = get_reqs.fetch_from_json(talisman, 'json/talismans.json')
        weight += talismanInfo['weight']
    
    return weight

def getArmorInfoJson():
    helm_array = []
    chest_armor_array = []
    gauntlet_array = []
    leg_armor_array = []

    with open('json/armors.json') as f:
        armor_data = json.load(f)
        for armor in armor_data['data']:
            #We print out the name, type, weight, poise, and physical damage negation of the armor piece.
            #0 is used in the snippet "armor['dmgNegation'][0]['amount']" as armor[dmgNegation] returns an array instead of a dictonary. The first value (0 index) of this array is a dictonary of the armors physical damage negation. 
            type = armor['category']
            armor_info = {"name":armor['name'], 'weight': armor['weight'], 'phyNeg':armor['dmgNegation'][0]['amount'], 'poise':armor['resistance'][4]['amount']}
            if(type == "Helm"):
                helm_array.append(armor_info)
            elif(type == "Chest Armor"):
                chest_armor_array.append(armor_info)
            elif(type == "Gauntlets"):
                gauntlet_array.append(armor_info)
            else:
                leg_armor_array.append(armor_info)

    return {"helm": helm_array, "chest": chest_armor_array, "gauntlets":gauntlet_array, "legs":leg_armor_array}

def getArmorTier(weightLeft,armors):

    armors['helm'].sort(key = lambda x:x['weight']) #size- 167
    armors['chest'].sort(key = lambda x:x['weight']) #203
    armors['gauntlets'].sort(key = lambda x:x['weight']) #93
    armors['legs'].sort(key = lambda x:x['weight']) #105

    numHelms = int(len(armors['helm']))
    numChests = int(len(armors['chest']))
    numGauntlets = int(len(armors['gauntlets']))
    numLegs = int(len(armors['legs']))
    
    #Want to reduce search space by atleast 70%.
    #If weighLeft 0-10 - search 0-20 - instant
    if(weightLeft < 11): 
        armors['helm'] = armors['helm'][:int(numHelms*.2)]
        armors['chest'] = armors['chest'][:int(numChests*.2)]
        armors['gauntlets'] = armors['gauntlets'][:int(numGauntlets*.2)]
        armors['legs'] = armors['legs'][:int(numLegs*.2)]
    # 10%-35%
    elif(weightLeft < 16):
        armors['helm'] = armors['helm'][int(numHelms*.1):int(numHelms*.35)]
        armors['chest'] = armors['chest'][int(numChests*.1):int(numChests*.35)]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.1):int(numGauntlets*.35)]
        armors['legs'] = armors['legs'][int(numLegs*.1):int(numLegs*.35)]
    #25%-50%
    elif(weightLeft < 21): 
        armors['helm'] = armors['helm'][int(numHelms*.25):int(numHelms*.5)]
        armors['chest'] = armors['chest'][int(numChests*.25):int(numChests*.5)]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.25):int(numGauntlets*.5)]
        armors['legs'] = armors['legs'][int(numLegs*.25):int(numLegs*.5)]
    #Search 35-65
    elif(weightLeft < 26):
        armors['helm'] = armors['helm'][int(numHelms*.35):int(numHelms*.65)]
        armors['chest'] = armors['chest'][int(numChests*.35):int(numChests*.65)]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.35):int(numGauntlets*.65)]
        armors['legs'] = armors['legs'][int(numLegs*.35):int(numLegs*.65)]
    #55-85 (30%)
    elif(weightLeft < 29):
        armors['helm'] = armors['helm'][int(numHelms*.55):int(numHelms*.85)]
        armors['chest'] = armors['chest'][int(numChests*.55):int(numChests*.85)]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.55):int(numGauntlets*.85)]
        armors['legs'] = armors['legs'][int(numLegs*.55):int(numLegs*.85)]
    #60-90
    elif(weightLeft < 36):
        armors['helm'] = armors['helm'][int(numHelms*.60):int(numHelms*.9)]
        armors['chest'] = armors['chest'][int(numChests*.60):int(numChests*.9)]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.60):int(numGauntlets*.9)]
        armors['legs'] = armors['legs'][int(numLegs*.60):int(numLegs*.9)]
    #80-100
    else:
        armors['helm'] = armors['helm'][int(numHelms*.8):]
        armors['chest'] = armors['chest'][int(numChests*.8):]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.8):]
        armors['legs'] = armors['legs'][int(numLegs*.8):]

    return {"helm": armors['helm'], "chest": armors['chest'], "gauntlets":armors['gauntlets'], "legs":armors['legs']}

def calcOptimalArmorSets(weaponName, talismans, targetEndurance, equipLoadIncrease, rollType):
    usedWeight = calcUsedWeight(weaponName, talismans)
    weightLeft = calcWeightLeft(targetEndurance, equipLoadIncrease, rollType, usedWeight) 

    armors = getArmorInfoJson()
    armors = getArmorTier(weightLeft,armors) 

    phyNegSet = findOptimalArmor(weightLeft,armors,0)
    poiseSet = findOptimalArmor(weightLeft,armors,1)

    return [phyNegSet, poiseSet]

def getRollThreshold(rollType):
    rollThresh = {'light'	: 0.299,
			 'med'		: 0.699,
			 'fat'		: 0.999,
			 'overencumbered' : None}
    
    return rollThresh[rollType]

########################## OPTIMIZATION ########################################################
'''
Todo:
    -Does not work for: 0 < weighs <= 5

Params: 
    -weightLeft: float of the amount of weight left in the build that the player can use in order to be medium/light rolling.
    -armors: List of arrays consisting of the armor for each of the four armor types. Keys: {'helm': , 'chest': , 'gauntlets': , 'legs': }
    -type: what the method should maximize. 0 = physical neg, 1 = poise.

Returns list in the form of:
    {'chest':None, 'legs':None, 'gauntlets':None, 'helm': None, 'weight':0, 'neg':0, 'poi':0},
    where the answer has the highest maximum negation or poise, depending on the type
'''
def findOptimalArmor(weightLeft,armors,type):
    #Init vars
    attribute = "poi" if(type == 1) else "neg"
    count = 0
    optimalSet = {'chest':None, 'legs':None, 'gauntlets':None, 'helm': None, 'weight':0, 'neg':0, 'poi':0}
    stack = deque()
    stack.append(optimalSet.copy())

    #Loop through stack
    while(len(stack) > 0):
       
        current= stack.pop().copy()
        count+=1
       
        if(current['chest'] is None):
            for i in range(len(armors['chest'])):
                current['chest'] = armors['chest'][i]['name']
                current['weight'] = armors['chest'][i]['weight']
                current['neg'] = armors['chest'][i]['phyNeg']
                current['poi'] = armors['chest'][i]['poise']

                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())
        
        elif(current['legs'] is None):
            for i in range(len(armors['legs'])):
                current['legs'] = armors['legs'][i]['name']
                current['weight'] += armors['legs'][i]['weight']
                current['neg'] += armors['legs'][i]['phyNeg']
                current['poi'] += armors['legs'][i]['poise']

                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())

                current['weight'] -= armors['legs'][i]['weight']
                current['neg'] -= armors['legs'][i]['phyNeg']
                current['poi'] -= armors['legs'][i]['poise']

        elif(current['gauntlets'] is None):
            for i in range(len(armors['gauntlets'])):
                current['gauntlets'] = armors['gauntlets'][i]['name']
                current['weight'] += armors['gauntlets'][i]['weight']
                current['neg'] += armors['gauntlets'][i]['phyNeg']
                current['poi'] += armors['gauntlets'][i]['poise']

                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())
                
                current['weight'] -= armors['gauntlets'][i]['weight']
                current['neg'] -= armors['gauntlets'][i]['phyNeg']
                current['poi'] -= armors['gauntlets'][i]['poise']

        elif(current['helm'] is None):
            for i in range(len(armors['helm'])):
                current['helm'] = armors['helm'][i]['name']
                current['weight'] += armors['helm'][i]['weight']
                current['neg'] += armors['helm'][i]['phyNeg']
                current['poi'] += armors['helm'][i]['poise']

                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())

                current['weight'] -= armors['helm'][i]['weight']
                current['neg'] -= armors['helm'][i]['phyNeg']
                current['poi'] -= armors['helm'][i]['poise']
        
        else:
            if(current[attribute]>optimalSet[attribute] or (current[attribute] == optimalSet[attribute] and current['weight'] < optimalSet['weight'])):
                optimalSet = current.copy()

    #Round optimal set, and return list
    optimalSet['weight'] = round(optimalSet['weight'],2)
    optimalSet['neg'] = round(optimalSet['neg'],2)
    optimalSet['poi'] = round(optimalSet['poi'],1)
    return optimalSet
################################################################################################

### Get Armor with target poise, then highest resistance, then lowest weight
#Poise goes from 0-100 from armor
def getArmorWithPoise(targetPoise,armors,tieBreaker,bgTalisman): #tieBreaker is either weight or neg
    if(targetPoise > 133):
        targetPoise = 133

    if(bgTalisman):
        targetPoise = round(targetPoise/1.33,0)

    secondaryTieBreaker = 'weight' if(tieBreaker == 'neg') else 'neg'

    optimalSet = {'chest':None, 'legs':None, 'gauntlets':None, 'helm': None, 'weight':0, 'neg':0, 'poi':0}

    stack = deque()
    stack.append(optimalSet.copy())

    #Loop through stack
    while(len(stack) > 0):
       
        current = stack.pop()
       
        if(current['chest'] is None):
            for chest in armors['chest']:
                current['chest'] = chest['name']
                current['weight'] = chest['weight']
                current['neg'] = chest['phyNeg']
                current['poi'] = chest['poise']

                if(current['poi'] <= targetPoise):
                    stack.append(current.copy())
        
        elif(current['legs'] is None):
            for legs in armors['legs']:
                temp = current.copy()
                temp['legs'] = legs['name']
                temp['weight'] += legs['weight']
                temp['neg'] += legs['phyNeg']
                temp['poi'] += legs['poise']

                if(temp['poi'] <= targetPoise):
                    stack.append(temp.copy())

        elif(current['gauntlets'] is None):
            for gauntlet in armors['gauntlets']:
                temp = current.copy()
                temp['gauntlets'] = gauntlet['name']
                temp['weight'] += gauntlet['weight']
                temp['neg'] += gauntlet['phyNeg']
                temp['poi'] += gauntlet['poise']

                if(temp['poi'] <= targetPoise):
                    stack.append(temp.copy())
                
        elif(current['helm'] is None): 
            neededPoise = targetPoise - current['poi']
            for helm in armors['helm']:
                
                if(helm['poise'] == neededPoise): #0 > any # is always false
                    temp = current.copy()
                    temp['helm'] = helm['name']
                    temp['weight'] += helm['weight']
                    temp['neg'] += helm['phyNeg']
                    temp['poi'] = targetPoise
                    
                    #Else, use tiebreaker
                    if(tieBreaker == "neg"):
                        if(temp[tieBreaker] > optimalSet[tieBreaker] or optimalSet[tieBreaker] == 0):
                            optimalSet = temp.copy()
                        elif(temp[tieBreaker] == optimalSet[tieBreaker] and temp[secondaryTieBreaker] < optimalSet[secondaryTieBreaker]):
                            optimalSet = temp.copy()

                    else:
                        if(temp[tieBreaker] < optimalSet[tieBreaker] or optimalSet[tieBreaker] == 0):
                            optimalSet = temp.copy()
                        elif(temp[tieBreaker] == optimalSet[tieBreaker] and temp[secondaryTieBreaker] > optimalSet[secondaryTieBreaker]):
                            optimalSet = temp.copy()

    #Round optimal set, and return list
    optimalSet['weight'] = round(optimalSet['weight'],2)
    optimalSet['neg'] = round(optimalSet['neg'],2)
    optimalSet['poi'] = round(optimalSet['poi'] * 1.33,0) if(bgTalisman) else round(optimalSet['poi'],0)
    return optimalSet

def getArmorTierByPoise(targetPoise, armors):
    armors['helm'].sort(key = lambda x:x['poise']) #size- 167
    armors['chest'].sort(key = lambda x:x['poise']) #203
    armors['gauntlets'].sort(key = lambda x:x['poise']) #93
    armors['legs'].sort(key = lambda x:x['poise']) #105

    numHelms = int(len(armors['helm']))
    numChests = int(len(armors['chest']))
    numGauntlets = int(len(armors['gauntlets']))
    numLegs = int(len(armors['legs']))
    
    #Want to reduce search space by atleast 70%.
    if(targetPoise < 30): 
        armors['helm'] = armors['helm'][:int(numHelms*.75)]
        armors['chest'] = armors['chest'][:int(numChests*.75)]
        armors['gauntlets'] = armors['gauntlets'][:int(numGauntlets*.75)]
        armors['legs'] = armors['legs'][:int(numLegs*.75)]
    #80-100
    else:
        armors['helm'] = armors['helm'][int(numHelms*.25):]
        armors['chest'] = armors['chest'][int(numChests*.25):]
        armors['gauntlets'] = armors['gauntlets'][int(numGauntlets*.25):]
        armors['legs'] = armors['legs'][int(numLegs*.25):]

    return {"helm": armors['helm'], "chest": armors['chest'], "gauntlets":armors['gauntlets'], "legs":armors['legs']}

#TieBreaker is either neg or weight (if two or more armor sets hit the target poise, then break ties with the chosen value (weight or physical negation))
def calcArmorWithPoise(targetPoise, tieBreaker,bgtalisman):
    
    armors = getArmorInfoJson()
    #armors = getArmorTierByPoise(targetPoise,armors) 

    armorSet = getArmorWithPoise(targetPoise,armors,tieBreaker,bgtalisman)

    return armorSet

def armorPoiseToJson():

    talismanWeight = []
    talismanNeg = []
    noTalismanWeight = []
    noTalismanNeg = []

    for i in range(0,134):
        if(i <= 100):
            noTalismanWeight.append({"Target Poise": i, "Armor Set":calcArmorWithPoise(i,"weight",False)})
            noTalismanNeg.append({"Target Poise": i, "Armor Set":calcArmorWithPoise(i,"neg",False)})
        talismanWeight.append({"Target Poise": i, "Armor Set":calcArmorWithPoise(i,"weight",True)})
        talismanNeg.append({"Target Poise": i, "Armor Set":calcArmorWithPoise(i,"neg",True)})
        print("Done with: " + str(i))

    bgTalisman = {"weight":talismanWeight, "neg":talismanNeg}
    noTalisman = {"weight":noTalismanWeight, "neg":noTalismanNeg}

    string = {"Bull Goat Increase": bgTalisman, "Standard": noTalisman}

    with open(f'poiseArmorSets2.json', 'w') as f:
        json.dump(string,f)
    
    return string

def testArmorPoise():
    for i in range(11):
        print(calcArmorWithPoise(i,"weight",True))

def getArmorByPoise(poise, tieBreaker, bullGoatTalisman):
    talisman = None
    if(bullGoatTalisman):
        talisman = "Bull Goat Increase"
    else:
        talisman = "Standard"

    with open('json/poiseArmorSets.json') as f:
        data = json.load(f)
    
    for set in data[talisman][tieBreaker]:
        if(set["Target Poise"] == poise):
            return set["Armor Set"]

    return None

print(getArmorByPoise(10,"weight",False))
