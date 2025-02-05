import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pickle
from sklearn.preprocessing import LabelEncoder
import re



"""""""""""""""""""""""""""""""""""""""""""""

# CREATING FILE FROM .txt DATA

"""""""""""""""""""""""""""""""""""""""""""""




f = open("C:/Users/gpro0/OneDrive/Рабочий стол/PROJEEEECT/ALLTHEDATA.txt", 'r')                                
a = f.read()

pattern = r"Temperature:(\d+\.\d+)\nSoil Moisture Value: (\d+)\nSensor Value: (\d+)\s*TDS \(mg/l\): (\d+\.\d+)\nCO2: (\d+)"

matches = re.findall(pattern, a)

df = pd.DataFrame(matches, columns=['TEMPERATURE', 'HUMIDITY',"Sensor Value", 'TDS', 'CO2'])

df["TEMPERATURE"] = df['TEMPERATURE'].astype(float)
df['HUMIDITY'] = df['HUMIDITY'].astype(int)
df['Sensor Value'] = df["Sensor Value"].astype(int)
df['TDS'] = df['TDS'].astype(float)
df['CO2'] = df['CO2'].astype(int)
df = df.drop("Sensor Value", axis=1)


dates = pd.date_range(start='2023-01-01', end='2023-04-10')
num_rows = len(df)
indices = np.arange(num_rows)
all_dates = np.tile(dates, int(np.ceil(num_rows/len(dates))))[:num_rows]
df.insert(0, 'DATE', all_dates)


if 'generated_data' not in st.session_state:

    df.insert(1, "N_SOIL", np.random.randint(0, 141, size=len(df)))
    df.insert(2, "P_SOIL", np.random.randint(5, 145, size=len(df)))
    df.insert(3, "K_SOIL", np.random.randint(5, 205, size=len(df)))
    df.insert(4, "ph", np.random.uniform(3.5, 10, size=len(df)))
    df.insert(5, "RAINFALL", np.random.uniform(20.2, 298.6, size=len(df)))
    crop_list = ["Rice", "Maize", "ChickPea", "KidneyBeans", 'PigeonPeas', "MothBeans", "MungBean", "Blackgram", "Lentil", "Pomegranate", "Banana", "Mango", "Grapes", "Watermelon", "Muskmelon", "Apple", "Orange", "Papaya", "Coconut", "Cotton", "Jute", "Coffee"]
    df.insert(6, "CROP", np.random.choice(crop_list, size=len(df)))
    st.session_state.generated_data = df.copy()  
else:

    df = st.session_state.generated_data


df = df.reindex(columns=["DATE","N_SOIL","P_SOIL","K_SOIL","TEMPERATURE","HUMIDITY","ph","RAINFALL","YIELD_LVL","CROP","TDS","CO2"])





df.to_csv("C:/Users/gpro0/OneDrive/Рабочий стол/PROJEEEECT/DATA_LATEST.csv")




"""""""""""""""""""""""""""""""""""""""""""""

# STREAMLIT PROGRAMM

"""""""""""""""""""""""""""""""""""""""""""""



def plot_graph(df, x, y, kind='line'):
    fig = px.line(df, x=x, y=y)
    st.plotly_chart(fig)

st.title("Data analys and prediction")

file = "C:/Users/gpro0/OneDrive/Рабочий стол/PROJEEEECT/DATA_LATEST.csv"

# uploaded_file = st.file_uploader("Upload .csv file")

if file is not None:
    df0 = pd.read_csv(file, index_col=0)
    df2 = df0.drop(columns=['YIELD_LVL'], errors='ignore')
    st.dataframe(df2)
    col = df0.select_dtypes(['object']).columns
    le=LabelEncoder()
    for i in col:
        df0[i]=le.fit_transform(df0[i])
    df0.head()

    df1 = df0.drop(columns=['YIELD_LVL', 'DATE', "CO2", "TDS"], errors='ignore')


model = pickle.load(open("C:/Users/gpro0/OneDrive/Рабочий стол/project/model.pkl", 'rb'))


if st.button("Make Yield prediction"):

    predictions = np.minimum(120.,np.maximum(0., model.predict(df1)))
    preds = pd.DataFrame()
    preds.insert(0, 'DATE', df2["DATE"])
    preds.insert(1, "PREDS", predictions)
    st.write(preds)

if st.checkbox("Build graph"):
    x_column = st.selectbox("Choose X coordinate", df0.columns)
    y_column = st.selectbox("Choose Y coordinate", df0.columns)
    # plot_graph(df0.iloc[100:200], x_column, y_column)
    plot_graph(df0[0:100], x_column, y_column)
