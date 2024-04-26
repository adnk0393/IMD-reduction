import numpy as np
import pandas as pd
import os

os.chdir(os.path.abspath( os.path.dirname( __file__ ) )) #change the current working directory to location of the script

# data to be returned in the format SiO2, TiO2, Al2O3, FeO, MnO, MgO, CaO, Na2O, K2O

oxide = pd.read_excel("oxide_data.xlsx", sheet_name="Sheet1",index_col=0,header=0)

oxlist = ["SiO2", "TiO2", "Al2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "K2O"]


def convert_to_wt(data, oxide = oxide):
    data[data<0] = 0
    oxide = oxide.T[oxlist].iloc[0, :].to_numpy()
    data = normalize(data)
    [r, c] = data.shape
    data_f = np.empty((r, c))
    for i in range(0, c):
        data_f[:, i] = data[:, i] * oxide[i]
    data_f = normalize(data_f)
    return(data_f.round(2))


def normalize(data):
    [r, c] = data.shape
    a = data.sum(axis=1).reshape((len(data), 1))
    data_formatted = ((data*100)/a).round(1)
    return(data_formatted)

def addnoise(data,threshold = 1):
    data = normalize(data)
    [r, c] = data.shape
    noise = np.random.uniform(0, threshold, (r, c)).round(3)
    data_f = normalize(data+noise)
    return(data_f)

def create_model_table(inpdata):
    nak = inpdata[:, 7:9].sum(axis=1)
    nakca = inpdata[:, 6:9].sum(axis=1)
    femgmn = inpdata[:, 3:6].sum(axis=1)
    femgmnca = inpdata[:, 3:7].sum(axis=1)
    al = inpdata[:, 2]
    si = inpdata[:, 0]
    amal = (al-nak)/(al+nak+ 0.00000000001)
    alsi = (si-al)/(si+al + 0.00000000001)
    am2 = (nakca - femgmnca) / (nakca + femgmnca + 0.00000000001)
    am2 = np.nan_to_num(am2)
    inpdata1 = np.column_stack((inpdata[:, 0:3], femgmnca, nak, alsi,am2,amal))
    return(inpdata1)

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

def wt_to_mol_table(data1, oxide1 = oxide):
    data = data1.copy()
    data[data<=2] = 0
    oxlist1 = list(data.columns)
    oxide = oxide1.T[oxlist1]
    data.divide(oxide.iloc[0,:])
    if 'Cr2O3' in list(data.columns):
        data["Al2O3"] = data["Al2O3"] + data["Cr2O3"]
        data.pop("Cr2O3")
    if 'Fe2O3' in list(data.columns):
        data["Al2O3"] = data["Al2O3"] + data["Fe2O3"]
        data.pop("Fe2O3")
    if 'ZnO' in list(data.columns):
        data["FeO"] = data["FeO"] + data["ZnO"]
        data.pop("ZnO")
    data_f = normalize(data.to_numpy())
    return(data_f.round(2))

def gt_endmember(data,significant_digit=1):
    x = data.copy()
    y = 1
    if 'Fe3' not in x.index:
      y = 0
      x['Fe3'] = 0
    if 'Cr' not in x.index:
      y = 0 
      x['Cr'] = 0 
    fe = x['Fe']
    al = x['Al']
    si = x['Si']
    mg = x['Mg']
    mn = x['Mn']
    ca = x['Ca']
    fe3 = x['Fe3']
    cr = x['Cr']
    aliv=0
    if si<=3:
        aliv = 3 - si
    alvi = al - aliv
    alm = round((fe/(fe+mg+mn+ca))*100,significant_digit)
    prp = round((mg/(fe+mg+mn+ca))*100,significant_digit)
    sps = round((mn/(fe+mg+mn+ca))*100,significant_digit)
    uv = round((cr/(alvi+cr+fe3))*100,significant_digit)
    adr = round((fe3/(alvi+cr+fe3))*100,significant_digit)
    xca = (ca/(fe+mg+mn+ca))*100
    grs = round((xca-(adr + uv)),significant_digit-1)
    comp = "Prp("+str(prp)+") Alm("+str(alm)+") Grs("+str(grs)+") Uv("+str(uv)+") Adr("+str(adr)+") Sps("+str(sps)+")"
    return comp

def ol_endmember(data,significant_digit=1):
    x = data.copy()
    fe = x['Fe'] 
    mg = x['Mg']
    fo = round((mg/(mg+fe))*100,significant_digit)
    fa = round((fe/(mg+fe))*100,significant_digit)
    comp = "Fo("+str(fo)+") Fa("+str(fa)+")"
    return comp

def px_endmember(data,significant_digit=1):
    x = data.copy()
    fe = x['Fe'] 
    mg = x['Mg']
    ca = x['Ca']
    en = round((mg/(mg+fe+ca))*100,significant_digit)
    fs = round((fe/(mg+fe+ca))*100,significant_digit)
    wo = round((ca/(mg+fe+ca))*100,significant_digit)
    comp = "En("+str(en)+") Fs("+str(fs)+") Wo("+str(wo)+")"
    return comp

def fs_endmember(data,significant_digit=1):
    x = data.copy()
    k = x['K'] 
    na = x['Na']
    ca = x['Ca']
    ort = round((k/(ca+na+k)*100),significant_digit)
    ab = round((na/(ca+na+k))*100,significant_digit)
    an = round((ca/(ca+na+k))*100,significant_digit)
    comp = "An("+str(an)+") Ab("+str(ab)+") Or("+str(ort)+")"
    return comp

def ilm_endmember(data,significant_digit=1):
    x = data.copy()
    fe = x['Fe'] 
    mg = x['Mg']
    mn = x['Mn']
    ilm = round((fe/(mg+fe+mn))*100,significant_digit)
    gk = round((mg/(mg+fe+mn))*100,significant_digit)
    pph = round((mn/(mg+fe+mn))*100,significant_digit)
    comp = "Ilm("+str(ilm)+") Gk("+str(gk)+") Pph("+str(pph)+")"
    return comp

def sp_endmember(data,significant_digit=1):
    x = data.copy()
    if "Zn" not in x.index:
        x['Zn'] = 0
    if "Mn" not in x.index:
        x['Mn'] = 0
    fe = x['Fe'] 
    mg = x['Mg']
    mn = x['Mn']
    zn = x['Zn']
    sp = round((mg/(mg+fe+mn+zn))*100,significant_digit)
    hc = round((fe/(mg+fe+mn+zn))*100,significant_digit)
    glx = round((mn/(mg+fe+mn+zn))*100,significant_digit)
    ghn = round((zn/(mg+fe+mn+zn))*100,significant_digit)
    comp = "Sp("+str(sp)+") Hc("+str(hc)+") Glx("+str(glx)+") Ghn("+str(ghn)+")"
    return comp

def ferromag_mineral(data):
    x = data.copy()
    fe = x['Fe'] 
    mg = x['Mg']
    XMg = round((mg/(mg+fe)),2)#*100
    XFe = round((fe/(mg+fe)),2)#*100
    return(XFe,XMg)

def endmember_calc(data):
    m = data.columns.get_loc("Mineral")
    data['X(Fe)'] = np.nan
    data['X(Mg)'] = np.nan
    data['Endmember Composition'] = np.nan
    c = data.columns.get_loc("Endmember Composition")
    xfe = data.columns.get_loc("X(Fe)")
    xmg = data.columns.get_loc("X(Mg)")
    for i in range(len(data)):
        if data.iloc[i,m] == "gt":
            data.iloc[i,c] = gt_endmember(data.iloc[i,:])
        elif data.iloc[i,m] == "ol":
            data.iloc[i,c] = ol_endmember(data.iloc[i,:])
        elif data.iloc[i,m] == "ilm":
            data.iloc[i,c] = ilm_endmember(data.iloc[i,:])
        elif data.iloc[i,m] == "sp":
            data.iloc[i,c] = sp_endmember(data.iloc[i,:])
        elif (data.iloc[i,m] == "opx") or (data.iloc[i,m] == "cpx"):
            data.iloc[i,c] = px_endmember(data.iloc[i,:])
        elif (data.iloc[i,m] == "kfs") or (data.iloc[i,m] == "pl"):
            data.iloc[i,c] = fs_endmember(data.iloc[i,:])
        elif (data.iloc[i,m] == "bi") or (data.iloc[i,m] == "chl") or (data.iloc[i,m] == "st") or (data.iloc[i,m] == "ctd") or (data.iloc[i,m] == "cd") or (data.iloc[i,m] == "Li-ph") or (data.iloc[i,m] == "znw"):
            data.iloc[i,xfe],data.iloc[i,xmg] = ferromag_mineral(data.iloc[i,:])
    return(data)

def rename_minerals(data):
    data = data.copy()
    min_name = pd.read_excel("oxide_data.xlsx", sheet_name="Sheet2",index_col=0,header=0)
    ox = min_name.reset_index()
    ox = ox.set_index("Mineral")
    x = []
    for i in range(len(data)):
        x.append(ox.loc[data.iloc[i,:]['Mineral'],'Abbreviations(WH2010)'])
    return(x)

def fullname_minerals(data):
    data = data.copy()
    min_name = pd.read_excel("oxide_data.xlsx", sheet_name="Sheet2",index_col=0,header=0)
    ox = min_name.reset_index()
    ox = ox.set_index("Mineral")
    x = []
    for i in range(len(data)):
        x.append(ox.loc[data.iloc[i,:]['Mineral'],'Fullname'])
    return(x)        