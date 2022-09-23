import pandas as pd
import armorOptimizer as armorOptimization
import get_reqs

#Todo- getReqs optimizes endurnace and mind levels, whic hare returned in starting class
df_vigor = pd.read_csv(r'csv/vigor.csv')

#Talismans that affect health total
crimsonHealthBonus = {'None': 1, 'Crimson Amber Medallion': 1.06, 'Crimson Amber Medallion +1': 1.07,'Crimson Amber Medallion +2': 1.08}
erdtreesFavorHealthBonus = {'None': 1, "Erdtree's Favor": 1.03,"Erdtree's Favor +1": 1.035,"Erdtree's Favor +2": 1.04}

def vigorLevelToHealth(level):
    index = int(df_vigor.loc[df_vigor['Level']==level].index[0])
    return df_vigor.iloc[index]['HP']

def healthToVigorLevel(health):
    #Returns the min levels of vigor needed (if not exact, than returns the level such that the health total is higher)
    index = 0
    while(health > df_vigor.iloc[index]['HP']):
        index += 1
    return df_vigor.iloc[index]['Level']

#Calculates the levels of vigor needed to reach user-inputted health goal, including health-boosting talismans
def calcVigorLevels(health, healthIncrease):
    health = health / healthIncrease
    return healthToVigorLevel(health)

def calcStartingClass(weaponName, targetHealth, rollType, healthIncrease):
    rollThreshold = armorOptimization.getRollThreshold(rollType)
    levels = calcVigorLevels(targetHealth,healthIncrease)
    reqs = get_reqs.get_reqs(weaponName,'json/weapons.json',rollThreshold, levels)
    startingClass = get_reqs.optimize_class(reqs)
    return startingClass

