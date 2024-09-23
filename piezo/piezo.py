#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymatgen.ext.matproj import MPRester, Composition
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json
import math
import pprint
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# get data from materials project
with MPRester("8kovBjpngTHHQ1juZK") as m:
    piezo_data = m.query({"piezo": {"$exists": True}}, properties=["task_id", 
                                                                          "pretty_formula", 
                                                                          "spacegroup", 
                                                                          "band_gap", 
                                                                          "density", 
                                                                          "piezo"])
    with open('piezo-data.json', 'w') as f:
        json.dump(piezo_data, f)


# In[3]:


# load data from json file 
# with open('piezo-data.json', 'r') as f:
#     piezo_data = json.load(f)
pprint.pprint(piezo_data[4])


# In[4]:


piezo_dict = {'formula': [], 
                'space group': [], 
                'piezoelectric modulus (C/m^2)': [], 
                'density (g/cm^3)': [], 
                'band gap (eV)': []}

for i in range(len(piezo_data)):
    
    piezo_dict['formula'].append(str(piezo_data[i]['pretty_formula']) + '-' + str(piezo_data[i]['task_id'])) 
    piezo_dict['space group'].append(str(piezo_data[i]['spacegroup']['symbol']))
    piezo_dict['piezoelectric modulus (C/m^2)'].append(round(piezo_data[i]['piezo']['eij_max'], 4))
    piezo_dict['density (g/cm^3)'].append(round(piezo_data[i]['density'], 4))
    piezo_dict['band gap (eV)'].append(round(piezo_data[i]['band_gap'], 4))


# In[5]:


df = pd.DataFrame(data = piezo_dict).sort_values(by = ['piezoelectric modulus (C/m^2)'], ascending = False)
df.to_csv('piezo-data.csv', index = False)

