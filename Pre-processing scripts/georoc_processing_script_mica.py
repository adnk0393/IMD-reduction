# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:33:15 2024

@author: naik3
"""

import pandas as pd
import numpy as np


        
data = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/2022-12-SGFTFN_MICA_unprocessed.xlsx",header=0,index_col=0)
oxide = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/oxide_data.xlsx", sheet_name="Sheet1",index_col=0,header=0)
oxlist = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O"]

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
Extracting muscovite-paragonite data

'''
data2 = data[['SIO2(WT%)', 'TIO2(WT%)','AL2O3(WT%)','CR2O3(WT%)','FE2O3T(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)','FEO(WT%)', 'MNO(WT%)','MGO(WT%)','CAO(WT%)', 'NA2O(WT%)','K2O(WT%)','MINERAL']]
data_cleaned = data2.loc[~data2['SIO2(WT%)'].isna(),:]
data_mica = data_cleaned.loc[(data_cleaned['MINERAL']=="MUSCOVITE") | (data_cleaned['MINERAL']=="PARAGONITE") | (data_cleaned['MINERAL']=='PHENGITE')\
                             | (data_cleaned['MINERAL']=='PHENGITE-MUSCOVITE'),:]
data_mica.loc[~data_mica['FEOT(WT%)'].isna(),:]
data_mica.pop("FE2O3(WT%)")
data_mica.pop("FE2O3T(WT%)")
data_mica.pop("FEO(WT%)")
data_mica.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O",'Mineral']
data_mica2 = data_mica.apply(pd.to_numeric,args=('coerce',)).astype('float')
data_mica2 = data_mica2.fillna(0)
data_mica2["Mineral"] = data_mica["Mineral"]
m = data_mica2[['FeO','MnO','MgO']].sum(axis=1)
total = data_mica2.iloc[:,:-1].sum(axis=1)
data_mica2 = data_mica2[(data_mica2.SiO2 >=44) & (data_mica2.Al2O3 >=30) & (data_mica2.Al2O3 <=39) & (data_mica2.K2O + data_mica2.Na2O >=9.8) & (m<6) & (total>92)]
# data_mica2 = data_mica2.loc[data_mica2['Al2O3']>20,:]

data_mica_mol = wt_to_mol(data_mica2.iloc[:,:-1].to_numpy())
data_mica2.to_excel(r"C:\Users\naik3\Documents\Research\Mineral identifier ann IISER Mohali\new random comp generator\GEOROC data\musco_paragonite_partially_processed.xlsx")
data_mica_mol = pd.DataFrame(data_mica_mol,columns=data_mica.iloc[:,:-1].columns,index=data_mica2.index)
data_mica_mol['Al2O3'] = data_mica_mol['Al2O3'] + data_mica_mol['Cr2O3']
data_mica_mol.pop('Cr2O3')
data_mica_mol['Mineral'] = data_mica2['Mineral']
data_mica_mol.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/muscovite_processed_mol.xlsx")


#%%

'''
Extracting biotite data

'''
data2 = data[['SIO2(WT%)', 'TIO2(WT%)','AL2O3(WT%)','CR2O3(WT%)','FE2O3T(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)','FEO(WT%)', 'MNO(WT%)','MGO(WT%)','CAO(WT%)', 'NA2O(WT%)','K2O(WT%)','MINERAL']]
data_cleaned = data2.loc[~data2['SIO2(WT%)'].isna(),:]
data_mica = data_cleaned.loc[(data_cleaned['MINERAL']=="PHLOGOPITE") | (data_cleaned['MINERAL']=="BIOTITE") | (data_cleaned['MINERAL']=='ANNITE'),:]
data_mica = data_mica.loc[~data_mica['FEOT(WT%)'].isna(),:]
data_mica.pop("FE2O3(WT%)")
data_mica.pop("FE2O3T(WT%)")
data_mica.pop("FEO(WT%)")
data_mica2 = data_mica.apply(pd.to_numeric,args=('coerce',)).astype('float')
data_mica2 = data_mica2.fillna(0)
total = data_mica2.sum(axis=1)
m = data_mica2[['']]
data_mica2['MINERAL'] = data_mica['MINERAL']
data_mica2.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O",'Mineral']
# data_mica2 = data_mica2.loc[(data_mica2['Al2O3']>8) & (data_mica2['Al2O3']<26) & (total>93),:]
# data_mica2 = data_mica2.loc[data_mica2['K2O']>7,:]
data_mica_mol = wt_to_mol(data_mica2.iloc[:,:-1].to_numpy())
# data_mica2.to_excel(r"C:\Users\naik3\Documents\Research\Mineral identifier ann IISER Mohali\new random comp generator\GEOROC data\biotite_partially_processed.xlsx")
data_mica_mol = pd.DataFrame(data_mica_mol,columns=data_mica2.iloc[:,:-1].columns,index=data_mica2.index)
data_mica_mol["Mineral"] = data_mica2['Mineral']
m = data_mica_mol[['FeO','MnO','MgO']].sum(axis=1)
data_mica_mol = data_mica_mol.loc[(data_mica_mol['SiO2']>32) &(data_mica_mol['SiO2']<44) &
                                  (data_mica_mol['Al2O3']>8) & (data_mica_mol['Al2O3']<26) 
                                  & (m>32) & (m<44)
                                  & (data_mica_mol['K2O']>7) & (data_mica_mol['K2O']<9),:]

data_mica_mol['Al2O3'] = data_mica_mol['Al2O3'] + data_mica_mol['Cr2O3']
data_mica_mol.pop('Cr2O3')
# data_mica_mol['Mineral'] = data_mica2.iloc['Mineral']
data_mica_mol.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/biotite_processed_mol.xlsx")

# import matplotlib.pyplot as plt
# import seaborn as sns

# for i in ["SiO2"]:
#     for j in data_cleaned2.columns:
#         if j != i:
#             sns.displot(data=data_cleaned2,x=i,y=j,kind="kde")
    
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