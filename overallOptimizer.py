import weaponOptimizer
import armorOptimizer as armorOptimization
import optimizeClass

# Catching errors in user input can be done on the frontend

#Combines all other optimizers into one, to output the final correct build
def optimizeBuild(weaponName, weaponLevel, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetMind, arsenalTalisman, erdtreeTalisman, talismans, weaponNameDmg): #WeaponName is for the base weapon, weaponNameDmg is the weapon name with affinities.
    ### Calc starting class
    startingClass = optimizeClass.calcStartingClass(weaponName, targetVitality, rollType)

    ### Calc Optimal Weapon Stats
    dmgStats = weaponOptimizer.calcStatsForWeapon(targetLevel, targetVitality, targetEndurance, targetMind, startingClass, weaponNameDmg, weaponLevel, isTwoHanded)

    ### Get Optimal Armor Sets 
    armorSets = armorOptimization.calcOptimalArmorSets(weaponName, talismans, targetEndurance, arsenalTalisman, erdtreeTalisman, rollType) #Need to change this to include talisman weight (Change talismans.json to include)

    ### Add Up & Print Results ########
    build = {'StartingClass': startingClass['name'], 'Level': targetLevel, 'Vitality':targetVitality, 'Endurance': targetEndurance, 'Mind':targetMind} 
    build = {**build,**dmgStats}

    print("Build Stats: " + str(build))
    print('Physical Neg Set: ' + str(armorSets[0]))
    print('Poise Set: ' + str(armorSets[1]))

    return [build, armorSets]

### User Entered Information - Example on how optimizeBuild should be called.
affinity = None #Either an affinity ('Flame Art', 'Sacred', etc. or None)
weaponName = "Greatsword"
weapon = affinity + " " + weaponName if(affinity) else weaponName
weaponLevel = str(25)
isTwoHanded = True
rollType = 'med'

#User entered target levels
targetLevel = 150
targetVitality = 50
targetEndurance = 20
targetMind = 15

#User enterted talismans that effect equipload
arsenalTalisman = 'GreatJarArsenal' #{'GreatJarArsenal':1.19, 'Arsenal+1':1.17, 'Arsenal':1.15, 'None': 1}
erdtreeTalisman = 'None' #{'Erdtree': 1.05, 'Erdtree+1': 1.065, 'Erdtree+2': 1.08, 'None': 1}

talismans = ["Great-jar's Arsenal"] #Array of up to size 4 consisting of strings of the names of the user-chosen talismans

totalOptimalBuild = optimizeBuild(weaponName, weaponLevel, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetMind, arsenalTalisman, erdtreeTalisman, talismans, weapon)
#######################


