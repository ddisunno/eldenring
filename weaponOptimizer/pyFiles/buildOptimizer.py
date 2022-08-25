import requests
import pygsheets
import simplejson as JSON
import calcWeaponAR as calcWeapon

gc = pygsheets.authorize(service_file='eldenring/weaponOptimizer/elden-ring-build-optimizer-c393835be6d1.json')
sh = gc.open('Elden Ring Weapon Calculator 2')
calculator = sh[0]
calculations = sh[3]

def main():
    #First, get the contants from the spreadsheet for the weapon AR formula. This takes the longest amount of time.
    constants = calcWeapon.getWeaponFormulaConstants()
    print('Done constants')

    #On Button press, get user entered information
    numOfLevels = int(calculator.get_value((4, 8)))
    startingClass = calculator.get_value((6, 8)).lower()

    #Get the wepon requirement levels & scaling of the chosen weapon.
    weaponReq = {'strength':int(calculator.get_value((3, 2))),'dexterity':int(calculator.get_value((3, 3))),'intelligence':int(calculator.get_value((3, 4))),'faith':int(calculator.get_value((3, 5))),'arcane':int(calculator.get_value((3, 6)))}

    scaling = [calculator.get_value((4, 2)),calculator.get_value((4, 3)),calculator.get_value((4, 4)),calculator.get_value((4, 5)),calculator.get_value((4, 6))]

    scalingStats = getScalingStats(scaling)

    #Get classes from eldenring.fanapis.com
    classes = JSON.loads(requests.get("https://eldenring.fanapis.com/api/classes").text)

    #Call optimizeBuildStats() based off of which class the user chose.
    for i in range(len(classes['data'])):
        if(startingClass == classes['data'][i]['name'].lower()):
            startingStats = classes['data'][i]['stats']
            optimizeBuildStats(numOfLevels, startingStats, weaponReq, scalingStats, constants)
            #print("hi")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Works for weapons that scale off of 0,1, or 2 stats. 3 stats takes too long due to using calculator. 4 or 5 is not supported. (I'm not sure if 4 or 5 is even possible).
def optimizeBuildStats(numOfLevels, startingStats, weaponReq, scalingStats, constants):

    #If too many levels are enterted, and all scaling stats can be maxed to 99, return every value being 99.
    if(isNumOfLevelsOver(numOfLevels, startingStats, scalingStats)):
        #setStats({'strength': 99, 'dexterity': 99, 'intelligence': 99, 'faith': 99, 'arcane': 99, 'ar': None})
        #print("Hi")
        return 1


    #Get min stats, then get the number of levels to be initially added to the stats that scale.
    minStats = getMinStats(startingStats, weaponReq)
    numOfLevels = getLevelsAfterStatReq(numOfLevels, scalingStats, startingStats, weaponReq)
    numOfLevelsStack = getInitialAddedLevelsPerStat(minStats, scalingStats, numOfLevels)

    #Create the starting state
    startState = {'strength': minStats['strength'], 'dexterity': minStats['dexterity'], 'intelligence': minStats['intelligence'], 'faith': minStats['faith'], 'arcane': minStats['arcane'], 'ar': None}

    #Add initial levels to stats that scale.
    for i in range(len(scalingStats)):
        startState[scalingStats[i]] += numOfLevelsStack[i]

    #Get AR of this state
    startState['ar'] = calcWeapon.getWeaponAR(startState['strength'], startState['dexterity'], startState['intelligence'], startState['faith'], startState['arcane'], constants)

    #If no stats scale or only one stat scales, return startState
    if len(scalingStats) == 0 or len(scalingStats) == 1:
        return 1

    #Min-max for state with the highest AR (Valid state cannot have a stat under the stat minimum defined in minStats, or total # of levels != starting # of levels)
    #Brute Force approach (although other methods won't be much better) */
    optimialBuild = startState.copy() #Initially the start state
    stateStack = [startState]

    #With 2 scalinf stats- branching factor of 1. With 3, branching factor of 2.
    #Feel like im thinking of this the wrong way...
    statesVisited = {}
    statesVisited[str(startState)] = True
    while len(stateStack) > 0:
        state = stateStack.pop().copy()
        
        #console.log(state['strength'], state['dexterity'], state['faith']);

        if(state[scalingStats[0]] - 1 >= minStats[scalingStats[0]]):

            state[scalingStats[0]] -= 1
            for i in range(1, len(scalingStats)):
                newState = state.copy()
                if(newState[scalingStats[i]]+1 <= 99):
                    newState[scalingStats[i]] += 1
                    newState['ar'] = calcWeapon.getWeaponAR(newState['strength'], newState['dexterity'], newState['intelligence'], newState['faith'], newState['arcane'], constants);

                    if(newState['ar'] > optimialBuild['ar']):
                        optimialBuild = newState.copy()
                    
                    
                    if(str(newState) not in statesVisited.keys()):
                        stateStack.append(newState.copy())
                        statesVisited[str(newState)] = True
                    
    #setStats(optimialBuild)
    print("Done Optimization: " + str(optimialBuild['ar']))
    return 1

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/** Helper functions */
#Set the stats on the spreadsheet to the given stats. {str: ...}
def setStats(stats):
  calculator.set_value(stats['strength'], (2,2))
  calculator.set_value(stats['dexterity'], (2,3))
  calculator.set_value(stats['intelligence'], (2,4))
  calculator.set_value(stats['faith'], (2,5))
  calculator.set_value(stats['arcane'], (2,6))
  
#Return an array with the names of the stats that scale with the given weapon.
def getScalingStats(scaling):
  scalingStats = []

  for i in range(len(scaling)):
    if(scaling[i]!='-'):
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
    
main()