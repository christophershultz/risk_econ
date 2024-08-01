import pandas as pd
import numpy as np
import os, pdb, sys

path = 'C://Users//cshul//Downloads//'
files = [path + i for i in os.listdir(path)]
files = [i for i in files if '.csv' in i]

df = None
for f in files: 
    tmp = pd.read_csv(f)
    keeps = ['State', 'State ANSI', 'County', 'County ANSI', 'Commodity', 'Data Item', 'Domain', 'Domain Category', 'Value']
    tmp = tmp[keeps]
    name = tmp['Data Item'][0]
    tmp['key'] = [tmp['State'][i] + '-' + tmp['County'][i] for i in tmp.index]

    newVal = [] 
    for i in tmp['Value']: 
        try: 
            newVal.append(float(str(i).replace(',', '')))
        except: 
            newVal.append(np.nan)
    tmp['Value'] = newVal

    tmp = tmp[['key', 'Value']].groupby(['key']).sum().reset_index()
    tmp.columns = ['key', name]

    if df is None: df = tmp.copy(deep = True)
    else: 
        if name not in df.columns: 
            df = pd.merge(df, tmp, how = 'outer', on = 'key')

df.to_csv(os.getcwd() + '\\bm_ag_economy\\raw_data.csv', index = None)
