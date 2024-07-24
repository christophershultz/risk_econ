import pandas as pd
import numpy as np
import os, pdb, sys

def gen_key(df): 
    for col in ['Year', 'State ANSI', 'County ANSI']: 
        df[col] = [int(i) for i in df[col]]
    df['key'] = [str(df['Year'][i]) + '-' + str(df['State ANSI'][i]) + '-' + str(df['County ANSI'][i]) for i in df.index]
    return df

def getLHS(): 
    # This gets the superset of county/state/year combinations and returns it as the LHS of a data frame. 
    path = 'C://Users//cshul//Downloads//'
    files = [path + i for i in os.listdir(path) if '.csv' in i]
    res = None
    for file in files: 
        df = pd.read_csv(file)
        if res is None: res = df[['Year', 'State', 'State ANSI', 'County', 'County ANSI']]
        else: res = pd.concat([res, df[['Year', 'State', 'State ANSI', 'County', 'County ANSI']]])
    res = res.drop_duplicates().reset_index(drop = True)
    res = res[~res['State'].isin(['ALASKA', 'HAWAII'])]
    return res

def addSingles(df): 
    path = 'C://Users//cshul//Downloads//'
    files = [path + i for i in os.listdir(path) if '.csv' in i]
    files = [i for i in files if '_and_' not in i]
    
    for file in files: 
        sub = pd.read_csv(file)
        sub = sub[~sub['County ANSI'].isna()].reset_index(drop = True)
        for col in ['Year', 'State ANSI', 'County ANSI']: 
            df[col] = [int(i) for i in df[col]]
        sub = gen_key(sub)
        name = sub['Data Item'][0]
        keeps = ['key', 'Value']
        sub = sub[keeps]
        sub.columns = ['key', name]
        if len(set(sub['key'])) < len(sub): 
            pdb.set_trace()
        df = pd.merge(df, sub, how = 'left', on = 'key')
    return df

def addDoubles(df): 
    path = 'C://Users//cshul//Downloads//'
    files = [path + i for i in os.listdir(path) if '.csv' in i]
    files = [i for i in files if '_and_' in i]

    for file in files: 
        sub = pd.read_csv(file)
        sub = sub[~sub['County ANSI'].isna()].reset_index(drop = True)
        for col in ['Year', 'State ANSI', 'County ANSI']: 
            df[col] = [int(i) for i in df[col]]
        sub = gen_key(sub)

        for group in list(set(sub['Data Item'])): 
            sub2 = sub[sub['Data Item'] == group].reset_index(drop = True)
            name = sub2['Data Item'][0]
            keeps = ['key', 'Value']
            sub2 = sub2[keeps]
            sub2.columns = ['key', name]
            if len(set(sub2['key'])) < len(sub2): 
                pdb.set_trace()
            df = pd.merge(df, sub2, how = 'left', on = 'key')
    return df

def main():
    df = gen_key(getLHS()) # Create LHS and generate key

    df = addSingles(df)

    df = addDoubles(df)
    
    # Rename Columns

    colNames = ['yr', 'state', 'state_ansi', 'county', 'county_ansi', 'key', 'animal_expense_usd', 'animal_sales_usd', 
                'crop_sales_usd', 'cropland_insured_acres', 'ccc_loan_receipts_usd', 'irrigated_acres', 'fertilizer_treated_acres', 
                'conservation_acres', 'total_land_area_acres', 'operated_acres', 'num_operations', 'operations_w_sales', 'sales_usd', 
                'operations_w_income', 'farm_related_income_usd', 'gov_programs_receipts_usd', 'operations_w_gov_programs', 
                'net_income_usd_per_operation', 'net_income_usd', 'expenses_usd', 'expenses_per_operation']
    df.columns = colNames

    # Fix Column Formatting
    for col in colNames[6:]: 
        df[col] = [np.nan if '(' in str(i) else i for i in df[col]]
        df[col] = [float(str(i).replace(',', '')) for i in df[col]]

    # Derived Variables
    pdb.set_trace()

main()