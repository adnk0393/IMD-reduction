#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:09:17 2024

@author: avi
"""

import pandas as pd
import numpy as np


        
data = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/2022-12-SGFTFN_APATITES_unprocessed.xlsx",header=0,index_col=0)
oxide = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/oxide_data.xlsx", sheet_name="Sheet1",index_col=0,header=0)
oxlist = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O","P2O5"]

def wt_to_mol(data, oxide = oxide):
    data[data<=2] = 0
    oxlist1 = oxlist.copy()
    oxide = oxide.T[oxlist1].iloc[0, :].to_numpy()
    data = normalize(data)
    [r, c] = data.shape
    data_f = np.empty((r, c))
    for i in range(0, c):
        data_f[:, i] = data[:, i] / oxide[i]
    data
    data_f = normalize(data_f)
    return(data_f.round(2))


def normalize(data):
    [r, c] = data.shape
    a = data.sum(axis=1).reshape((len(data), 1))
    data_formatted = ((data*100)/a).round(1)
    return(data_formatted)


def cat_calc(data1,oxide_list):
    total = data1.columns.get_loc("Total")
    o_no = data1.loc[:,"Oxygen_no"]
    data = data1.iloc[:,:total].copy()
    oxide = oxide_list.loc[data.columns]
    data = data.div(oxide['Mol. Wt.'].values,axis=1).round(3)
    data = data.mul(oxide['O_no'].values,axis=1).round(3)
    norm = o_no.div(data.sum(axis=1)).round(3)
    data = data.mul(norm.values,axis=0).round(3)
    data = data.mul(oxide['Cat_per_o'].values,axis=1).round(3)
    total = data.sum(axis=1).round(3)
    data.columns = oxide['Cation'].values
    data['Cation_Total'] = total
    return data.round(3)

#%%


# data1 = data.iloc[:,22:75]

# data_cleaned1 = data_cleaned.apply(pd.to_numeric,args=('coerce',)).astype('float')
# data_cleaned1 = data_cleaned1.loc[~data_cleaned1['SIO2(WT%)'].isna(),:]
# data_cleaned1.loc[(data_cleaned1["FEOT(WT%)"].isna()) & (~data_cleaned1["FE2O3T(WT%)"].isna()),"FEOT(WT%)"] = data_cleaned1.loc[(data_cleaned1["FEOT(WT%)"].isna()) & (~data_cleaned1["FE2O3T(WT%)"].isna()),"FE2O3T(WT%)"]*.8998
# data_cleaned1.loc[(data_cleaned1["FEOT(WT%)"].isna()) & (~data_cleaned1["FE2O3T(WT%)"].isna()),"FE2O3T(WT%)"] = np.nan
# data_cleaned2 = data_cleaned1.loc[~data_cleaned1['FEOT(WT%)'].isna(),:]
# data_cleaned2.pop("FE2O3(WT%)")
# data_cleaned2.pop("FE2O3T(WT%)")
# data_cleaned2.pop("FEO(WT%)")
# data_cleaned2 = data_cleaned2.loc[data_cleaned2['SIO2(WT%)']>30,:]
# data_cleaned2 = data_cleaned2.loc[data_cleaned2["SIO2(WT%)"]<=60,:]
# data_cleaned2 = data_cleaned2.loc[data_cleaned2['TIO2(WT%)']<10,:]
# data_cleaned2 = data_cleaned2.loc[data_cleaned2['CAO(WT%)']<40,:]
# data_cleaned2 = data_cleaned2.fi

# data_cleaned2.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O"]
# data_cleaned2['Total'] = data_cleaned2.sum(axis=1)
# data_cleaned2 = data_cleaned2.loc[data_cleaned2['Total']>94,:]
# data_cleaned2['Oxygen_no'] = 23
#%%

'''
Extracting pyroxene data

'''
data2 = data[['SIO2(WT%)', 'TIO2(WT%)','AL2O3(WT%)','CR2O3(WT%)','FE2O3T(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)','FEO(WT%)', 'MNO(WT%)','MGO(WT%)','CAO(WT%)', 'NA2O(WT%)','K2O(WT%)',"P2O5(WT%)",'MINERAL']]
data_cleaned = data2.loc[~data2['P2O5(WT%)'].isna(),:]
data_px = data_cleaned.loc[(data_cleaned['MINERAL']=="APATITE") | (data_cleaned['MINERAL']=="HYDROXYLAPATITE"),:]
data_px.loc[~data_px['FEOT(WT%)'].isna(),:]
data_px.pop("FE2O3(WT%)")
data_px.pop("FE2O3T(WT%)")
data_px.pop("FEO(WT%)")
data_px.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O","P2O5",'Mineral']
mineral = data_px['Mineral']
data_px = data_px.iloc[:,:-1].apply(pd.to_numeric,args=('coerce',)).astype('float')
data_px2 = data_px.fillna(0)
# total = data_px2.iloc[:,:-1].sum(axis=1)
total = data_px2.sum(axis=1)
data_px2["Mineral"] = mineral
data_px2 = data_px2.loc[(data_px2['P2O5']>35) & (data_px2['P2O5']<60) & (data_px2['CaO']>49) & (data_px2['CaO']<60) & (total>80) & (total<100.5),:]


#%%
def cat_calc(data1,oxide_list):
    total = data1.columns.get_loc("Total")
    o_no = data1.loc[:,"Oxygen_no"]
    data = data1.iloc[:,:total].copy()
    oxide = oxide_list.loc[data.columns]
    data = data.div(oxide['Mol. Wt.'].values,axis=1).round(3)
    data = data.mul(oxide['O_no'].values,axis=1).round(3)
    norm = o_no.div(data.sum(axis=1)).round(3)
    data = data.mul(norm.values,axis=0).round(3)
    data = data.mul(oxide['Cat_per_o'].values,axis=1).round(3)
    total = data.sum(axis=1).round(3)
    data.columns = oxide['Cation'].values
    data['Cation_Total'] = total
    return data.round(3)

mineral = data_px2['Mineral']
data_px2.pop("Mineral")
data_px2['Total'] = data_px2.sum(axis=1)
data_px2['Mineral'] = mineral
data_px2['Oxygen_no'] = 26
data_px_cat = cat_calc(data_px2, oxide)

m = data_px_cat[['Fe','Mn','Mg','Ca','Na']].sum(axis=1)
data_px2 = data_px2.loc[(data_px_cat['Cation_Total']>=14.90) & (data_px_cat['Cation_Total']<=17.00) & (data_px_cat['P']>=4.900)  & (data_px_cat['P']<=6.100), :]

#%%

data_px_mol = wt_to_mol(data_px2.iloc[:,:-3].to_numpy())
data_px_mol = pd.DataFrame(data_px_mol,columns=data_px2.iloc[:,:-3].columns,index=data_px2.index)
data_px_mol['Al2O3'] = data_px_mol['Al2O3'] + data_px_mol['Cr2O3']
data_px_mol.pop('Cr2O3')
# data_px_mol['Mineral'] = data_px2['Mineral']
data_px_mol['Mineral'] = "Ap"

total_m = data_px_mol[['SiO2','FeO','MnO','MgO','K2O']].sum(axis=1)
data_px_mol = data_px_mol.loc[total_m<=8,:]
#%%


data_px2.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/Ap_partially_processed.xlsx")

data_px_mol.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/Ap_processed_mol.xlsx")


#%%    

'''
data_cleaned_mol = wt_to_mol(data_cleaned2.iloc[:,:-2].to_numpy())
data_cleaned_mol = pd.DataFrame(data_cleaned_mol,index=data_cleaned2.index,columns=data_cleaned2.iloc[:,:-2].columns)
data_cleaned_mol.to_excel(r"C:\Users\naik3\Documents\Research\Mineral identifier ann IISER Mohali\new random comp generator\GEOROC data\processed minerals\molar tables\amph_georoc_processed_mol.xlsx")

'''
#%%

'''
data_cleaned1.to_excel(r"C:\Users\naik3\Documents\Research\Mineral identifier ann IISER Mohali\new random comp generator\GEOROC data\processed minerals\amph_georoc_partiallyprocessed1.xlsx")
'''