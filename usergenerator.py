import pandas as pd
import uuid
import requests 
import random
import string
import pycountry
import time 

letters = string.ascii_lowercase
c = list(pycountry.countries)[0]
print(len(pycountry.countries))
print(c)
print(c.alpha_2)
names = []
ids = []
countries = []
points = []
for i in range(10000):
	names.append(''.join(random.choice(letters) for i in range(5)))
	ids.append(uuid.uuid1())
	points.append(random.randint(0, 10000))
	index = random.randint(1,240)
	countries.append(list(pycountry.countries)[index].alpha_2)
dic = {"scores": points, "country": countries, "user_id": ids, "display_name": names}

df = pd.DataFrame(dic, columns = ['scores', 'country', "user_id", "display_name"])
#print(df.head())
#df = df.sort_values(by=['scores'])
df['rank'] = df['scores'].rank(method="min", ascending=False)
df.to_csv('dataset.csv')
print(df.loc[df['scores'] == 0])
print(df.head())
