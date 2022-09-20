import weaponOptimizer
import armorOptimizer as armorOptimization
import optimizeClass

# Catching errors in user input can be done on the frontend
#Todo: function that determines what level to make vigor based on desiered health total (including talismans)
#Combines all other optimizers into one, to output the final correct build
#If weapon AR cannot be calc, just calculates armor
def optimizeBuild(baseName, fullName, weaponLevel, affinity, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetMind, arsenalTalisman, erdtreeTalisman, talismans): #baseName is for the base weapon, fullName is the weapon name with affinities.
    ### Calc starting class
    startingClass = optimizeClass.calcStartingClass(baseName, targetVitality, rollType) #Might want to make this take target endurance and mind aswell
   
    ### Calc Optimal Weapon Stats
    dmgStats = weaponOptimizer.calcStatsForWeapon(targetLevel, targetVitality, targetEndurance, targetMind, startingClass, fullName, weaponLevel, isTwoHanded, affinity, baseName)

    ### Get Optimal Armor Sets 
    armorSets = armorOptimization.calcOptimalArmorSets(baseName, talismans, targetEndurance, arsenalTalisman, erdtreeTalisman, rollType) #Need to change this to include talisman weight (Change talismans.json to include)

    ### Add Up & Print Results ########
    build = {'StartingClass': startingClass['name'], 'Level': targetLevel, 'Vitality':targetVitality, 'Endurance': targetEndurance, 'Mind':targetMind} 
    build = {**build,**dmgStats}

    print("Weapon Name: " + fullName + " | Weapon Level: " + weaponLevel + " | Roll Type: " + rollType + " | isTwoHanded: " + str(isTwoHanded))
    print("Build Stats: " + str(build))
    print('Physical Neg Set: ' + str(armorSets[0]))
    print('Poise Set: ' + str(armorSets[1]))

    return [build, armorSets]

### User Entered Information - Example on how optimizeBuild should be called.
affinity = None #Either an affinity ('Flame Art', 'Sacred', etc. or None)
weaponName = "Golden Order Greatsword"
weapon = affinity + " " + weaponName if(affinity) else weaponName
weaponLevel = str(10) #Should check if entered weapon level is in correct range (1-10 for somber, 1-25 for non-somber)
isTwoHanded = True
rollType = 'med'

#User entered target levels
targetLevel = 150 #User enters this. This is the total level of the build, no more, no less.
targetVitality = 50 #Viality is affected by talismans
targetEndurance = 20 #Make based off stamina?
targetMind = 15 #Make mind based off entered spells/ashes of war/spirit summons

#User enterted talismans that effect equipload
arsenalTalisman = 'GreatJarArsenal' #{'GreatJarArsenal':1.19, 'Arsenal+1':1.17, 'Arsenal':1.15, 'None': 1}
erdtreeTalisman = 'None' #{'Erdtree': 1.05, 'Erdtree+1': 1.065, 'Erdtree+2': 1.08, 'None': 1}

talismans = ["Great-jar's Arsenal"] #Array of up to size 4 consisting of strings of the names of the user-chosen talismans

totalOptimalBuild = optimizeBuild(weaponName, weapon, weaponLevel, affinity, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetMind, arsenalTalisman, erdtreeTalisman, talismans)
#######################
