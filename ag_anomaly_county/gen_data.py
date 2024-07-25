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
        if 'fertilizer' in file: 
            sub['keep'] = [1 if 'TOTAL' in i else 0 for i in sub['Domain Category']]
            sub = sub[sub['keep'] == 1].drop(columns = ['keep']).reset_index(drop = True)
        sub = sub[~sub['County ANSI'].isna()].reset_index(drop = True)
        for col in ['Year', 'State ANSI', 'County ANSI']: 
            df[col] = [int(i) for i in df[col]]
        sub = gen_key(sub)
        name = sub['Data Item'][0]
        keeps = ['key', 'Value']
        sub = sub[keeps]
        sub.columns = ['key', name]
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
    df['animal_expense_div_by_animal_sales'] = df['animal_expense_usd'] / df['animal_sales_usd']
    df['pct_animal_sales'] = df['animal_sales_usd'] / df['sales_usd']
    df['pct_crop_sales'] = df['crop_sales_usd'] / df['sales_usd']
    df['pct_acres_insured'] = df['cropland_insured_acres'] / df['total_land_area_acres']
    df['ccc_loan_receipts_usd'] = [0 if str(i).lower() == 'nan' else i for i in df['ccc_loan_receipts_usd']]
    df['pct_sales_ccc_loans'] = df['ccc_loan_receipts_usd'] / df['sales_usd']
    df['pct_acres_irrigated'] = df['irrigated_acres'] / df['total_land_area_acres'] 
    df['pct_acres_fertilized'] = df['fertilizer_treated_acres'] / df['total_land_area_acres']
    df['pct_acres_conserved'] = df['conservation_acres'] / df['total_land_area_acres'] 
    df['pct_acres_operated'] = df['operated_acres'] / df['total_land_area_acres'] 
    df['pct_operations_with_sales'] = df['operations_w_sales'] / df['num_operations']
    df['pct_ops_w_gov_programs'] = df['operations_w_gov_programs'] / df['num_operations']
    df['expense_ratio'] = df['expenses_usd'] / df['sales_usd']
    df['expenses_div_net_income'] = df['expenses_usd'] / df['net_income_usd']

    df.to_csv('C://Users//cshul//Desktop//risk_econ//ag_anomaly_county//prepared_data.csv', index = None)

main()