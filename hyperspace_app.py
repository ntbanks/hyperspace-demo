import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
import pickle
from pickle import load
from keras.models import load_model
import keras
from sklearn.preprocessing import StandardScaler

from time import sleep

@st.cache
def get_dfval_frame():
    with sqlite3.connect('turbofandata.db') as connection:
        dfval_new = pd.read_sql('SELECT * from dfval_notime', connection)
        return dfval_new
    
@st.cache
def load_saved_model():
    model = load_model('model_notime.h5')
    

@st.cache
def load_scaler():
    scaler_xtrain = load(open('scaler_xtrain_notime.pkl','rb'))
    
dfval = get_dfval_frame()
#model = load_saved_model()
model = load_model('model_notime.h5')
#scaler_xtrain = load_scaler()
scaler_xtrain = load(open('scaler_xtrain_notime.pkl','rb'))
#st.write(f'{type(model)} : {type(dfval)} : {type(scaler_xtrain)}')
input_cols = ['setting_1', 'setting_2', 'setting_3', 's_1', 
              's_2', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8',
              's_9', 's_10', 's_11', 's_12', 's_13', 's_14',
              's_15', 's_16', 's_17', 's_18', 's_19', 's_20', 's_21']

st.title("Realtime Survival Curve Prediction for Streaming Data")
sats = tuple(dfval['id'].unique())
sat = st.sidebar.selectbox('Select Satellite', sats)


dfsat = dfval[dfval['id']==sat]
dfsat.reset_index(inplace=True)
# treat each row as a separate input; loop through the index
# can even set the time.sleep function argument as a parameter
# in the app

def get_single_hazard(params:dict,
                     scaler_xtrain, clf):
    """takes a single sample of data in the form of a dictionary and 
    returns the hazard function predicted by the model clf."""
    db = pd.DataFrame(params.values(), index=b.keys()).T[input_cols]
    X = scaler_xtrain.transform(db.to_numpy())
    hazard = clf.predict(X)
    return hazard

survival_curve = [1]

def get_single_hazard(params:dict,
                     scaler_xtrain, clf):
    """takes a single sample of data in the form of a dictionary and 
    returns the hazard function predicted by the model clf."""
    db = pd.DataFrame(params.values(), index=b.keys()).T[input_cols]
    X = scaler_xtrain.transform(db.to_numpy())
    hazard = clf.predict(X)
    survival_curve.append(survival_curve[-1]*(1 - hazard[0][0]))
    return hazard


for i in dfsat.index:
    b = dfsat.iloc[i].to_dict()
    h = get_single_hazard(b, scaler_xtrain, model)
    print(survival_curve[-1])
    sleep(.8)
    
    
