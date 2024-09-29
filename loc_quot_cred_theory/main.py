import pandas as pd
import numpy as np
import os, pdb, sys, pickle

path = 'C://Users//cshul//Desktop//LQ//output//'

def get_lq(df): 
    # Compute Standard LQ
    df['LQnum'] = (df['ESTAB_C']/df['ESTAB_TOTAL_C'])
    df['LQden'] = (df['ESTAB_US']/df['ESTAB_TOTAL_US'])
    df['LQ'] = df['LQnum']/df['LQden']
    return df

def get_lq_new(df): 
    # Compute the LQ_new with marginal increase
    df['ESTAB_C_PLUS'] = df['ESTAB_C'] + 1
    numIndustries = len(set(df['NAICS'])) ## 86 for the 3-digit NAICS case
    df['ESTAB_TOTAL_C_PLUS'] = df['ESTAB_TOTAL_C'] + numIndustries
    df['LQnum_new'] = (df['ESTAB_C_PLUS']/df['ESTAB_TOTAL_C_PLUS'])
    df['LQ.new'] = df['LQnum_new'] / df['LQden']
    return df

def get_diff_sq(df): 
    df['DiffSq'] = (df['LQ']-df['LQ.new'])**2
    return df

def get_epv(df): 
    # This is the within region variance of proportions
    vars_list = [] 
    for region in set(df['GEOID']): 
        sub = df[df['GEOID'] == region]
        # Compute the proportion of each industry within each region.
        pir = sub['LQnum'] # LQnum is equivalent to this proportion
        # For each region, compute the variance of these proportions. 
        vars_list.append(np.var(pir))
    # Across regions, EPV is the average of these variances.
    df['epv'] = np.nanmean(vars_list) 
    return df

def get_vhm(df): 
    # This is the across region variance of proportions
    vars_list = [] 
    for indust in set(df['NAICS']): 
        sub = df[df['NAICS'] == indust]
        # Compute the average proportion of this industry across regions
        avgPir = np.nanmean(sub['LQnum'])
        # What's the variance of this outcome across all regions? 
        su = np.sum([(sub['LQnum'][i] - avgPir)**2 for i in sub.index])
        vars_list.append(su)
    # Across industries, VHM is the average of these variances
    df['vhm'] = np.nanmean(vars_list)
    return df

def main(): 
    df = pd.read_excel(path + 'lq_paper_us_county_2017.xlsx')
    df = get_lq(df)
    df = get_lq_new(df)
    df = get_diff_sq(df)
    df = get_epv(df)
    df = get_vhm(df)
    df['k'] = df['epv']/df['vhm']
    df['Zr'] = df['ESTAB_TOTAL_C']/(df['ESTAB_TOTAL_C'] + df['k'])
    pdb.set_trace()

main()