import pandas as pd

df = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\Attack.csv')
df_scaling = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\Scaling.csv')
#print(df.loc[0,:])
weapon = "Flame Art Great Knife"
infusion = "Fire"
weaponLevel = "25"

weaponCustom = infusion + " " + weaponLevel

#Get weapon row by weapon name, then get the right value with the given infusion.
print(df.loc[df['Name'] == weapon].index[0])
print(df_scaling.columns.get_loc("Str +" + str(weaponLevel)) + 1)
#print(df.loc[df['Name'] == weapon][weaponCustom][0])
#df.to_json(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\Attack.json')\