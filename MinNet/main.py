#!/usr/bin/env python
# coding: utf-8

#import os

#os.chdir("C:/Users/naik3/Documents/Research/Mineral identifier ann IISER Mohali/MinNet version 2/")
#import os
#os.chdir(r"C:\Users\naik3\Desktop\Streamlit app testiing\first try")

import pandas as pd
from joblib import load
from randcomp import *
import streamlit as st


# le = load("labelencoder_01042024.pkl")
# scaler = load("scaler_01042024.pkl")
# model = load("model_01042024.pkl")

#le = load("Labeler_C3.lbl")
#scaler = load("Scaler_C3.scl")
#model = load("KNN_C3.mdl")

oxlist = ["SiO2", "TiO2", "Al2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O","P2O5","CO2"]
oxlist1 = ["SiO2", "TiO2", "Al2O3", "M", "CaO", "A","P2O5","CO2"]
oxide = pd.read_excel("MinNet/oxide_data.xlsx",index_col=0,sheet_name="Sheet1")
mineral_oxygen = pd.read_excel("oxide_data.xlsx",index_col=0,sheet_name="Sheet2")

def load_model(model,inp_comb):
    mdl = model+"_"+inp_comb+".mdl"
    scaler = 'Scaler_'+model+"_"+inp_comb+".scl"
    labeler = "Labeler_"+model+"_"+inp_comb+".lbl"
    if (inp_comb == "C4"):
        mdl = model+"_"+inp_comb+"_5_components.mdl"
        scaler = 'Scaler_'+model+"_"+inp_comb+"_5_components.scl"
        labeler = "Labeler_"+model+"_"+inp_comb+"_5_components.lbl"
    mdl = load(mdl)
    labeler = load(labeler)
    if(model != "RF"):
        scaler = load(scaler)
        return([mdl,scaler,labeler])
    else:
        scaler = None
        return([mdl,scaler,labeler])
    
def clean_data(data, type = 1):
    data = data.copy()
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

def create_model_table(data, model, scaler, input_combination):
    data1 = data[['SiO2', 'TiO2', 'Al2O3', 'FeO', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5', 'CO2']].copy()
    data1 = data1.apply(normalize, axis = 1)
    if (input_combination == "C2"):
        data1['M'] = data1[['FeO','MnO','MgO']].sum(axis=1)
        data1.pop("FeO")
        data1.pop("MnO")
        data1.pop("MgO")
        data1 = data1[["SiO2", "TiO2", "Al2O3", "M", "CaO", "Na2O", "K2O","P2O5","CO2"]]
    elif (input_combination == "C3"):
        data1['M'] = data1[['FeO','MnO','MgO']].sum(axis=1)
        data1['A'] = data1[['Na2O','K2O']].sum(axis=1)
        data1.pop("FeO")
        data1.pop("MnO")
        data1.pop("MgO")
        data1.pop("Na2O")
        data1.pop("K2O")
        data1 = data1[["SiO2", "TiO2", "Al2O3", "M", "CaO", "A","P2O5","CO2"]]
    scaled_data = data1.copy()
    if (model != "RF"):
        if (scaler is not None):
            scaled_data = scaler.transform(data1)
    
    if (input_combination == "C4"):
        pc = "PCA_" + model + "_" + input_combination + "_5_components.pc"
        pc = load(pc)
        scaled_data = pc.transform(scaled_data)

    return(scaled_data)

def normalize(x):
    return x*(100/sum(x))

def wt_to_mol(data, oxide = oxide):
    data=data.copy()
    data[data<0.01] = 0
    oxlist1 = list(data.columns)
    oxide1 = oxide.T[oxlist1].iloc[0, :].to_numpy()
    [r, c] = data.shape
    data = data.div(oxide1,axis=1)
    data = data.apply(normalize,axis=1)
    return data


def assign_oxygen(data, mineral_oxygen):
    ox = []
    mineral = data.columns.get_loc("Mineral")
    for i in range(len(data)):
        ox.append(mineral_oxygen.loc[data.iloc[i,mineral], "Oxygen_number"])
    return(ox)


def predict(data,model, inp_comb, pred_threshold = 0.9):
    data1 = data.copy()
    data1 = data1.round(1)
    data1[data1<1] = 0
    data1 = wt_to_mol(data1)
    data1 = prep_data(data1)
    # data1['M'] = data1[['FeO','MnO','MgO']].sum(axis=1)
    # data1['A'] = data1[['Na2O','K2O']].sum(axis=1)
    mdl,scaler,labeler = load_model(model,inp_comb)
    data1 = create_model_table(data1, model, scaler, input_combination=inp_comb)
    # data1.pop('FeO')
    # data1.pop('MnO')
    # data1.pop('MgO')
    # # data1.pop('CaO')
    # data1.pop('Na2O')
    # data1.pop('K2O')
    # data1['Total'] = data1.sum(axis=1)
    # data1 = data1[oxlist1]
    # if (scaler == None):
    #     scaled_data = data1.copy().to_numpy()
    # else:
    #     scaled_data = scaler.transform(data1)
    data2 = data.copy()
    pred = mdl.predict(data1)
    pred_qual = mdl.predict_proba(data1)
    # data2['Mineral'] = labeler.inverse_transform(pred)
    # data2['Confidence'] = pred_qual.max(axis=1).round(4)*100
    # data2.loc[pred_qual.max(axis=1)<pred_threshold,'Mineral'] = "??"
    mins = pd.Series(labeler.inverse_transform(pred), index = data.index)
    conf = pd.Series(pred_qual.max(axis=1).round(4)*100, index = data.index).round(2)
    data2 = pd.concat([mins,conf], axis = 1)
    data2.columns =["Prediction", "Confidence"]
    return data2

def cat_calc(data1,oxide_list):
    c = data1.columns
    if 'F' in c:
        data1.pop('F')
    if 'Cl' in c:
        data1.pop('Cl')
    if 'F2' in c:
        data1.pop('F2')
    if 'Cl2' in c:
        data1.pop('Cl2')
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


# Original app design
# st.title('MinNet\n(automated mineral classification program)')
# st.divider()
# st.write("Glossary")
# st.write("*Oxide-Sum threshold* refers to minimum oxide sum below which classifier will consider the analysis wrong and won't classify it")
# st.write("*Mimium Prediction threshold* confidence below which classifier thinks its prediction is incorrect and will not report it")
# st.divider()
# st.text_input("Oxide Sum Threshold [Values between 0 and 100]", key="oxsum",value=90.0)
# st.text_input("Predictive confidence Threshold [Values between 0 and 1]", key="pred_threshold",value=0.9)
# st.divider()
# model = pd.Series({'model':["KNN", "SVM", "RF"]})
# inp_comb = pd.Series({'inp_comb':["C1", "C2", "C3", "C4"]})
# model = st.selectbox("Select the model",model["model"], index = 0)
# inp_comb = st.selectbox("Select the Input combination",inp_comb["inp_comb"], index = 2)
# mdl,scl,lbl = load_model(model,inp_comb)
# st.divider()

#Revised 2-columns app design 19062026
st.title('MinNet\n(automated mineral classification program)')
st.divider()
st.write("Glossary")
st.write("*Oxide-Sum threshold* refers to minimum oxide sum below which classifier will consider the analysis wrong and won't classify it")
st.write("*Mimium Prediction threshold* confidence below which classifier thinks its prediction is incorrect and will not report it")
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.text_input("Oxide Sum Threshold [Values between 0 and 100]", key="oxsum",value=90.0)
    st.text_input("Predictive confidence Threshold [Values between 0 and 1]", key="pred_threshold",value=0.9)
with col2:
    st.write("Change only for testing purpose.")
    model = pd.Series({'model':["KNN", "SVM", "RF"]})
    inp_comb = pd.Series({'inp_comb':["C1", "C2", "C3", "C4"]})
    model = st.selectbox("Select the model",model["model"], index = 0)
    inp_comb = st.selectbox("Select the Input combination",inp_comb["inp_comb"], index = 2)
st.divider()


uploaded_data = st.file_uploader("Choose a file")
if uploaded_data is not None:
    data = pd.read_excel(uploaded_data,index_col=0,header=0)
    data = clean_data(data, type = 2)
    data = data.round(2)
    data1 = clean_data(data)
    pred_threshold = float(st.session_state.pred_threshold)
    data2 = predict(data1, model, inp_comb, pred_threshold= pred_threshold)
    data["Total"] = data.sum(axis=1).round(2)
    # data2.insert(data2.columns.get_loc("Prediction"),"Total",total)
    oxsum = float(st.session_state.oxsum)
    data2.loc[data.Total < oxsum,'Prediction'] = "??"
    data2['Oxygen_no'] = (mineral_oxygen.loc[data2['Prediction'],"Oxygen_number"]).to_list()
    data = pd.concat([data,data2], axis = 1)
    data_cat = cat_calc(data1=data,oxide_list=oxide)
    data_cat = data_cat.round(3)
    data_final = pd.concat([data,data_cat],axis=1)
    #dataset summarizing the number of classified minerals in a given dataset
    summary = data_final.groupby("Prediction").count().iloc[:,0].reset_index()
    summary.columns = [['Prediction','Population']]
    summary = summary.T
    data_down = data_final.to_csv(index = True).encode("utf-8")
# Output the two datasets
    st.divider()
    st.write("Classification Summary")
    st.write(summary)
    st.divider()
    st.write("Data Table")
    st.download_button(
        label = "Download",
        data = data_down,
        file_name = "MinNet output.csv",
        mime="text/csv"
        )
    st.dataframe(data_final.astype(str),width='stretch')
# data2.loc[data.sum(axis=1)<90,'Mineral'] = "??" 
