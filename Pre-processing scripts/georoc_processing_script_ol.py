#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 11:14:58 2024

@author: avi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 09:59:38 2024

@author: avi
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:33:15 2024

@author: naik3
"""

import pandas as pd
import numpy as np


        
data = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/2022-12-SGFTFN_OLIVINES_unprocessed.xlsx",header=0,index_col=0)
# data = pd.concat([data,data1],axis=0)
oxide = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/oxide_data.xlsx", sheet_name="Sheet1",index_col=0,header=0)
oxlist = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O",'P2O5']

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
Extracting olivine data

'''
data2 = data[['SIO2(WT%)', 'TIO2(WT%)','AL2O3(WT%)','CR2O3(WT%)','FE2O3T(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)','FEO(WT%)', 'MNO(WT%)','MGO(WT%)','CAO(WT%)', 'NA2O(WT%)','K2O(WT%)','P2O5(WT%)','MINERAL']]
data_cleaned = data2.loc[~data2['SIO2(WT%)'].isna(),:]
data_px = data_cleaned.loc[~pd.isna(data_cleaned['MINERAL']),:]
data_px.loc[~data_px['FEOT(WT%)'].isna(),:]
data_px.pop("FE2O3(WT%)")
data_px.pop("FE2O3T(WT%)")
data_px.pop("FEO(WT%)")
data_px.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O",'P2O5','Mineral']
mineral = data_px['Mineral']
data_px = data_px.iloc[:,:-1].apply(pd.to_numeric,args=('coerce',)).astype('float')
data_px2 = data_px.fillna(0)
total = data_px2.sum(axis=1)
data_px2['Mineral'] = mineral
data_px2 = data_px2[(total>99.93) & (total<100.01)]
mineral = data_px2.pop("Mineral")
col = data_px2.columns
ind = data_px2.index
data_px2 = pd.DataFrame(wt_to_mol(data_px2.to_numpy(),oxide),columns = col,index=ind)
data_px2['Mineral'] = mineral
# data_px2 = data
non_essential_sum = data_px2[["TiO2","Al2O3","Cr2O3","Na2O", "K2O","P2O5"]].sum(axis=1)
data_px2 = data_px2[non_essential_sum<.5]
m = data_px2[["FeO","MnO","MgO","CaO"]].sum(axis=1)
data_px2 = data_px2[ (data_px2['SiO2']>33) & (data_px2['SiO2']<34) & (m > 66) & (m < 67)]
# data_px2 = data_px2[(data_px2.TiO2 > 48) & (data_px2.TiO2 < 52)]
# data_px2['P2O5'] = 0
data_px2['Mineral'] = "Ol"
data_px2['Al2O3'] = data_px2['Al2O3'] + data_px2['Cr2O3']
data_px2.pop("Cr2O3")

#%%

mineral = data_px2['Mineral']
data_px2.pop("Mineral")
data_px2['Total'] = data_px2.iloc[:,:-1].sum(axis=1)
data_px2['Mineral'] = mineral
data_px2['Oxygen_no'] = 3
data_px_cat = cat_calc(data_px2, oxide)

m = data_px_cat[['Fe','Mn','Mg','Ca','Na','K']].sum(axis=1)
data_px2 = data_px2.loc[(data_px_cat['Cation_Total']>=1.950) & (data_px_cat['Cation_Total']<=2.100) & (m<=2)
                        & (data_px_cat['Ti']>=0.500) & (data_px_cat['Ti']<=1.000), :]
data_px2 = data_px2.loc[(data_px2['SiO2']<=2.00) & (data_px2['Al2O3']<=2.00) & (data_px2['Cr2O3']<=2.00) &(data_px2['CaO']<=2.00)
                        & (data_px2['Na2O']<=2.00) & (data_px2['K2O']<=2.00), :]

#%%

data_px_mol = wt_to_mol(data_px2.iloc[:,:-3].to_numpy())
data_px_mol = pd.DataFrame(data_px_mol,columns=data_px2.iloc[:,:-3].columns,index=data_px2.index)
data_px_mol['Al2O3'] = data_px_mol['Al2O3'] + data_px_mol['Cr2O3']
data_px_mol.pop('Cr2O3')
data_px_mol['Mineral'] = data_px2['Mineral']

total_m = data_px_mol[['FeO','MnO','MgO','CaO','Na2O','K2O']].sum(axis=1)
data_px_mol = data_px_mol.loc[total_m <=50,:]

#%%


# data_px2.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/Ilm_partially_processed.xlsx")


data_px2.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/ol_processed_mol.xlsx")


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