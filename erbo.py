"""
Elden Ring Build Optimizer (ERBO)
Author(s): Dylan DiSunno, Rudy DeSanti
Copyright 10/19/2022
"""
from UI_funcs import get_data
from UI_funcs import format_inputs

url_list = []
items_list = []

# pull data from API
get_data(url_list, pull = False)

# format optimizer inputs
items_list = format_inputs(accept_inputs = True)

print(items_list)