import pandas as pd
import armorOptimizer as armorOptimization
import get_reqs

df_vigor = pd.read_csv(r'csv\vigor.csv')

def vigorLevelToHealth(level):
    index = int(df_vigor.loc[df_vigor['Level']==level].index[0])
    return df_vigor.iloc[index]['HP']

def calcStartingClass(weaponName, targetVitality, rollType):
    rollThreshold = armorOptimization.getRollThreshold(rollType)
    health = vigorLevelToHealth(targetVitality)
    reqs = get_reqs.get_reqs(weaponName,'json\weapons.json',rollThreshold, health)
    startingClass = get_reqs.optimize_class(reqs)
    return startingClass