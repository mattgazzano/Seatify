import streamlit as st
from PIL import Image
import pandas as pd
import gspread

# Page Title
st.set_page_config(page_title='Seatify', page_icon=':chart_with_upwards_trend:',layout='wide')

# Header Section
st.image(Image.open('/visualization/seatify_logo.jpg'), width=400)
st.title('Seatify')
st.subheader('by [Matthew Gazzano](https://www.linkedin.com/in/matthewgazzano/)')
st.write('''
Both [Spotify](https://developer.spotify.com/documentation/web-api/) and [SeatGeek](https://platform.seatgeek.com/?ref=publicapis.dev) 
offer open source API’s to access Artists and Event data respectively. What's unique with using both of these sources is that SeatGeek provides a 
[Spotify Artist ID in the Performers object](https://platform.seatgeek.com/?ref=publicapis.dev#performers) which therefore allows you to connect 
data between the two platforms. In doing this, we can draw many conclusions on popular Artists, such as understanding the total number of listens 
they are receiving on their songs, and how many shows they are performing this year.

The goal of this project is to create a full stack analytics solution that connects both of these sources via their API’s, 
transforms their raw data into a usable star-schema inside of a Postgres database, and present it in a meaningful way.
    
You can learn more about the architechture of the project on [Github](https://github.com/mattgazzano/seatify).
''')

gcloud_service_account = gspread.service_account()
seatify_dashboard_postgres_tables = gcloud_service_account.open_by_key(st.secrets['seatify_dashboard_postgres_tables']).worksheet('dim_artists')
df_artists = pd.json_normalize(seatify_dashboard_postgres_tables.get_all_records())

st.table(df_artists.head(50))