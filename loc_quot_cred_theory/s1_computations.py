import pandas as pd
import numpy as np
import os, pdb, sys

path = os.getcwd() + '\\loc_quot_cred_theory\\prepared_data_2022.csv'

def compute_lq(su, df): 
    lq = [] 
    for i in su.index: 
        ind = su['naics'][i]
        sta = su['state_fips'][i]
        cty = su['cty_fips'][i]

        # Numerator X_ir / X_r
        tmp = su[su['naics'] == ind]
        tmp = tmp[tmp['cty_fips'] == cty].reset_index(drop = True)
        xir = tmp['establishments'][0] if len(tmp) > 0 else 0 

        tmp = su[su['cty_fips'] == cty]
        xr = sum(tmp['establishments'])

        # Denominator X_iN / X_N 
        tmp = df[df['naics'] == ind]
        xiN = sum(tmp['establishments'])
        xN = sum(df['establishments'])

        lq.append((xir/xr) / (xiN/xN))
    su['lq'] = lq
    return su

def compute_adj_lq(su, df): 
    lq_adj= [] 
    for i in su.index: 
        ind = su['naics'][i]
        sta = su['state_fips'][i]
        cty = su['cty_fips'][i]

        # Numerator X_ir / X_r
        tmp = su[su['naics'] == ind]
        tmp = tmp[tmp['cty_fips'] == cty].reset_index(drop = True)
        xir = tmp['establishments'][0] if len(tmp) > 0 else 0 
        xir += 1

        tmp = su[su['cty_fips'] == cty]
        xr = sum(tmp['establishments'])
        xr += 1

        # Denominator X_iN / X_N 
        tmp = df[df['naics'] == ind]
        xiN = sum(tmp['establishments']) + 1
        xN = sum(df['establishments']) + 1

        lq_adj.append((xir/xr) / (xiN/xN))
    su['lq_adj'] = lq_adj
    return su

def compute_stability(su, df): 
    su['stab'] = [np.abs(su['lq'][i] - su['lq_adj'][i]) for i in su.index]
    return su

def cred_theory(su, df): 
    pdb.set_trace()

def recompute_stability(su, df): 
    pdb.set_trace()

def main(): 
    df = pd.read_csv(path)
    df['keeps'] = [1 if (i[-4:] == '----' and i[:2] != '--') else 0 for i in df['naics']]
    df = df[df['keeps'] == 1].reset_index(drop = True)

    res = {} 
    for region in set(df['state']): 
        su = df[df['state'] == region].reset_index(drop = True)

        # Compute LQ
        su = compute_lq(su, df)

        # Compute Adj LQ
        su = compute_adj_lq(su, df)
        
        # Compute Stability Measure
        su = compute_stability(su, df)

        # Compute Cred-Theory-Adj LQ
        su = cred_theory(su, df)

        # Recompute Stability Measure
        su = recompute_stability(su, df)

        pdb.set_trace()


main()