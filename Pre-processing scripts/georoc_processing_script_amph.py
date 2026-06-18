#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:54:56 2024

@author: avi
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:33:15 2024

@author: naik3
"""

import pandas as pd
import numpy as np


        
data = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/2022-12-SGFTFN_AMPHIBOLES_unprocessed.xlsx",header=0,index_col=0)
oxide = pd.read_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/oxide_data.xlsx", sheet_name="Sheet1",index_col=0,header=0)
oxlist = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O", "P2O5"]

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
Extracting amphibole as whole data

'''
data2 = data[['SIO2(WT%)', 'TIO2(WT%)','AL2O3(WT%)','CR2O3(WT%)','FE2O3T(WT%)', 'FE2O3(WT%)', 'FEOT(WT%)','FEO(WT%)', 'MNO(WT%)','MGO(WT%)','CAO(WT%)', 'NA2O(WT%)','K2O(WT%)', 'P2O5(WT%)','MINERAL']]
data_cleaned = data2.loc[~data2['SIO2(WT%)'].isna(),:]
# data_px = data_cleaned.loc[(data_cleaned['MINERAL']=="ORTHOPYROXENE") | (data_cleaned['MINERAL']=="PYROXENE"),:]
data_px = data_cleaned.copy()
data_px.loc[~data_px['FEOT(WT%)'].isna(),:]
data_px.pop("FE2O3(WT%)")
data_px.pop("FE2O3T(WT%)")
data_px.pop("FEO(WT%)")
data_px.columns = ["SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O", "P2O5",'Mineral']
mineral = data_px['Mineral']
data_px = data_px.iloc[:,:-1].apply(pd.to_numeric,args=('coerce',)).astype('float')
data_px2 = data_px.fillna(0)
total = data_px2.iloc[:,:-1].sum(axis=1)
data_px2["Mineral"] = mineral
data_px2 = data_px2.loc[(data_px2['SiO2']>35) & (data_px2['SiO2']<60) & (total>94) & (total<101),:]
mineral = data_px2.pop("Mineral")
data_px2 = pd.DataFrame(wt_to_mol(data_px2.to_numpy(),oxide),columns=data_px.columns,index=data_px2.index)
m = data_px2['FeO']+data_px2['MnO']+data_px2['MgO']
data_px2['Mineral'] = mineral

#%%

'''
extracting orthoamphibole and Fe-Mg clinoamphibole
'''
data_femg = data_px2.copy()
non_essential_sum = data_femg[["TiO2",'CaO','Na2O',"K2O","P2O5"]].sum(axis=1)
data_femg = data_femg[non_essential_sum<5]
m = data_femg[['FeO','MnO','MgO']].sum(axis=1)
data_femg = data_femg[(data_femg['SiO2']>=52) & (data_femg['SiO2']<=55) & (m>=40) & (m<=47)]
# data_femg_px2 = data_px2.loc[(data_px2['CaO']<5),:]
# data_femg = data_px2[(data_px2['Mineral']=="ANTHOPHYLLITE")|(data_px2['Mineral']=="GEDRITE")|(data_px2['Mineral']=="CUMMINGTONITE")]
# data_femg_px2 = data_femg_px2[data_femg_px2['SiO2']> ] 
# data_femg.pop("Mineral")
# data_femg1 = pd.DataFrame(wt_to_mol(data_femg.to_numpy(),oxide),columns=data_femg.columns,index=data_femg.index)
# m = data_femg1[["FeO","MnO","MgO"]].sum(axis=1)
# data_femg1 = data_femg1[(data_femg1['SiO2']>40) & (data_femg1['SiO2']<55) & (m>37) ]
data_femg['Mineral'] = "Fe-Mg Amp"

#%%
'''
extracting Ca-M clinoamphibole
'''
data_actrem = data_px2.copy()
non_essential_sum = data_actrem[['TiO2','Al2O3','Na2O',"K2O","P2O5"]].sum(axis=1)
data_actrem = data_actrem[non_essential_sum<5]
# data_actrem_px2 = data_px2[(data_px2['Mineral']=="ACTINOLITE")|(data_px2['Mineral']=="TREMOLITE")]
m = data_actrem["FeO"] + data_actrem["MnO"] + data_actrem["MgO"]
data_actrem= data_actrem[(data_actrem['SiO2']>52) & (data_actrem['SiO2']<54) & (data_actrem['CaO']>11)  & (data_actrem['CaO']<14) & (m>=32) & (m<=34)]
data_actrem['Mineral'] = "Act/Tr"

#%%

'''
extracting hornblende
'''
data_hbl = data_px2[(data_px2['Mineral']=="HORNBLENDE")|
                    (data_px2['Mineral']=="MAGNESIO-HORNBLENDE")|
                    (data_px2['Mineral']=="EDENITE")|
                    (data_px2['Mineral']=="TSCHERMAKITE") |
                    (data_px2['Mineral']=="PARGASITE") |
                    (data_px2['Mineral']=="PARGASITE") |
                    (data_px2['Mineral']=="HASTINGSITE") |
                    (data_px2['Mineral']=="MAGNESIO-HASTINGSITE") |
                    (data_px2['Mineral']=="KAERSUTITE")]
data_hbl = data_px2.copy()
non_essential_sum = data_hbl[['TiO2',"P2O5"]].sum(axis=1)
data_hbl = data_hbl[non_essential_sum<5]

# mineral = data_hbl.pop("Mineral")
# data_hbl1 = pd.DataFrame(wt_to_mol(data_hbl.to_numpy(),oxide),columns=data_hbl.columns,index=data_hbl.index)
data_hbl = data_hbl[(data_hbl['SiO2']>=48) & (data_hbl['SiO2']<=52) & (data_hbl['Al2O3']<13) & (data_hbl['CaO']>=13) & (data_hbl['CaO']<=15) & (data_hbl['Na2O']<=3)]
data_hbl['Mineral'] = "Hbl"
#%%

# '''
# extracting Kaesutite
# '''
# data_kaersutite_px2 = data_px2[(data_px2['Mineral']=="KAERSUTITE")]
# data_kaersutite_px2['Mineral'] = "Krs"
# mineral = data_kaersutite_px2.pop("Mineral")
# data_krs = pd.DataFrame(wt_to_mol(data_kaersutite_px2.to_numpy(),oxide),columns=data_kaersutite_px2.columns,index=data_kaersutite_px2.index)
# m = data_krs[["FeO","MnO","MgO"]].sum(axis=1)
# data_krs = data_krs[(data_krs['SiO2']>40) & (data_krs['SiO2']<43) & (data_krs['Al2O3']>6) & (data_krs['CaO']>13) & (m>=26)]
# data_krs["Mineral"]="Krs"

#%%
'''
extracting Na-Amp data
'''
# data_namp = data_px2[(data_px2['Mineral']=="GLAUCOPHANE") | (data_px2['Mineral']=="RIEBECKITE") | 
#                      (data_px2['Mineral']=="RICHTERITE") | 
#                      (data_px2['Mineral']=="ARFVEDSONITE") | 
#                      (data_px2['Mineral']=="MAGNESIOARFVEDSONITE") |
#                      (data_px2['Mineral']=="KATAPHORITE")]

data_namp = data_px2.copy()
# mineral = data_namp.pop("Mineral")
non_essential_sum = data_namp[['TiO2',"P2O5"]].sum(axis=1)
data_namp = data_namp[non_essential_sum<5]
# data_namp1 = pd.DataFrame(wt_to_mol(data_namp.to_numpy(),oxide),columns=data_namp.columns,index=data_namp.index)
data_namp = data_namp[(data_namp['SiO2']>=49.5) & (data_namp['SiO2']<=62) & (data_namp['Na2O']<=12.2) & (data_namp['Na2O']>=6)]
data_namp['Mineral'] = "Na-Amp"

#%%

data_amp = pd.concat([data_femg,data_actrem,data_hbl,data_namp],axis=0) 
data_amp['Al2O3'] = data_amp['Al2O3'] + data_amp['Cr2O3']
data_amp.pop("Cr2O3")
data_amp = data_amp[data_amp['K2O']<9]

data_amp.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/Amp1_processed_mol.xlsx")

 #%%
# def cat_calc(data1,oxide_list):
#     total = data1.columns.get_loc("Total")
#     o_no = data1.loc[:,"Oxygen_no"]
#     data = data1.iloc[:,:total].copy()
#     oxide = oxide_list.loc[data.columns]
#     data = data.div(oxide['Mol. Wt.'].values,axis=1).round(3)
#     data = data.mul(oxide['O_no'].values,axis=1).round(3)
#     norm = o_no.div(data.sum(axis=1)).round(3)
#     data = data.mul(norm.values,axis=0).round(3)
#     data = data.mul(oxide['Cat_per_o'].values,axis=1).round(3)
#     total = data.sum(axis=1).round(3)
#     data.columns = oxide['Cation'].values
#     data['Cation_Total'] = total
#     return data.round(3)

# mineral = data_px2['Mineral']
# data_px2.pop("Mineral")
# data_px2['Total'] = data_px2.iloc[:,:-1].sum(axis=1)
# data_px2['Mineral'] = mineral
# data_px2['Oxygen_no'] = 6
# data_px_cat = cat_calc(data_px2, oxide)

# m = data_px_cat[['Fe','Mn','Mg','Ca','Na','K']].sum(axis=1)
# data_px2 = data_px2.loc[(data_px_cat['Cation_Total']>=3.995) & (data_px_cat['Cation_Total']<=4.100) & (m<=2)
#                         & (data_px_cat['Si']<=2.000) & (data_px_cat['Si']>=1.500), :]

# # #%%
# # data_px2 = data_amp.copy()
# # data_px_mol = wt_to_mol(data_px2.iloc[:,:-1].to_numpy())
# # data_px_mol = pd.DataFrame(data_px_mol,columns=data_px2.iloc[:,:-1].columns,index=data_px2.index)
# # data_px_mol['Al2O3'] = data_px_mol['Al2O3'] + data_px_mol['Cr2O3']
# # data_px_mol.pop('Cr2O3')
# # data_px_mol['Mineral'] = data_px2['Mineral']

# # # total_m = data_px_mol[['FeO','MnO','MgO','CaO','Na2O','K2O']].sum(axis=1)
# # data_px_mol = data_px_mol.loc[data_px_mol["CaO"]<15,:]
# #%%


# data_amp.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/Amp_partially_processed.xlsx")

# data_amp.to_excel(r"/home/avi/Documents/Research/Mineral identifier ann IISER Mohali/new random comp generator/GEOROC data/processed minerals/molar tables/new data/Amp1_processed_mol.xlsx")


# #%%    

# '''
# data_cleaned_mol = wt_to_mol(data_cleaned2.iloc[:,:-2].to_numpy())
# data_cleaned_mol = pd.DataFrame(data_cleaned_mol,index=data_cleaned2.index,columns=data_cleaned2.iloc[:,:-2].columns)
# data_cleaned_mol.to_excel(r"C:\Users\naik3\Documents\Research\Mineral identifier ann IISER Mohali\new random comp generator\GEOROC data\processed minerals\molar tables\amph_georoc_processed_mol.xlsx")

# '''
# #%%

# '''
# data_cleaned1.to_excel(r"C:\Users\naik3\Documents\Research\Mineral identifier ann IISER Mohali\new random comp generator\GEOROC data\processed minerals\amph_georoc_partiallyprocessed1.xlsx")
# '''