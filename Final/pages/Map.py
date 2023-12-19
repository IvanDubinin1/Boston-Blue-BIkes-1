import streamlit as st
import pydeck as pdk
import pandas as pd


path = "/Users/ivandubinin/Library/CloudStorage/OneDrive-BentleyUniversity/CS230/Final312/Final/"

st.title("Adjustable Map of Blue Bikes")

df_bikes = pd.read_csv(path + "current_bluebikes_stations.csv", skiprows=1)
df_bikes['District'].fillna('Unknown', inplace=True)
df_bikes1 = df_bikes[['Number', 'Name', 'Latitude', 'Longitude', 'District', 'Public', 'Total docks', 'Deployment Year']]



districts = df_bikes['District'].unique()
default_district = ['Boston']
selected_districts = st.sidebar.multiselect("Select Districts", districts, default=default_district)
filtered_df = df_bikes[df_bikes['District'].isin(selected_districts)]
filtered_df1 = filtered_df[['Number', 'Name', 'Latitude', 'Longitude', 'District', 'Public', 'Total docks', 'Deployment Year']]


min_docks = int(filtered_df['Total docks'].min())
max_docks = int(filtered_df['Total docks'].max())

dock_range = st.sidebar.slider("Select Range of Total Docks", min_docks, max_docks, (min_docks, max_docks))

# Filter the DataFrame based on the selected range of total docks
filtered_by_docks_df = filtered_df[
    (filtered_df['Total docks'] >= dock_range[0]) & (filtered_df['Total docks'] <= dock_range[1])
]
filtered_by_docks_df1 = filtered_by_docks_df[['Number', 'Name', 'Latitude', 'Longitude', 'District', 'Public', 'Total docks', 'Deployment Year']]



filtered_by_docks_df.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'}, inplace=True)


scatterplot = pdk.Layer(
    'ScatterplotLayer',
    data=filtered_by_docks_df,
    get_position='[LON, LAT]',
    get_color=[200, 30, 0, 160],
    get_radius=100,
    pickable=True,
    stroked=True,
    filled=True,
)

# Set the initial viewport location
view_state = pdk.ViewState(
    longitude=filtered_by_docks_df['LON'].mean(),
    latitude=filtered_by_docks_df['LAT'].mean(),
    zoom=10
)


st.write("Map with Points based on Latitude and Longitude:")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v11',
    layers=[scatterplot],
    initial_view_state=view_state,
    tooltip={"text": "{Name}\n{District}"}
))
expand_text = st.checkbox("Map Description")


if expand_text:
    st.write("This map shows the plotted points for the BlueBikes associated with the selected District and the selected total range of docks.")
else:
    st.write("Map Description (click to expand)")



selected_tab = st.sidebar.selectbox("Select Tab", ["Original DataFrame", "DataFrame Filtered by District", "DataFrame Filtered by District and Total Docks"])


if selected_tab == "DataFrame Filtered by District":
    st.write("DataFrame Filtered by District:")
    st.write(filtered_df1)
elif selected_tab == "DataFrame Filtered by District and Total Docks":
    st.write("DataFrame Filtered by District and Total Docks:")
    st.write(filtered_by_docks_df1)
elif selected_tab == "Original DataFrame":
    st.write("Original DataFrame:")
    st.write(df_bikes1)