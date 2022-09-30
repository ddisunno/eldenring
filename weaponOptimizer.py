'''
Build Optimizer for a given weapon.
Todo: 
   
'''
#Import needed libraries
import calcWeaponAR as calcWeapon
import pandas as pd
import get_reqs

#Declare global variables, this being dataframes build from CSV files holding weapon information.
df_attack = pd.read_csv(r'csv/Attack.csv')
df_scaling = pd.read_csv(r'csv/Scaling.csv')
df_extraData = pd.read_csv(r'csv/Extra_Data.csv')
df_elementParam = pd.read_csv(r'csv/AttackElementCorrectParam.csv')
df_calcCorrect = pd.read_csv(r'csv/CalcCorrectGraph_ID.csv')
                
#### Optimize Functions ############################
#Works for weapons that scale off of 0,1, or 2 stats. 3 stats takes too long due to using calculator. 4 or 5 is not supported. Need to change algorithm to support 4 & 5.
def optimizeWeaponAR(numOfLevels, startingStats, weaponReq, scalingStats, constants):

    #If too many levels are enterted, and all scaling stats can be maxed to 99, return every value being 99.
    if(isNumOfLevelsOver(numOfLevels, startingStats, scalingStats)):
        #print("Enough levels to max out every damage stat.")
        ar = calcWeapon.getWeaponAR(99, 99, 99, 99, 99, constants)
        return {'strength': 99, 'dexterity': 99, 'intelligence': 99, 'faith': 99, 'arcane': 99, 'ar': ar}
    
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
                        
    return optimialBuild

def optimizeWeaponSpellScaling(numOfLevels, startingStats, weaponReq, scalingStats, constants):

    #If too many levels are enterted, and all scaling stats can be maxed to 99, return every value being 99.
    if(isNumOfLevelsOver(numOfLevels, startingStats, scalingStats)):
        #print("Enough levels to max out every damage stat.")
        spellScaling = calcWeapon.getSpellScaling(99, 99, 99, 99, 99, constants)
        return {'strength': 99, 'dexterity': 99, 'intelligence': 99, 'faith': 99, 'arcane': 99, 'spellScaling': spellScaling}
    
    #Get min stats, then get the number of levels to be initially added to the stats that scale.
    minStats = getMinStats(startingStats, weaponReq)
    numOfLevels = getLevelsAfterStatReq(numOfLevels, scalingStats, startingStats, weaponReq)
    numOfLevelsStack = getInitialAddedLevelsPerStat(minStats, scalingStats, numOfLevels)

    #Create the starting state
    startState = {'strength': minStats['strength'], 'dexterity': minStats['dexterity'], 'intelligence': minStats['intelligence'], 'faith': minStats['faith'], 'arcane': minStats['arcane'], 'spellScaling': None}
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

        state['spellScaling'] = calcWeapon.getSpellScaling(state['strength'], state['dexterity'], state['intelligence'], state['faith'], state['arcane'], constants)

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
                        newState['spellScaling'] = calcWeapon.getSpellScaling(newState['strength'], newState['dexterity'], newState['intelligence'], newState['faith'], newState['arcane'], constants);

                        #If the new state has a higher AR then the current optimal state, make the optimal state the new state.
                        if(newState['spellScaling'] > optimialBuild['spellScaling']):
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
                        newState['spellScaling'] = calcWeapon.getSpellScaling(newState['strength'], newState['dexterity'], newState['intelligence'], newState['faith'], newState['arcane'], constants);

                        #If the new state has a higher AR then the current optimal state, make the optimal state the new state.
                        if(newState['spellScaling'] > optimialBuild['spellScaling']):
                            optimialBuild = newState.copy()
                        
                        #If the children states from this state have not been expanded, add them tho the queue, and mark this current state as expanded.
                        if(str(newState) not in statesVisited):
                            stateStack.append(newState.copy())
                            statesVisited.update({str(newState):True})
                        
    return optimialBuild
####################################################

### Helper functions ###############################
def isSomber(weaponName):
    try: 
        affinities = calcWeapon.getAffinities(weaponName)
    except:
        print(f"Error: {weaponName} not found")
        affinities = [""]
    return True if len(affinities) == 1 else False
#Returns false if user entered weapon level is not in range. WeaponLevel is int

def checkWeaponLevel(weaponName, weaponLevel):
    
    isSomberWeapon = isSomber(weaponName)

    if(isSomberWeapon):
        if(weaponLevel > 10):
            print("Error: Weapon level not in correct range. (1-10)")
            return False
        elif(weaponLevel < 1):
            print("Error: Weapon level not in correct range. (1-10)")
            return False
    else:
        if(weaponLevel > 25):
            print("Error: Weapon level not in correct range. (1-25)")
            return False
        elif(weaponLevel < 1):
            print("Error: Weapon level not in correct range. (1-25)")
            return False
    return True

def checkAffinity(weaponName, affinity):
    isSomberWeapon = isSomber(weaponName)
    if(isSomberWeapon and affinity != None):
        print("Error: Affinity added for somber weapon")
        return False
    return True

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
    
#Get starting stats based off of starting class
def getStartingStats(startingClass):
    startClass = get_reqs.fetch_from_json(startingClass, 'json/classes.json')
    return startClass['stats']
                
def calcStatsForWeapon(targetLevel, startingClass, weaponName, weaponLevel, isTwoHanded, affinity, baseName):
    #WeaponName here is affinity + name. affinity is just the affinity, used for checking input error.
    #Check user entered data is correct
    if(not checkWeaponLevel(baseName, int(weaponLevel)) or not checkAffinity(baseName, affinity)):
        return {}

    #Get how many levels are left in the build, the class startiung stats, and the weapon type
    #levelsLeft = targetLevel - (int(startingClass['startLevel']) + int(startingClass['stats'][0]) + targetEndurance + targetMind) #stats[0] is vigor
    levelsLeft = targetLevel - startingClass['lowest']
    startingStats = getStartingStats(startingClass['name'])
    weaponType = calcWeapon.getWeaponType(weaponName)

    #Get the right contants based on weapon type (AR for real weapons, Spell Scaling for spell casters)
    constants = calcWeapon.getWeaponFormulaConstants(weaponName,weaponLevel,isTwoHanded) if(weaponType != 'Glintstone Staff' and weaponType != 'Sacred Seal') else calcWeapon.getSpellScalingFormulaConstants(weaponName,weaponLevel,isTwoHanded)

    #Get weapon requirements and weapon scaling
    weaponReq = calcWeapon.getWeaponReq(weaponName)
    scaling = calcWeapon.getScaling(weaponName, weaponLevel)
    scalingStats = getScalingStats(scaling)

    #Call the right optimizer based on weapon type (AR for real weapons, Spell Scaling for spell casters)
    dmgStats = optimizeWeaponAR(levelsLeft, startingStats, weaponReq, scalingStats, constants) if(weaponType != 'Glintstone Staff' and weaponType != 'Sacred Seal') else optimizeWeaponSpellScaling(levelsLeft, startingStats, weaponReq, scalingStats, constants)

    return dmgStats
###################################################
