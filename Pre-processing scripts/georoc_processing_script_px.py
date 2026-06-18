# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:33:15 2024

@author: naik3
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

        
data = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/2022-12-SGFTFN_PYROXENES_unprocessed.xlsx",header=0,index_col=0)
data1 = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/2022-12-SGFTFN_ORTHOPYROXENES_unprocessed.xlsx",header=0,index_col=0)
data = pd.concat([data,data1],axis=0)
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

'''
Extracting pyroxene data

'''
data2 = data[['SIO2(WT%)', 'TIO2(WT%)','AL2O3(WT%)','CR2O3(WT%)','FE2O3T(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)','FEO(WT%)', 'MNO(WT%)','MGO(WT%)','CAO(WT%)', 'NA2O(WT%)','K2O(WT%)','P2O5(WT%)','MINERAL']]
data_cleaned = data2.loc[~data2['SIO2(WT%)'].isna(),:]
data_px = data_cleaned.loc[(data_cleaned['MINERAL']=="ORTHOPYROXENE") | (data_cleaned['MINERAL']=="PYROXENE"),:]
data_px.loc[~data_px['FEOT(WT%)'].isna(),:]
data_px.pop("FE2O3(WT%)")
data_px.pop("FE2O3T(WT%)")
data_px.pop("FEO(WT%)")
data_px.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O",'P2O5','Mineral']
mineral = data_px['Mineral']
data_px = data_px.iloc[:,:-1].apply(pd.to_numeric,args=('coerce',)).astype('float')
data_px2 = data_px.fillna(0)
total = data_px2.sum(axis=1)
data_px2["Mineral"] = mineral
data_px2 = data_px2[(total>99.8) & (total<100.4)]
mineral = data_px2['Mineral']
data_px_mol = wt_to_mol(data_px2.iloc[:,:-1].to_numpy())
data_px_mol = pd.DataFrame(data_px_mol,columns=data_px2.iloc[:,:-1].columns,index=data_px2.index)
data_px_mol['Al2O3'] = data_px_mol['Al2O3'] + data_px_mol['Cr2O3']
data_px_mol.pop('Cr2O3')
data_px_mol['Mineral'] = data_px2['Mineral']
non_essential_sum = data_px_mol[["TiO2", "K2O","P2O5"]].sum(axis=1)
total_m = data_px_mol[['FeO','MnO','MgO']].sum(axis=1)
data_px_mol = data_px_mol[(non_essential_sum<2) & (total_m<53) & (data_px_mol['SiO2']>=47) & (data_px_mol['SiO2']<=70)]
total_m = data_px_mol[['FeO','MnO','MgO']].sum(axis=1)

data_opx_mol = data_px_mol.loc[(data_px_mol['SiO2']>=49.5) & (data_px_mol['SiO2']<=50.5) & (data_px_mol['Al2O3']<=1) & (total_m >=47) & (total_m <=51) & (data_px_mol['CaO']<2),:]
data_opx_mol1 = data_opx_mol.sample(n=int(0.4*len(data_opx_mol)))
data_cpx_aug_mol = data_px_mol[(data_px_mol['SiO2']>=46) & (total_m >=27) & (total_m <=48) & (data_px_mol['CaO']>2) & (data_px_mol['CaO']<=22)]
data_cpx_nonal_mol = data_px_mol[(data_px_mol['SiO2']>=49) & (total_m>=23) & (total_m<=28) & (data_px_mol['CaO']>22) & (data_px_mol['CaO']<=26)]
data_napx_mol = data_px_mol[(data_px_mol['SiO2']>=59) & (data_px_mol['Na2O']>= 10)]
data_px_mol1 = pd.concat([data_opx_mol,data_cpx_aug_mol,data_cpx_nonal_mol,data_napx_mol],axis=0)
# data_px2 = data_px2.loc[(data_px2['SiO2']>40) & (data_px2['SiO2']<65) & (total>99) & (total<101),:]
# mineral = data_px.pop("Mineral")
#%%
data_px_mol1.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/px_art_processed_mol.xlsx")


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
data_px2['Total'] = data_px2.iloc[:,:-1].sum(axis=1)
data_px2['Mineral'] = mineral
data_px2['Oxygen_no'] = 6
data_px_cat = cat_calc(data_px2, oxide)

m = data_px_cat[['Fe','Mn','Mg','Ca','Na','K']].sum(axis=1)
data_px2 = data_px2.loc[(data_px_cat['Cation_Total']>=3.995) & (data_px_cat['Cation_Total']<=4.100) & (m<=2)
                        & (data_px_cat['Si']<=2.000) & (data_px_cat['Si']>=1.500), :]

#%%

data_px_mol = wt_to_mol(data_px2.iloc[:,:-3].to_numpy())
data_px_mol = pd.DataFrame(data_px_mol,columns=data_px2.iloc[:,:-3].columns,index=data_px2.index)
data_px_mol['Al2O3'] = data_px_mol['Al2O3'] + data_px_mol['Cr2O3']
data_px_mol.pop('Cr2O3')
data_px_mol['Mineral'] = data_px2['Mineral']

total_m = data_px_mol[['FeO','MnO','MgO','CaO','Na2O','K2O']].sum(axis=1)
data_px_mol = data_px_mol.loc[total_m <=50,:]
#%%


data_px2.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/Px_partially_processed.xlsx")

data_px_mol.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/px_processed_mol.xlsx")


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