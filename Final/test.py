import streamlit as st
import pydeck as pdk
import pandas as pd


st.title("Blue Bike Data")
path = "/Users/ivandubinin/Library/CloudStorage/OneDrive-BentleyUniversity/CS230/Final Project/test.py/"

df_bikes = pd.read_csv(path + "current_bluebikes_stations.csv", skiprows=1)

st.dataframe(df_bikes)