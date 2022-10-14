from get_requirements import get_requirements
from optimize_class import optimize_class
from can_equip import can_equip
"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti
project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans)
    3. write build to .txt file
"""
'''


##### BEGIN: UI INPUTS #####
roll_type = {'light'    : 0.299,
             'med'      : 0.699,
             'fat'      : 0.999,
             'overencumbered' : None}

items_list = [{"name": "Greatsword",
               "file": "json/weapons.json"},
              {"name": "Clawmark Seal",
               "file": "json/weapons.json"},
              {"name": "Elden Stars",
               "file": "json/incantations.json"},
              {"name": "Veteran's Helm",
               "file": "json/armors.json"},
              {"name": "Erdtree Surcoat",
               "file": "json/armors.json"},
              {"name": "Veteran's Gauntlets",
               "file": "json/armors.json"},
              {"name": "Bull-goat Greaves",
               "file": "json/armors.json"},
              {"name": "Crimson Amber Medallion +2",
               "file": "json/talismans.json"},
              {"name": "Erdtree's Favor +2",
               "file": "json/talismans.json"},
              {"name": "Great-jar's Arsenal",
               "file": "json/talismans.json"},
              {"name": "Radagon Icon",
               "file": "json/talismans.json"}]


desired_health = 1900

current_roll_type = roll_type['med']

file = 'json/weapons.json'
##### END: UI INPUTS #####

#Armor (if poise is given instead of user selecting) -> get_reqs -> optimize_class -> can_equip X 2 -> weapon_optimizer -> can_equip
req_stats = get_requirements(items_list, desired_health, current_roll_type)
best_class, lowest_level, best_stats = optimize_class(req_stats)
equippable_weapons = can_equip(best_stats, current_roll_type, file)
equippable_shields = can_equip(best_stats, current_roll_type, 'json/shields.json')

print(f"Required Stats: {req_stats}\
      \n\nbest class is:\
      \n{best_class}: {lowest_level},\t{best_stats}\
      \n\nbuild can also use:\
      \n\tweapons:\
      \n{equippable_weapons}\
      \n\tshields:\
      \n{equippable_shields}")
'''

roll_type = {'light'    : 0.299,
             'med'      : 0.699,
             'fat'      : 0.999,
             'overencumbered' : None}
def optimize_build(build):

    #Do armor here if not all amor is pre-chosen



    #All weapons are in weapons.json, all armor in armors.json, etc.
    #Does get rqs account for spells?
    item_list = []
    for weapon in build['weapons']['chosenWeapons']:
        if(weapon['name'] != ""):
            item_list.append({"name":weapon['name'],"file":"json/weapons.json"})
    for weapon in build['weapons']['chosenWeaponsSomber']:
        if(weapon['name'] != ""):
            item_list.append({"name":weapon['name'],"file":"json/weapons.json"})
    for talisman in build['talismans']:
        if(talisman['name'] != ""):
            item_list.append({"name":talisman['name'],"file":"json/talismans.json"})
    for armor in build['targetArmor']:
        if(armor['name'] != "" or armor['name'] != "Choose For Me"):
            item_list.append({"name":armor['name'],"file":"json/armors.json"})
    req_stats = get_requirements(item_list, int(build['targetHealth']),roll_type[build['targetRoll']]) #If req_stats['level'] > targetLevel return not possible
    best_class, lowest_level, best_stats = optimize_class(req_stats)

    #Do weapon optimization here with targetLevel - lowest_level # of stats.



    equippable_weapons = can_equip(best_stats, roll_type[build['targetRoll']], 'json/weapons.json')
    equippable_shields = can_equip(best_stats, roll_type[build['targetRoll']], 'json/shields.json')

    print(f"Required Stats: {req_stats}\
      \n\nbest class is:\
      \n{best_class}: {lowest_level},\t{best_stats}\
      \n\nbuild can also use:\
      \n\tweapons:\
      \n{equippable_weapons}\
      \n\tshields:\
      \n{equippable_shields}")
    return ""