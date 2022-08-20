"""
Elden Ring Build Optimizer:
Author(s): Dylan DiSunno, Rudy DeSanti

project goals:
    1. min-max stats to user selected weapon
    2. talismans
    3. armor
"""

import requests
import pandas as pd

url = "https://github.com/ddisunno/Elden-Ring-Optimizer.git"

requests.get(url)
print(requests.status_code)
