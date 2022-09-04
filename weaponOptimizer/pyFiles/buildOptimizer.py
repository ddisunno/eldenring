'''
Build Optimizer for a given weapon.
'''
#Import needed libraries
import requests
import simplejson as JSON
import calcWeaponAR as calcWeapon
import pandas as pd

#Declare global variables, this being dataframes build from CSV files holding weapon information.
df_attack = pd.read_csv(r'eldenring\weaponOptimizer\pyFiles\.csv\Attack.csv')
df_scaling = pd.read_csv(r'eldenring\weaponOptimizer\pyFiles\.csv\Scaling.csv')
df_extraData = pd.read_csv(r'eldenring\weaponOptimizer\pyFiles\.csv\Extra_Data.csv')
df_elementParam = pd.read_csv(r'eldenring\weaponOptimizer\pyFiles\.csv\AttackElementCorrectParam.csv')
df_calcCorrect = pd.read_csv(r'eldenring\weaponOptimizer\pyFiles\.csv\CalcCorrectGraph_ID.csv')

### Main Function ### Takes in the user input, gets the needed information from the CSV files, and calculates the optimal stats needed for the given weapon. User input includes: Weapon Name, Weapon Level, Weapon Affinity(if any), isTwoHanded, Starting class, and the number of levels the user has left in their build to spend on damage stats (str, dex, int, fai, arc).
def main():
    #These var should be entered from user in front-end
    weaponName = "Erdsteel Dagger"
    weaponLevel = str(25)
    isTwoHanded = True
    numOfLevels = 90
    startingClass = "prophet"
    
    #Get if weapon upgrades to +10 or +25, and if it can have affinities.
    affinities = getAffinities(weaponName)
    isSomberWeapon = True if len(affinities) == 1 else False

    #If user enters a weapon level above 10 for a somber weapon, set the weapon level to 10 (Max level)
    weaponLevel = str(10) if (isSomberWeapon and int(weaponLevel) > 10) else weaponLevel

    #Get starting class stats
    startingStats = getStartingStats(startingClass)
    
    #If somber, run once, if can have affinities, run once for each affinity
    for i in range(len(affinities)):
        #If non-somber, then get the next affinity and update weaon name. Else, weapon becomes weaponName.
        if not isSomberWeapon:
            weaponAffinity = affinities[i]
            weapon = weaponAffinity + " " + weaponName
        else:
            weaponAffinity = ""
            weapon = weaponName

        #Get constants for the weapon AR formula for the given weapon. This comes from CSV files parsed by Pandas Dataframes.
        constants = calcWeapon.getWeaponFormulaConstants(weapon,weaponLevel,isTwoHanded)
        print('Done constants')

        #Get the wepon requirement levels & scaling of the chosen weapon. (Repeated work with H2 and H4)
        H2 = int(df_attack.loc[df_attack['Name'] == weapon].index[0])
        H4 = int(df_scaling.columns.get_loc("Str +" + str(weaponLevel)))

        result = df_extraData.iloc[H2,5:10]
        weaponReq = {'strength':int(result[0]),'dexterity':int(result[1]),'intelligence':int(result[2]),'faith':int(result[3]),'arcane':int(result[4])}
        
        scaling = df_scaling.iloc[H2,H4:H4+5].astype(float)
        scalingStats = getScalingStats(scaling)

        #Call optimizeBuildStats()
        print("Affinity: " + weaponAffinity)
        optimizeBuildStats(numOfLevels, startingStats, weaponReq, scalingStats, constants)
                
################################################################################################################
#Works for weapons that scale off of 0,1, or 2 stats. 3 stats takes too long due to using calculator. 4 or 5 is not supported. Need to change algorithm to support 4 & 5.
def optimizeBuildStats(numOfLevels, startingStats, weaponReq, scalingStats, constants):

    #If too many levels are enterted, and all scaling stats can be maxed to 99, return every value being 99.
    if(isNumOfLevelsOver(numOfLevels, startingStats, scalingStats)):
        print("Enough levels to max out every damage stat.")
        return 1
    
    #Get min stats, then get the number of levels to be initially added to the stats that scale.
    minStats = getMinStats(startingStats, weaponReq)
    numOfLevels = getLevelsAfterStatReq(numOfLevels, scalingStats, startingStats, weaponReq)
    numOfLevelsStack = getInitialAddedLevelsPerStat(minStats, scalingStats, numOfLevels)

    #Create the starting state
    startState = {'strength': minStats['strength'], 'dexterity': minStats['dexterity'], 'intelligence': minStats['intelligence'], 'faith': minStats['faith'], 'arcane': minStats['arcane'], 'ar': None}
    statesVisited = {}
    optimialBuild = None

    #Loop through starting here, intililize stateVisted above, each loop has starting stats changed.
    for stat in range(len(scalingStats)):

        state = startState.copy()

        index = 0
        for i in range(stat, len(scalingStats)):
           state[scalingStats[i]] += numOfLevelsStack[index]
           index+=1
        if stat > 0:
            for i in reversed(range(stat-1, 0)):
                state[scalingStats[i]] += numOfLevelsStack[index]
                index+=1
        
        statesVisited[str(state)] = True

        state['ar'] = calcWeapon.getWeaponAR(state['strength'], state['dexterity'], state['intelligence'], state['faith'], state['arcane'], constants)

        #If no stats scale or only one stat scales, return startState
        if len(scalingStats) == 0 or len(scalingStats) == 1:
            return 1

        #Min-max for state with the highest AR (Valid state cannot have a stat under the stat minimum defined in minStats, or total # of levels != starting # of levels)
        #Brute Force approach (although other methods won't be much better) */
        #optimialBuild = state.copy() #Initially the start state
        if optimialBuild is None:
            optimialBuild = state.copy()
        
        #Create a queue to hold the state nodes, starting with the startState. A dict is used to keep track of whether or not a node has been visited, so that the same node is not added back into the queue.
        stateStack = [state]
        
        #Note: With 2 scaling stats, there is a branching factor of 1. With 3 sclaing stats, branching factor of 2.
        #While our queue is not empty, pop the queue.
        while len(stateStack) > 0:
            #Get current state
            state = stateStack.pop().copy()
            
            #Subtract 1 from the first scaling stat
            if(state[scalingStats[stat]] - 1 >= minStats[scalingStats[stat]]):
                state[scalingStats[stat]] -= 1

                #For every other scaling stat, create a state in which the level taken away from the first scaling stat was added to the scaling stat. This (has the potential to) create multiple states.
                for i in range(stat+1, len(scalingStats)):
                    newState = state.copy()
                    #If the stat is not maxed out (less than 99), then add 1 to that stat.
                    if(newState[scalingStats[i]]+1 <= 99):
                        newState[scalingStats[i]] += 1
                        newState['ar'] = calcWeapon.getWeaponAR(newState['strength'], newState['dexterity'], newState['intelligence'], newState['faith'], newState['arcane'], constants);

                        #If the new state has a higher AR then the current optimal state, make the optimal state the new state.
                        if(newState['ar'] > optimialBuild['ar']):
                            optimialBuild = newState.copy()
                        
                        #If the children states from this state have not been expanded, add them tho the queue, and mark this current state as expanded.
                        if(str(newState) not in statesVisited):
                            stateStack.append(newState.copy())
                            statesVisited.update({str(newState):True})
                #From stat - 1 to 0
                for i in reversed(range(stat-1, 0)):
                    newState = state.copy()
                    #If the stat is not maxed out (less than 99), then add 1 to that stat.
                    if(newState[scalingStats[i]]+1 <= 99):
                        newState[scalingStats[i]] += 1
                        newState['ar'] = calcWeapon.getWeaponAR(newState['strength'], newState['dexterity'], newState['intelligence'], newState['faith'], newState['arcane'], constants);

                        #If the new state has a higher AR then the current optimal state, make the optimal state the new state.
                        if(newState['ar'] > optimialBuild['ar']):
                            optimialBuild = newState.copy()
                        
                        #If the children states from this state have not been expanded, add them tho the queue, and mark this current state as expanded.
                        if(str(newState) not in statesVisited):
                            stateStack.append(newState.copy())
                            statesVisited.update({str(newState):True})
                        
    #Done with algorithm, print results to console (for now).
    #print("Done Optimization")
    #print("Str: " + str(optimialBuild['strength']))
    #print("Dex: " + str(optimialBuild['dexterity']))
    #print("Int: " + str(optimialBuild['intelligence']))
    #print("Fai: " + str(optimialBuild['faith']))
    #print("Arc: " + str(optimialBuild['arcane']))
    print("AR: " + str(optimialBuild["ar"]))
   
    return optimialBuild

################################################################################################################
### Helper functions ###
#Return an array with the names of the stats that scale with the given weapon.
def getScalingStats(scaling):
  scalingStats = []

  for i in range(len(scaling)):
    if(scaling[i]!=0):
        if(i == 0):
            scalingStats.append('strength')
        elif(i==1):
            scalingStats.append('dexterity')
        elif(i==2):
            scalingStats.append('intelligence')
        elif(i==3):
            scalingStats.append('faith')
        elif(i==4):
            scalingStats.append('arcane')
        
  return scalingStats

def getMinStats(startingStats, weaponReq):
    #Minimum stats based off of starting class
    minStr = max(int(startingStats['strength']),weaponReq['strength'])
    minDex = max(int(startingStats['dexterity']),weaponReq['dexterity'])
    minInt = max(int(startingStats['intelligence']),weaponReq['intelligence'])
    minFai = max(int(startingStats['faith']),weaponReq['faith'])
    minArc = max(int(startingStats['arcane']),weaponReq['arcane'])
    return {'strength':minStr, 'dexterity':minDex, 'intelligence':minInt, 'faith':minFai, 'arcane':minArc}
    
#Get the amount of levels taken from weapon requirments, that cannot be used in optimizing.
def getLevelsAfterStatReq(numOfLevels, scalingStats, startingStats, weaponReq):
    levelsFromStatReq = 0

    for i in range(len(scalingStats)):
        if(int(startingStats[scalingStats[i]]) < weaponReq[scalingStats[i]]):
            levelsFromStatReq += weaponReq[scalingStats[i]] - int(startingStats[scalingStats[i]])
        
    return numOfLevels - levelsFromStatReq

#If the user entered enough stats to max out each statline that scales, return true.
def isNumOfLevelsOver(numOfLevels, startingStats, scalingStats):
    #Get total number of levels already in scaled stats
    startScalingTotal = 0

    for i in range(len(scalingStats)):
        startScalingTotal = startScalingTotal + int(startingStats[scalingStats[i]])

    #If the user entered too many levels, then true
    if(numOfLevels >= (len(scalingStats) * 99) - startScalingTotal):
        return True
    else:
        return False
    
#Get the amount of levels to be initally added to each scaling stat line based of the number of levels given, and the min stats of the character. Returns an array of length = # of scaling stats, with each entry being between minStat and 99.
def getInitialAddedLevelsPerStat(minStats, scalingStats, numOfLevels):
    numOfLevelsStack = [0] * len(scalingStats)

    for i in range(len(scalingStats)):
        if(minStats[scalingStats[i]] + numOfLevels > 99):
            numOfLevelsStack[i] = 99-minStats[scalingStats[i]]
            numOfLevels -= numOfLevelsStack[i]
        else:
            numOfLevelsStack[i] += numOfLevels
            break
    return numOfLevelsStack
    
#Get the weapon's affinities
def getAffinities(weaponName):
    H2 = int(df_extraData.loc[df_extraData['Name'] == weaponName].index[0])

    return [""] if int(df_extraData.iloc[H2,4]) == 10 else ["Heavy","Keen","Quality","Flame Art","Sacred","Magic","Cold","Fire","Lightning","Poison","Blood","Occult"]

#Get starting stats based off of starting class
def getStartingStats(startingClass):
    classes = JSON.loads(requests.get("https://eldenring.fanapis.com/api/classes").text)
    for i in range(len(classes['data'])):
        if(startingClass == classes['data'][i]['name'].lower()):
            return classes['data'][i]['stats']
                
main()