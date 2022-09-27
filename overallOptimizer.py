import weaponOptimizer
import armorOptimizer as armorOptimization
import optimizeClass

# Catching errors in user input can be done on the frontend
#Todo: scare/score seals
def checkTalismans(talismans):
    healthIncrease = 1
    equipLoadIncrease = 1

    for talisman in talismans:
        #Arsenal Charm
        if(talisman == "Great-jar's Arsenal"):
            equipLoadIncrease += .19
        elif(talisman == "Arsenal Charm"):
            equipLoadIncrease += .17
        elif(talisman == "Arsenal Charm +1"):
            equipLoadIncrease += .15

        #Erdtree's Favor
        elif(talisman == "Erdtree's Favor"):
            equipLoadIncrease += .05
            healthIncrease += .03
        elif(talisman == "Erdtree's Favor +1"):
            equipLoadIncrease += .065
            healthIncrease += .035
        elif(talisman == "Erdtree's Favor +2"):
            equipLoadIncrease += .08
            healthIncrease += .04
        
        #Crimson Amber Medallion
        elif(talisman == "Crimson Amber Medallion"):
            healthIncrease += .06
        elif(talisman == "Crimson Amber Medallion +1"):
            healthIncrease += .07
        elif(talisman == "Crimson Amber Medallion +2"):
            healthIncrease += .08

    return {"healthIncrease":healthIncrease, "equipLoadIncrease":equipLoadIncrease}

#Combines all other optimizers into one, to output the final correct build
#If weapon AR cannot be calc, just calculates armor
def optimizeBuild(baseName, weaponLevel, affinity, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetPoise, targetMind, talismans): #baseName is for the base weapon, fullName is the weapon name with affinities.
    
    #Pre-process full weapon name
    fullName = affinity + " " + weaponName if(affinity) else weaponName

    #Pre-process talisman infoormation
    statBoostsFromTalismans = checkTalismans(talismans)
    
    ### Calc starting class- includes final vigor, endurance, and mind levels. In form of list {name, lowest, stats, startlevel}
    startingClass = optimizeClass.calcStartingClass(baseName, targetVitality, rollType, statBoostsFromTalismans['healthIncrease']) #Might want to make this take target endurance and mind aswell

    ### Calc Optimal Weapon Stats
    dmgStats = weaponOptimizer.calcStatsForWeapon(targetLevel, startingClass, fullName, weaponLevel, isTwoHanded, affinity, baseName)

    ### Get Optimal Armor Sets 
    #armorSets = armorOptimization.calcOptimalArmorSets(baseName, talismans, targetEndurance, statBoostsFromTalismans['equipLoadIncrease'], rollType) #Need to change this to include talisman weight (Change talismans.json to include)
    armorSet = armorOptimization.calcArmorWithPoise(99,"neg")
    ### Add Up & Print Results ########
    build = {'StartingClass': startingClass['name'], 'Level': targetLevel, 'Vitality':int(startingClass['stats'][0]), 'Endurance': targetEndurance, 'Mind':targetMind} 
    build = {**build,**dmgStats}

    print("Weapon Name: " + fullName + " | Weapon Level: " + weaponLevel + " | Roll Type: " + rollType + " | isTwoHanded: " + str(isTwoHanded))
    print("Build Stats: " + str(build))
    #print('Physical Neg Set: ' + str(armorSet[0]))
    print('Poise Set: ' + str(armorSet))

    return {'build':dmgStats, "armorSets":armorSet}

### User Entered Information - Example on how optimizeBuild should be called.
affinity = None #Either an affinity string (Heavy, Quality, Keen, Fire, Flame Art, Sacred, Lightning, Magic, Poision, Bloody, Occult, Cold) or None/Null type
weaponName = "Golden Order Greatsword"
weaponLevel = str(10) #Should check if entered weapon level is in correct range (1-10 for somber, 1-25 for non-somber)
isTwoHanded = True #T or F
rollType = 'med' #light, med, fat, overencumbered

#User entered target levels
targetLevel = 150 #User enters this. This is the total level of the build, no more, no less.
targetHealth = 1700 #Health is affected by talismans
targetEndurance = None #Make based off stamina?
targetPoise = 51
targetMind = 15 #Make mind based off entered spells/ashes of war
spells = []
ashesOfAWar = []

talismans = ["Great-jar's Arsenal", "Crimson Amber Medallion", "Erdtree's Favor +2", "Blessed Dew Talisman"] #Array of up to size 4 consisting of strings of the names of the user-chosen talismans. Used for calc the total weight of talismans.

totalOptimalBuild = optimizeBuild(weaponName, weaponLevel, affinity, isTwoHanded, rollType, targetLevel, targetHealth, targetEndurance, targetPoise, targetMind, talismans)
#######################

