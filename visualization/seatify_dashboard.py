import streamlit as st
from PIL import Image
import pandas as pd
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["seatify_dashboard_postgres_tables"]
rows = run_query(f'SELECT * FROM "{sheet_url}" LIMIT 50')

# Page Title
st.set_page_config(page_title='Seatify', page_icon=':chart_with_upwards_trend:',layout='wide')

# Header Section
st.image(Image.open('/visualization/assets/seatify_logo.jpg'), width=400)
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

st.table(rows)