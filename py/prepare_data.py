# This .py file prepares the downloaded recipe1M data for usage by converting
# it to a sqlite3 database (.db).

import tarfile
import sqlite3
import json
import pandas as pd

# open tarfile
print("opening file...")
tar = tarfile.open("../recipe1M_layers.tar.gz")
files = tar.getmembers()

# extract recipe data into a string
print("extracting data...")
f = tar.extractfile(files[0]).read()

# convert to a python list
temp = json.loads(f)

# create DataFrame
df = pd.DataFrame()

for key in temp[0].keys():
    tempList = [temp[i][key] for i in range(0, len(temp)-1)]
    df[key] = tempList

# unpack the ingredients and instructions columns
print("unpacking recipes...")
ingr_unpacked = []
istr_unpacked = []
for i in range(0, df.shape[0]): # loop over each row
    ingr_list = []
    istr_list = []
    for ingr_dict in df['ingredients'][i]: # loop over each ingredient
        ingr_list.append(ingr_dict['text']) # add to new list
    for istr_dict in df['instructions'][i]: # repeat for instructions
        istr_list.append(istr_dict['text'])
    ingr_str = json.dumps(ingr_list) # convert to JSON string format
    istr_str = json.dumps(istr_list)
    ingr_unpacked.append(ingr_str) # add the string just constructed to another list
    istr_unpacked.append(istr_str)

df["ingredients"] = ingr_unpacked # replace columns
df["instructions"] = istr_unpacked

# convert to database
print("converting to sqlite3 database...")
conn = sqlite3.connect("../data/recipes1M.db")
df.to_sql("recipes", conn, if_exists = "replace", index = False, chunksize = 20000)

# verify success
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
if  (str(cursor.fetchall()) == "[('recipes',)]"):
    print("conversion successful!")
else:
    print("conversion unsuccessful")
    
conn.close()
print("connection closed...\nprogram complete.")