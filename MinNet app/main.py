#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
from joblib import load
#from randcomp import *
import streamlit as st


# In[28]:


le = load("labelencoder_01042024.pkl")
scaler = load("scaler_01042024.pkl")
model = load("model_01042024.pkl")
oxlist = ["SiO2", "TiO2", "Al2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O","P2O5","CO2"]
oxlist1 = ["SiO2", "TiO2", "Al2O3", "M", "A","P2O5","CO2"]
oxide = pd.read_excel("oxide_data.xlsx",index_col=0,sheet_name="Sheet1")
mineral_oxygen = pd.read_excel("oxide_data.xlsx",index_col=0,sheet_name="Sheet2")


# In[29]:


def clean_data(data):
    c = list(data.columns)

    if 'Total' in c:
        data.pop("Total")
    if 'Totals' in c:
        data.pop("Totals")
    if 'Sum' in c:
        data.pop("Sum")
    if 'Mineral' in c:
        act_min = data.pop('Mineral')
    if 'Minerals' in c:
        act_min = data.pop('Minerals')
    if 'Min' in c:
        act_min = data.pop('Min')
    if 'Source' in c:
        data.pop("Source")
    if 'Sources' in c:
        data.pop("Sources")
    if 'Reference' in c:
        data.pop("Reference")
    if 'References' in c:
        data.pop("References")
    data[data<0] = 0
    return data

def prep_data(data):
    c = list(data.columns)
    if 'F' in c:
        data.pop('F')
    if 'Cl' in c:
        data.pop('Cl')
    if 'F2' in c:
        data.pop('F2')
    if 'Cl2' in c:
        data.pop('Cl2')
    if "SiO2" not in c:
        data["SiO2"] = 0
    if "TiO2" not in c:
        data["TiO2"] = 0
    if "Al2O3" not in c:
        data["Al2O3"] = 0
    if "FeO" not in c:
        data["FeO"] = 0
    if "MnO" not in c:
        data["MnO"] = 0
    if "MgO" not in c:
        data["MgO"] = 0
    if "CaO" not in c:
        data["CaO"] = 0
    if "Na2O" not in c:
        data["Na2O"] = 0
    if "K2O" not in c:
        data["K2O"] = 0
    if "P2O5" not in c:
        data["P2O5"] = 0
    if "CO2" not in c:
        data["CO2"] = 0
    data_original = data.copy()
    
    if 'Cr2O3' in c:
        data["Al2O3"] = data["Al2O3"] + data["Cr2O3"]
        data.pop("Cr2O3")
    if 'ZnO' in c:
        data["FeO"] = data["FeO"] + data["ZnO"]
        data.pop("ZnO")
    if 'SrO' in c:
        data["CaO"] = data["CaO"] + data["SrO"]
        data.pop("SrO")
    if 'BaO' in c:
        data["CaO"] = data["CaO"] + data["BaO"]
        data.pop("BaO")
    if 'Li2O' in c:
        data["K2O"] = data["K2O"] + data["Li2O"]
        data.pop("Li2O")
    if 'B2O3' in c:
        data.pop("B2O3")
    return data


# In[30]:


def normalize(x):
    return x*(100/sum(x))


# In[31]:


def wt_to_mol(data, oxide = oxide):
    data=data.copy()
    data[data<0.01] = 0
    oxlist1 = list(data.columns)
    oxide1 = oxide.T[oxlist1].iloc[0, :].to_numpy()
    [r, c] = data.shape
    data = data.div(oxide1,axis=1)
    data = data.apply(normalize,axis=1)
    return data


# In[32]:


def assign_oxygen(data, mineral_oxygen):
    ox = []
    mineral = data.columns.get_loc("Mineral")
    for i in range(len(data)):
        ox.append(mineral_oxygen.loc[data.iloc[i,mineral], "Oxygen_number"])
    return(ox)


# In[33]:


def predict(data,model, scaler, le, pred_threshold = 0.9):
    data1 = data.copy()
    data1 = data1.round(1)
    data1[data1<1] = 0
    data1 = wt_to_mol(data1)
    data1 = prep_data(data1)
    data1['M'] = data1[['FeO','MnO','MgO','CaO']].sum(axis=1)
    data1['A'] = data1[['CaO','Na2O','K2O']].sum(axis=1)
    data1.pop('FeO')
    data1.pop('MnO')
    data1.pop('MgO')
    data1.pop('CaO')
    data1.pop('Na2O')
    data1.pop('K2O')
    data1['Total'] = data1.sum(axis=1)
    data1 = data1[oxlist1]
    scaled_data = scaler.transform(data1)
    data2 = data.copy()
    pred = model.predict(scaled_data)
    pred_qual = model.predict_proba(scaled_data)
    data2['Mineral'] = le.inverse_transform(pred)
    data2['Confidence'] = pred_qual.max(axis=1).round(4)*100
    data2.loc[pred_qual.max(axis=1)<pred_threshold,'Mineral'] = "??"
    return data2


# In[53]:


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


# In[12]:


# data =pd.read_excel("test_ladakh_1.xlsx",index_col=0)
st.title(':MinNet\n(automated mineral classification program)')
st.divider()
st.write("Glossary")
st.write("*Oxide-Sum threshold* refers to minimum oxide sum below which classifier will consider the analysis wrong and won't classify it")
st.write("*Mimium Prediction threshold* confidence below which classifier thinks its prediction is incorrect and will not report it")
st.divider()
st.text_input("Oxide Sum Threshold [Values between 0 and 100]", key="oxsum",value=90.0)
st.text_input("Predictive confidence Threshold [Values between 0 and 1]", key="pred_threshold",value=0.9)
st.divider()

uploaded_data = st.file_uploader("Choose a file")
if uploaded_data is not None:
    data = pd.read_excel(uploaded_data,index_col=0,header=0)
    data = clean_data(data)
    data2 = predict(data,model,scaler,le,pred_threshold=float(st.session_state.pred_threshold))
    total = data2.iloc[:,:-2].sum(axis=1)
    data2.insert(data2.columns.get_loc("Mineral"),"Total",total)
    data2.loc[data.sum(axis=1)<float(st.session_state.oxsum),'Mineral'] = "??"
    data2['Oxygen_no'] = (mineral_oxygen.loc[data2['Mineral'],"Oxygen_number"]).to_list()
    data_cat = cat_calc(data1=data2,oxide_list=oxide)
    data_final = pd.concat([data2,data_cat],axis=1)
    #dataset summarizing the number of classified minerals in a given dataset
    summary = data_final.groupby("Mineral").count().iloc[:,0].reset_index()
    summary.columns = [['Mineral','Population']]
    summary = summary.T

    #output of the two datasets
    st.divider()
    st.write("Classification Summary")
    st.write(summary)
    st.divider()
    st.write("Data Table")
    st.dataframe(data_final,use_container_width=True)
# data2.loc[data.sum(axis=1)<90,'Mineral'] = "??" 


# In[ ]:




