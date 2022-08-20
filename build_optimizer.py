"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti

project goals:
    1. min-max stats to user selected weapon
    2. optimal gear
    3. write build to .txt file
"""
import requests
import pandas as pd
import pygsheets

#cells
StrCell = (2,2)
DexCell = (2,3)
IntCell = (2,4)
FaiCell = (2,5)
ArcCell = (2,6)

weaponCell = (2,7)
totalARcell = (10,7)

#User enters information: What weapon they want the min-max(including weapon level and infusion), how many levels they have left for str,dex,int,faith,arc, their starting class, two-anding weapon or not
#authorization
gc = pygsheets.authorize(service_file='eldenring/elden-ring-build-optimizer-c393835be6d1.json')

# Create empty dataframe
#df = pd.DataFrame()
weaponNamedf = pd.DataFrame()

#Testing info
#df['20'] = []
weaponNamedf['Dagger'] = []
levels = 90

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Elden Ring Weapon Calculator 2')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(weaponNamedf,(2,7))



print(wks.get_value(totalARcell))

def minMaxStats(numOfLevels):
    return None

minMaxStats(90)

#Option 1: Add a script to the google spreadsheet that optimizes the build.
    #Pros: Simple, allows for multiple people to use the calculator at once, easy to spread, no need to build frontend for user input/display information, optimization runs on google servers (better runtime), can use on any device that has google spreadsheets. Overall a lot less work.
    #Cons: Have to use weird js for optimization algorithm, can't use python, harder to show on github

#Option 2: Use google sheet as calculator, use python as backend, display results to text file.
    #Pros: Python is easy to use for algorithm, easy to show on github
    #Cons: Have to write code to prompt user, no frontend besides command line, output is in a harder to read state, only one person can use the calculator at a time (no scalability), runs on local machine (could run slower), not as easy to distribute, can't run on phones. Overall: more work involved for a less flexible project, but can use python.

#Option 3: Copy API formulas from spreadsheet to python
    #Pros: Fixes scalabity issues of option 2.
    #Cons: Much much much more work involved.