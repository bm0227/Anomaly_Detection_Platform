import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

## logo
logo = Image.open("logo1.jpg")
#st.image(logo)

##sidebar
sidebar = st.sidebar.radio("guide", ("Home", "Image", "Time series"))

#Home
if sidebar == "Home":

##text_home
    st.write(" ")
    st.title("Anomaly Detection Green Light")
    st.subheader("자동차 제조업 품질 향상을 위한 딥러닝 기반 avi 플랫폼 개발")
    st.write("펌프 임펠러의 주조결함을 이상탐지를 통하여 자동차 제조업의 생산 효율 향상과 품질 관리 비용을 절감을 야기함.")
    st.write(" ")
    home = Image.open("C:\Users\bm0227\OneDrive - UOU\그림\home.png")
    st.image(home)
    st.write(" ")
    st.write("Green Light")

elif sidebar == "Image":
    select_func = st.sidebar.selectbox("image",("Image 메인 화면", "A 기능", "B 기능"))
    
    ##sidebar_image
    if select_func == "Image 메인 화면":
        st.title("이미지")
        st.subheader("   · 알고리즘 소개")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.subheader("   · 기능에 대한 사용 설명서")
        st.write("      ▶ A 기능")
        st.write("          ...")
        st.write(" ")
        st.write("      ▶ B 기능")
        st.write("          ...")

    elif select_func == "A 기능":
        st.header("A 기능")
        st.subheader(" A 기능 설명란")
        st.text(" ")
        st.text("실행")
        a_button = st.button("파일 업로드")
        st.text("---------------------------------------------------------------------------------")
        #default_image = ("")
        #st.image(default_image)
        a_picture_check = st.sidebar.radio(" ", ("업로드 한 사진은 정상인가요?","네", "아니오"))
        print("라디오 박스 정보 출력 : ",a_picture_check)
        a_className = st.sidebar.selectbox(" ", ("클래스를 선택하세요.","bottle", "casting", "가죽"))
        a_modelName = st.sidebar.selectbox(" ", ("모델을 선택하세요.","resnet50", "wide_resnt50_2"))
        a_Threshold = st.sidebar.slider('Threshold를 설정하세요.', 0.00, 1.00)

    elif select_func == "B 기능":
        st.header("B 기능")
        st.subheader(" B 기능 설명란")
        st.text(" ")
        st.text("실행")
        a_button = st.button("파일 업로드")
        st.text("---------------------------------------------------------------------------------")
        st.text("실행 결과")
        #st.image(default_image)
        st.text(" ")
        st.text("성능 지표")

        b_picture_check = st.sidebar.radio(" ", ("업로드 한 사진은 정상인가요?","네", "아니오"))
        b_className = st.sidebar.selectbox(" ", ("클래스를 선택하세요.","bottle", "casting", "가죽"))
        b_modelName = st.sidebar.selectbox(" ", ("모델을 선택하세요.","resnet50", "wide_resnt50_2"))
        b_Threshold = st.sidebar.slider('Threshold를 설정하세요.', 0.00, 1.00)

elif sidebar == "Time series":
      
##text_timeseries
    st.header("Time series")
    st.subheader("subheader")
    st.write("Dais open lab.")
    if st.button("Push2"):
        col1, col2, col3 = st.columns(3)
        with col1:
          st.header("A")
          st.write("Time series Algorithm")

        with col2:
          st.header("B")
          st.write("Time series Algorithm")

        with col3:
          st.header("C")
          st.write("Time series Algorithm")   


uploaded_file = st.file_uploader("파일 업로드")
if uploaded_file is not None:
          df = uploaded_file
          print(df)
          # st.write(df)