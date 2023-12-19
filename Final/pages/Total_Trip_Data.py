
import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd
import numpy as np
import folium
import matplotlib.pyplot as plt


path = "/Users/ivandubinin/Library/CloudStorage/OneDrive-BentleyUniversity/CS230/Final312/Final/"
st.title("Total Trip Data")
st.divider()

st.write('<span style="font-size:30px; color:#A0C8E0;">Usually Blue Bikes are not used as often in certain spots due to street dificulty, or location. The following graph will plot all of the starting station against the total number of trips started from that station. </span>', unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)
df_bikes_trip_data = pd.read_csv(path + "hubway-tripdata2.csv")
station_counts = df_bikes_trip_data['start station name'].value_counts()

# Create a horizontal bar chart
plt.figure(figsize=(8, 10))  # Set figure size

# Plotting the horizontal bar chart
station_counts.plot(kind='barh')
plt.xlabel('Number of Trips')
plt.ylabel('Start Station Name')
plt.title('Number of Trips Recorded per Start Station')


st.pyplot()


st.image("https://images.ctfassets.net/p6ae3zqfb1e3/2HkcjDwiQyGzxSaS4IgMZu/c914041107ecfa8d9abcf1b1ba022da5/MeetBike-Intro_New_Helmet_844.png", caption="Boston Blue Bikes")