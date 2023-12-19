
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(page_title='BlueBikes')

st.sidebar.success("Data Customization Bellow.")



st.title("Blue Bike Data")
st.write('<span style="font-size:30px; color:white;">Bluebikes is public transportation by bike! With more than 4,000 bikes and 400 stations, its a fast, fun, and affordable way to get around Metro Boston. Bluebikes is municipally owned and jointly managed by Boston, Brookline, Cambridge, Everett, and Somerville.</span>', unsafe_allow_html=True)
st.divider()
st.write('<span style="font-size:30px; color:#A0C8E0;">Below is the following total dataframe provided for Boston Blue bikes. It has all of the data used to create the maps and charts for the webpage.</span>', unsafe_allow_html=True)
path = "/Users/ivandubinin/Library/CloudStorage/OneDrive-BentleyUniversity/CS230/Final312/Final/"

df_bikes = pd.read_csv(path + "current_bluebikes_stations.csv", skiprows=1)


st.dataframe(df_bikes[['Number', 'Name', 'Latitude', 'Longitude', 'District', 'Public', 'Total docks', 'Deployment Year']],
             hide_index=True)

st.set_option('deprecation.showPyplotGlobalUse', False)
districts = df_bikes['District'].unique()
default_district = ['Boston','Somerville','Cambridge', 'Salem']  # Default selection
selected_districts = st.sidebar.multiselect("Select Districts", districts, default=default_district)

# Filter DataFrame based on selected districts
filtered_df = df_bikes[df_bikes['District'].isin(selected_districts)]

# Calculate counts for the selected districts
district_counts = filtered_df['District'].value_counts()
explode = [0 if district != 'Boston' else 0.1 for district in district_counts.index]


fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    district_counts,
    labels=district_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops=dict(color="black"),  # Change the text color to black,
    explode=explode
)

for autotext in autotexts:
    autotext.set_fontsize(12)
ax.set_title('Bike Count per District')
ax.axis('equal')

# Display the pie chart using Streamlit
st.write("Pie Chart of Bike Count per District")
st.pyplot(fig)

df_bikes_trip_data = pd.read_csv(path + "hubway-tripdata2.csv")

st.divider()
st.write('<span style="font-size:30px; color:#A0C8E0;">The below bar chart shows the 5 most popular stations to start from, plotted against the trip duration</span>', unsafe_allow_html=True)
# Get the top 5 most popular start station names
top_start_stations = df_bikes_trip_data['start station name'].value_counts().head(5).index.tolist()
filtered_data = df_bikes_trip_data[df_bikes_trip_data['start station name'].isin(top_start_stations)]
station_duration = filtered_data.groupby('start station name')['tripduration'].mean().sort_values()
shades_of_blue = ['#1f77b4', '#aec7e8', '#7fbfff', '#4b8aff', '#005eff']

plt.figure(figsize=(10, 6))
bar_height = 0.9  # Set bar height to remove spacing
for i in range(len(station_duration)):
    station = station_duration.index[i]
    duration = station_duration.values[i]
    plt.barh(station, duration, height=bar_height, color=shades_of_blue[i % len(shades_of_blue)], edgecolor='black', linewidth=1)

plt.xlabel('Trip Duration')
plt.ylabel('Start Station Name')
plt.title('Average Trip Duration for Top 5 Start Stations')
plt.grid(axis='x')
st.pyplot()




st.divider()
st.write('<span style="font-size:30px; color:#A0C8E0;">Below is the following chart plotting all of the longitudes and latitudes of each blue bike station. This provides a general desciption of where the blue bikes are located.</span>', unsafe_allow_html=True)
df_bikes1 = pd.read_csv(path + "current_bluebikes_stations.csv", usecols=[1, 2, 3, 4], skiprows=1)
df_bikes1['District'].fillna('Unknown', inplace=True)


x_min = df_bikes1['Longitude'].min()
x_max = df_bikes1['Longitude'].max()
y_min = df_bikes1['Latitude'].min()
y_max = df_bikes1['Latitude'].max()

chart = {
    "mark": "point",
    "encoding": {
        "x": {
            "field": "Longitude",
            "type": "quantitative",
            "scale": {"domain": [x_min, x_max]}
        },
        "y": {
            "field": "Latitude",
            "type": "quantitative",
            "scale": {"domain": [y_min, y_max]}
        },
        "color": {"field": "District", "type": "nominal"},
        "shape": {"field": "District", "type": "nominal"},
        "text": {"field": "District"}
    },
}

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Vega-Lite native theme"])

with tab1:
    st.vega_lite_chart(
        df_bikes1, chart, theme="streamlit", use_container_width=True
    )

with tab2:
    st.vega_lite_chart(
        df_bikes1, chart, theme=None, use_container_width=True
    )

st.divider()


