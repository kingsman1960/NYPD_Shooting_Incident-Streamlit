import pandas as pd
import streamlit as st
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = (
"NYPD_Shooting.csv"
)

st.title("Shooting cases in NYC")
st.markdown("This streamlit application is using for"
            "monitoring Shooting incidents in  NYC 💥🔫 \n By Youngwon Cho.")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates = [['OCCUR_DATE','OCCUR_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace = True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis= 'columns', inplace= True)
    data.rename(columns={'occur_date_occur_time': 'date/time'})
    return data


data = load_data(100000)




list = [1,5, 6, 7,9, 10 , 13
, 14, 17,18, 19, 20, 23, 24, 26, 28, 30, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
50, 52, 60, 61, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 75, 76, 77, 78, 79, 81, 83, 84, 88,
90, 94, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 120, 121, 122, 123]

st.header("which precinct happend most of shooting incidents")
precinct_test = st.selectbox("Number of Precinct of Police Area", list,1)
st.map(data.query("precinct >= @precinct_test")[["latitude", "longitude"]].dropna(how = "any"))


st.header("When does the incident happened a lot in a day?")
hour = st.selectbox("Hour to look at", range(0, 24), 1)
data = data[data['occur_date_occur_time'].dt.hour == hour]
st.markdown("Shooting incident between %i:00 and %i:00" % (hour, (hour + 1) % 24))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))


st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = {
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,


    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['occur_date_occur_time', 'latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale = 4,
        elevation_range = [0, 1000],
        ),
    ],
))
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)

st.subheader("Breakdown by hour between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data['occur_date_occur_time'].dt.hour >= hour) & (data['occur_date_occur_time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['occur_date_occur_time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "incidents": hist})
fig = px.bar(chart_data, x='minute', y='incidents', hover_data=['minute', 'incidents'], height=400)
st.write(fig)

