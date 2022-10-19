"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti
project goals:
    1. min-max stats to user selected weapon
    2. optimal gear (armor, talismans)
    3. write build to .txt file
"""

from get_requirements import get_requirements
from optimize_class import optimize_class
from can_equip import can_equip

##### BEGIN: UI INPUTS #####
check_items = True

roll_type = {'light'    : 0.299,
             'med'      : 0.699,
             'fat'      : 0.999,
             'overencumbered' : None}


items_list = [{"name": "Greatsword",
               "file": "weapons.json"},
              {"name": "Clawmark Seal",
               "file": "weapons.json"},
              {"name": "Elden Stars",
               "file": "incantations.json"},
              {"name": "Veteran's Helm",
               "file": "armors.json"},
              {"name": "Erdtree Surcoat",
               "file": "armors.json"},
              {"name": "Veteran's Gauntlets",
               "file": "armors.json"},
              {"name": "Bull-goat Greaves",
               "file": "armors.json"},
              {"name": "Crimson Amber Medallion +2",
               "file": "talismans.json"},
              {"name": "Erdtree's Favor +2",
               "file": "talismans.json"},
              {"name": "Great-jar's Arsenal",
               "file": "talismans.json"},
              {"name": "Radagon Icon",
               "file": "talismans.json"}]



desired_health = 1900

current_roll_type = roll_type['med']

file = 'weapons.json'
##### END: UI INPUTS #####


req_stats = get_requirements(items_list, desired_health, current_roll_type)
best_class, lowest_level, best_stats = optimize_class(req_stats)
equippable_weapons = can_equip(best_stats, current_roll_type, file)
equippable_shields = can_equip(best_stats, current_roll_type, 'shields.json')

print(f"Required Stats: {req_stats}\
      \n\nbest class is:\
      \n{best_class}: {lowest_level},\t{best_stats}\
      \n\nbuild can also use:\
      \n\tweapons:\
      \n{equippable_weapons}\
      \n\tshields:\
      \n{equippable_shields}")