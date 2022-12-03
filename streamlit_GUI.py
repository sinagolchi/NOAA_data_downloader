import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import datetime
header = {'token':'FNSThFbJGsLcmJazhidBvgMjkxqBXLMA'}
import matplotlib.pyplot as plt

#response = requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:NI", headers=header)
s_date = st.date_input('start date',value=datetime.date(1942,7,6),min_value=datetime.date(1940,7,6),max_value=datetime.date(2022,11,30))
e_date = st.date_input('end date',value=datetime.date(2022,11,30),min_value=datetime.date(1940,7,6),max_value=datetime.date(2022,12,2))

datatype =st.multiselect('Data type',options=['PRCP','TEMP'])

response = requests.get(f"https://www.ncei.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:12&startdate={s_date.strftime('%Y-%m-%d')}&enddate={e_date.strftime('%Y-%m-%d')}&limit=1000&datacategoryid={'&'.join(datatype)}&sortorder=asc", headers=header)

#response_des = requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:12&startdate=1950-10-03&limit=1000&sortorder=desc", headers=header)


#%%
#sortorder
df_asc = pd.DataFrame.from_dict(response.json()['results'])

st.dataframe(df_asc)

col1, col2 = st.columns(2)

f_start = col1.date_input('Start date',value=datetime.date(1942,11,1),min_value=datetime.date(1940,7,6),max_value=datetime.date(2022,11,30))

f_end = col2.date_input('End date',value=datetime.date(2022,11,25),min_value=datetime.date(1940,7,6),max_value=datetime.date(2022,12,2))

df_station = df_asc[(df_asc['mindate'] <= f_start.strftime('%Y-%m-%d')) & (df_asc['maxdate'] >= f_end.strftime('%Y-%m-%d'))]

st.dataframe(df_station)

station = st.selectbox('Station',options=df_station['id'])

#types_data = st.multiselect('Type of data', options=['PRCP','TMIN','TMAX'])

df_station = df_station.set_index('id')

date_range = pd.date_range(start=df_station.loc[station,'mindate'],end=df_station.loc[station,'maxdate'],freq='A')



dataframes = []

for i in range(len(date_range)-1):
    data = requests.get(f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid={station}&startdate={date_range[i].strftime('%Y-%m-%d')}&enddate={date_range[i+1].strftime('%Y-%m-%d')}&datatypeid=PRCP&limit=1000", headers=header)
    #st.write(data.json())
    try:
        dataframes.append(pd.DataFrame.from_dict(data.json()['results']))
    except:
        pass

big_data = pd.concat(dataframes)

st.download_button('Download CSV',big_data.to_csv().encode('utf-8'),"file.csv","text/csv")
# st.dataframe(big_data)
#big_data['date'] = pd.to_datetime(big_data['date'], format='%Y-%m-%d')
# # big_data['format_date'] = big_data['date'].dt.strftime('%Y/%m/%d')
#
# big_data.plot(x='date',y='value')
# plt.xticks(rotation=45)
# st.pyplot(plt.gcf())