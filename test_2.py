#### RANKED LISTS ####
from tqdm import tqdm
import random


list_ = []
for i in tqdm(range(100000)):
	list_.append(random.randint(0,10))

# show distribution
print(len(list_))
for i in range(11):
	print(f"{i}:\t{round(list_.count(i)/100000, 4)}%\t{list_.count(i)}/100,000")

#challenge:
# return x% of the lists highest values