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
#authorization
gc = pygsheets.authorize(service_file='eldenring/elden-ring-build-optimizer-c393835be6d1.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Elden Ring Weapon Calculator 2')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(1,1))
