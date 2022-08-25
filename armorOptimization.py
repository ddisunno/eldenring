#Elden Ring API test
#Print out the name of each piece of armor in Elden Ring.
#To use the requests module, had to move four files from Anaconda3/Library/bin to Anaconda3/DLLS.
#Use the Acaconda3 based Python interpreter for this project. 
from collections import deque
import json
import requests

#Roll thresholds- anything over 99.9% is overencumbered.
lightRollThreshold = 0.299
mediumRollThreshold = 0.699
heavyLoadThreshold = 0.999

#The rate at which each equip load talisman changes the equip load. (0.19 is a 19% increase).
#Note
arsenalTalismans = {'GreatJarArsenal':1.19, 'Arsenal+1':1.17, 'Arsenal':1.15}
erdtreeTalismans = {'Erdtree': 1.05, 'Erdtree+1': 1.065, 'Erdtree+2': 1.08}

#Endurance level to equip load- Endurance level is a value from 1-99. enduranceLevelToEquipLoad[level-1] = correctEquipLoad
enduranceLevelToEquipLoad = [45.0,45.0,45.0,45.0,45.0,45.0,45.0,45.0,46.6,48.2,49.8,51.4,52.9,54.5,56.1,57.7,59.3,60.9,62.5,64.1,65.6,67.2,68.8,70.4,72.0,73.0,74.1,75.2,76.4,77.6,78.9,80.2,81.5,82.8,84.1,85.4,6.8,88.1,89.5,90.9,92.3,93.7,95.1,96.5,97.9,99.4,100.8,102.2,103.7,105.2,106.6,108.1,109.6,111.0,112.5,114.0,115.5,117.0,118.5,120.0,121.0,122.1,123.1,124.1,125.1,126.2,127.2,128.2,129.2,130.3,131.3,132.3,133.3,134.4,135.4,136.4,137.4,138.5,139.5,140.5,141.5,142.6,143.6,144.6,145.6,146.7,147.7,148.7,149.7,150.8,151.8,152.8,153.8,154.9,155.9,156.9,157.9,159.0,160.0]

#Example of calculating a player's total equip load (Level 99 endurance + Great Jar and Ertree+2). Rounded to tenths.
level = 99
totalEquipLoad = round(enduranceLevelToEquipLoad[level-1] * arsenalTalismans['GreatJarArsenal']*erdtreeTalismans['Erdtree+2'],1)
#print(totalEquipLoad)

#With total equip load, can calculate the max weight a player can have for each equip load state.
maxWeightForMediumRoll = round(totalEquipLoad*mediumRollThreshold,1)
maxWeightForLightRoll = round(totalEquipLoad*lightRollThreshold,1)
#print(str(maxWeightForLightRoll) +" "+ str(maxWeightForMediumRoll))

#Player must add their weapons/tailsmans to calculate used weight. This would call API.
usedWeight = 0
weightLeft = round(maxWeightForMediumRoll - usedWeight,1)

#Find four armor pieces (head, chest, legs, boots) s.t. the total weight of the armor < weightLeft, and the Physical (or fire, bleed, etc.) damage negation is maximized. Uses API.
#This part will require some algorithms. 




#Returns dict with four values- one for each armor type. Each of these values is a list of dicts containing the info of each armor in the cooresponding armor type.
def getArmorInfo():
    helm_array = []
    chest_armor_array = []
    gauntlet_array = []
    leg_armor_array = []

    #There are 6 pages of info tp parse through. The API does not have a data['next'] value to show the next page to parse, so we must use this method
    for i in range(6):
        x = requests.get('https://eldenring.fanapis.com/api/armors?limit=500&page='+ str(i))
        total_data = json.loads(x.text)
        armor_data = total_data['data']
        for armor in armor_data:
            #We print out the name, type, weight, and physical damage negation of the armor piece.
            #0 is used in the snippet "armor['dmgNegation'][0]['amount']" as armor[dmgNegation] returns an array instead of a dictonary. The first value (0 index) of this array is a dictonary of the armors physical damage negation. 
            #print("Name: " + armor['name']+ ' | Type: ' + armor['category']+' | Weight: ' + str(armor['weight'])+' | Phy Neg: ' + str(armor['dmgNegation'][0]['amount']))
            type = armor['category']
            armor_info = {"name":armor['name'], 'weight': armor['weight'], 'phyNeg':armor['dmgNegation'][0]['amount']}
            if(type == "Helm"):
                helm_array.append(armor_info)
            elif(type == "Chest Armor"):
                chest_armor_array.append(armor_info)
            elif(type == "Gauntlets"):
                gauntlet_array.append(armor_info)
            else:
                leg_armor_array.append(armor_info)

    return {"helm": helm_array, "chest": chest_armor_array, "gauntlets":gauntlet_array, "legs":leg_armor_array}

#Worst case expands 333,047,079 nodes
#Best case expands 1 node.
#Split this into 3 groups based off weight left, with three different search trees. One for high weight left, medium wiehgt left, and low weight left.
#Does not work for: 0 < weighs <= 5
def findOptimalArmor(weightLeft):
    if(weightLeft >= 62.9):
        return {'chest': 'Bull-goat Armor', 'legs': 'Fire Prelate Greaves', 'gauntlets': 'Bull-goat Gauntlets', 'helm': 'Pumpkin Helm', 'weight': 62.89999999999998, 'neg': 43.0}

    count = 0
    optimalSet = {'chest':None, 'legs':None, 'gauntlets':None, 'helm': None, 'weight':0, 'neg':0}
    armors = getArmorInfo()
    stack = deque()

    stack.append({'chest':None, 'legs':None, 'gauntlets':None, 'helm': None, 'weight':0, 'neg':0})

    while(len(stack) > 0):
       
        popped = stack.pop()
        count+=1
        current = popped.copy()
        #print(current)
        if(current['chest'] is None):
            for i in range(len(armors['chest'])):
                #print(len(armors['chest']))
                current['chest'] = armors['chest'][i]['name']
                current['weight'] = armors['chest'][i]['weight']
                current['neg'] = armors['chest'][i]['phyNeg']
                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())
        
        elif(current['legs'] is None):
            for i in range(len(armors['legs'])):
                current['legs'] = armors['legs'][i]['name']
                current['weight'] += armors['legs'][i]['weight']
                current['neg'] += armors['legs'][i]['phyNeg']
                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())

                current['weight'] -= armors['legs'][i]['weight']
                current['neg'] -= armors['legs'][i]['phyNeg']

        elif(current['gauntlets'] is None):
            for i in range(len(armors['gauntlets'])):
                current['gauntlets'] = armors['gauntlets'][i]['name']
                current['weight'] += armors['gauntlets'][i]['weight']
                current['neg'] += armors['gauntlets'][i]['phyNeg']
                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())
                
                current['weight'] -= armors['gauntlets'][i]['weight']
                current['neg'] -= armors['gauntlets'][i]['phyNeg']

        elif(current['helm'] is None):
            for i in range(len(armors['helm'])):
                current['helm'] = armors['helm'][i]['name']
                current['weight'] += armors['helm'][i]['weight']
                current['neg'] += armors['helm'][i]['phyNeg']
                if(current['weight'] <= weightLeft):
                    stack.append(current.copy())

                current['weight'] -= armors['helm'][i]['weight']
                current['neg'] -= armors['helm'][i]['phyNeg']
        
        else:
            if(current['neg']>optimalSet['neg']):
                optimalSet = current.copy()

    print(count)
    return optimalSet

#DFS
print(findOptimalArmor(10))

#0 wL = 1 node expanded
#6 wL = 1034 nodes
#10 wL = 1,382,804 nodes
#15 wL = 36,023,046 nodes
#20 wL = 136,735,341 nodes
#25 wL = 240,270,445 nodes
#30 wL = 299,179,522 nodes
#35 wL = 322,888,116 Nodes
#40 wL = 330,627,057 nodes
#45 wL = 332,627,937 nodes
#50 wL = 332,997,271 nodes
#55 wL = 332,997,271 nodes
#60 wL = 333,047,011 nodes
#62.9 = 333,047,079 nodes
#65 wL = 333,047,079 nodes
#Worst case = 333,047,079 nodes (~6 min runtime on Rudy's laptop)

#Higher wL means less trees are pruned, since more armor fits.
#Any search where wL >= 62.9 is {'chest': 'Bull-goat Armor', 'legs': 'Fire Prelate Greaves', 'gauntlets': 'Bull-goat Gauntlets', 'helm': 'Pumpkin Helm', 'weight': 62.89999999999998, 'neg': 43.0}.
