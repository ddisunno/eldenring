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

url = "https://github.com/ddisunno/Elden-Ring-Optimizer.git"

requests.get(url)
print(requests.status_code)
