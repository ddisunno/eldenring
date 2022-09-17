import weaponOptimizer
import armorOptimizer as armorOptimization
import get_reqs

#Combines all other optimizers into one, to output the final correct build
def optimizeBuild(weaponName, weaponLevel, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetMind, arsenalTalisman, erdtreeTalisman, talismans):
    ### Calc starting class
    rollThreshold = armorOptimization.getRollThreshold(rollType)
    reqs = get_reqs.get_reqs(weaponName,'eldenring/weapons.json',rollThreshold)
    startingClass = get_reqs.fetch_from_json('Prophet', 'eldenring/classes.json') #Find Optimal starting class

    ### Calc Optimal Weapon Stats
    dmgStats = weaponOptimizer.calcStatsForWeapon(targetLevel, targetVitality, targetEndurance, targetMind, startingClass, weaponName, weaponLevel, isTwoHanded)

    ### Get Optimal Armor Sets 
    armorSets = armorOptimization.calcOptimalArmorSets(weaponName, talismans, targetEndurance, arsenalTalisman, erdtreeTalisman, rollType)

    ### Add Up & Print Results ########
    build = {'StartingClass': startingClass['name'], 'Level': targetLevel, 'Vitality':targetVitality, 'Endurance': targetEndurance, 'Mind':targetMind} 
    build = {**build,**dmgStats}

    print("Build Stats: " + str(build))
    print('Physical Neg Set: ' + str(armorSets[0]))
    print('Poise Set: ' + str(armorSets[1]))

    return [build, armorSets]

### User Entered Information - Example on how optimizeBuild should be called.
weaponName = "Moonveil"
weaponLevel = str(10)
isTwoHanded = True
rollType = 'med'

targetLevel = 150
targetVitality = 50
targetEndurance = 20
targetMind = 15

arsenalTalisman = 'GreatJarArsenal'
erdtreeTalisman = 'None'
#talismans = [arsenalTalisman,erdtreeTalisman] #ADD TALISMANS.JSON
talismans = []

totalOptimalBuild = optimizeBuild(weaponName, weaponLevel, isTwoHanded, rollType, targetLevel, targetVitality, targetEndurance, targetMind, arsenalTalisman, erdtreeTalisman, talismans)
#######################

