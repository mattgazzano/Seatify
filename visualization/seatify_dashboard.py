import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import requests

# Page Title
st.set_page_config(page_title='Seatify', page_icon=':chart_with_upwards_trend:',layout='wide')


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json

spotify_lottie = load_lottieurl('https://lottiefiles.com/59334-spotify-launch')

# Header Section
st.title('Seatify')
st.image(Image.open('/home/mattgazzano/github/seatify/visualization/seatify_logo.jpg'))
st.lottie(spotify_lottie)
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

