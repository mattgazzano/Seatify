import streamlit as st
from PIL import Image
import psycopg2
import pandas as pd

postgres_connection = psycopg2.connect(
    host='localhost'
    , port='5432'
    , database='seatify'
    , user=st.secrets["POSTGRES_USERNAME"]
    , password=st.secrets["POSTGRES_PASSWORD"]
    , options='-c search_path=dbo,seatify'
)

df_artists = pd.read_sql_query('select * from dim_artists',con=postgres_connection)

# Page Title
st.set_page_config(page_title='Seatify', page_icon=':chart_with_upwards_trend:',layout='wide')

# Header Section
st.image(Image.open('visualization/seatify_logo.jpg'), width=400)
st.title('Seatify')
st.subheader('by [Matthew Gazzano](https://www.linkedin.com/in/matthewgazzano/)')
st.write('''
Both [Spotify](https://developer.spotify.com/documentation/web-api/) and [SeatGeek](https://platform.seatgeek.com/?ref=publicapis.dev) 
offer open source API’s to access Artists and Event data respectively. What's unique with using both of these sources is that SeatGeek provides a 
[Spotify Artist ID in the Performers object](https://platform.seatgeek.com/?ref=publicapis.dev#performers) which therefore allows you to connect 
data between the two platforms. In doing this, we can draw many conclusions on popular Artists, such as understanding the total number of listens 
they are receiving on their songs, and how many shows they are performing this year.

The goal of this project is to create a full stack analytics project that connects both of these sources via their API’s, 
transform their raw data into a usable star-schema inside of a Postgres database, and present it in a meaningful way.
    
You can learn more about the architechture of the project on [Github](https://github.com/mattgazzano/seatify).
''')

st.table(df_artists.head(50))