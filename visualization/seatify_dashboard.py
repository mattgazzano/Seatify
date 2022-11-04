import streamlit as st
from PIL import Image

header = st.container()
seatify_logo = Image.open('seatify_logo.png')

st.image(seatify_logo)

with header:
    st.title('Seatify')
    st.subheader('Bringing together Spotify and Seatgeek data from publicly available APIs')