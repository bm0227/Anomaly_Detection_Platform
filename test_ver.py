from typing import Text
import streamlit as st
import pandas as pd
import numpy as np
import time
from streamlit import config
import random
from PIL import Image

## logo
logo = Image.open("그림3.jpg")
st.image(logo)

## menu(sidebar)
#menu = st.sidebar.radio("", ("Home", "Image", "Time series"))

##menu input(text)
menu = st.text_input('')

## menu input(form)
#with st.form(key='my_form'):
	#menu = st.text_input(label='Enter some text')
	#submit_button = st.form_submit_button(label='Submit')

if menu == "Home":
    ##st.image()
    st.write("DaiS OpenLab")
    st.write("제조업의 AI 기반 이상탐지를 위한 알고리즘 및 플랫폼 개발")
    st.write(" ")
    st.write("이상치 탐색을 하고 싶다면 Image 혹은 Time series를 입력해주세요.")
elif menu == "Image":
    ##st.image()
    st.write("이미지")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
    submit_button = st.button(label='Submit')
elif menu == "Time series":
    ##st.image()
    st.write("시계열")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
    submit_button = st.button(label='Submit')