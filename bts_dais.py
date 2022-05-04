import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from typing import List
import requests, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
import base64
import time
from io import BytesIO

# backend = "http://fastapi:8000/segmentation" http://ec55-116-121-38-22.ngrok.io
backendA = "http://127.0.0.1:3677/onefile"
backendB = "http://127.0.0.1:3677/somefile"
backendB_1 = "http://127.0.0.1:3677/result_File/"
backendC = "http://127.0.0.1:2000/"


#####
backendD = "http://127.0.0.1:2000/Model_prediction"

# backendA = "http://ec55-116-121-38-22.ngrok.io/onefile"
# backendB = "http://ec55-116-121-38-22.ngrok.io/somefile"
# backendB_1 = "http://ec55-116-121-38-22.ngrok.io/result_File/"


###################################################################################################################
# CSS Define
def fontSize(fontsize,content):
    html_str = f"""
                    <style>
                    p.a {{
                      font: bold {fontsize}px Courier;
                    }}
                    </style>
                    <p class="a">{content}</p>
                    """
    return html_str


###################################################################################################################
## 부가 기능 markdown 설정.
def makeSendFile():
    uploaded_file = st.file_uploader(label="파일 업로드")  # accept_multiple_files=True)
    col1, col2, col3 = st.columns([3, 0.7, 0.7])
    start_button = col2.button("보내기")
    cancel_button = col3.button("이전으로")
    return uploaded_file, start_button, cancel_button


######################################################################################################################
# Dais Logo 생성 함수 -> 인자로 image 경로를 받는다.
def DaisLogoCreate(img_path):
    logo = Image.open(img_path)
    st.image(logo, width=500)

# Dais Home Intro 생성 함수 -> 인자로 image 경로를 받는다.
def DaisHomeIntroCreate(img_path):
    HomeIntro = Image.open(img_path)
    st.image(HomeIntro)

# Dais Image Intro 생성 함수 -> 인자로 image 경로를 받는다.
def DaisImageIntroCreate(img_path):
    ImageIntro = Image.open(img_path)
    st.image(ImageIntro)

# Dais Time Series Intro 생성 함수 -> 인자로 image 경로를 받는다.
def DaisTimeIntroCreate(img_path):
    TimeIntro = Image.open(img_path)
    st.image(TimeIntro)


######################################################################################################################
# 메인 화면
def mainHomePage():

    DaisLogoCreate(img_path = "SandboX-logo.png")
    st.write(" ")
    st.title("  Anomaly Detection Sandbox")
    st.subheader("제조업의 AI 기반 이상탐지를 위한 알고리즘 및 플랫폼 개발")
    st.write(" ")
    #DaisHomeIntroCreate(img_path = "HomeIntro.jpg")
    st.write(" ")


######################################################################################################################
## 이미지 화면
### 이미지 사이드바
def ImageSidebar(Flag=True):
    if Flag:
        picture_check = st.sidebar.radio("업로드 한 사진은 정상인가요?", ("정상", "비정상"))
    className = st.sidebar.selectbox("클래스 선택",
                                     ("해당 클래스를 선택해주세요.", 'casting', 'bottle', 'cable', 'capsule', 'carpet', 'grid',
                                      'hazelnut', 'leather', 'metal_nut', 'pill', 'screw',
                                      'tile', 'toothbrush', 'transistor', 'wood', 'zipper'))
    modelName = st.sidebar.selectbox("모델 선택", ("모델을 선택해주세요.", "resnet18", "wide_resnet50_2"))
    Threshold = st.sidebar.slider('Threshold를 설정하세요.', 0.00, 1.00, 0.33)
    return [picture_check, className, modelName, Threshold] if Flag else [className, modelName, Threshold]


### 이미지 메인페이지
def ImageMainPage():
    #DaisLogoCreate(img_path = "SandboX-logo_small.png")
    st.title("이미지 이상진단 테스트")
    st.write("\n")
    st.subheader("PaDim 알고리즘 소개")
    DaisImageIntroCreate(img_path = "ImageIntro.png")
    st.markdown("---")

### 이미지 A 기능 페이지
def ImageApartPage():
    # picture_check, className, modelName, threshold = ImageSidebar(Flag=True)
    className, modelName, threshold = ImageSidebar(Flag=False)

    ## 메인 컨텐츠
    st.header("단일 사진에 대한 이상진단 테스트")
    st.write("\n")
    st.markdown(fontSize(20, "사용방법"), True)
    st.markdown("1. 왼쪽에 있는 사이드 바를 선택해주세요.\n"
                "   * 업로드할 사진에 대해 **해당 클래스를 선택**해주시고, 두 가지 **모델 중 하나를 선택**해주세요.\n"
                "   * 임계값이 **기본값(0.33)**입니다. `원하는 결과가 아니라면 해당 값을 낮추거나 올려주세요.`")
    st.markdown("2. 테스트할 사진을 업로드 해주세요.\n"
                "   * `Drag and drop file here` 라는 곳에 **Browse files** 라는 버튼이 있습니다.\n"
                "   * 해당 버튼을 눌러서 **테스트할 이미지 파일을 업로드** 해주세요.")
    st.markdown("3. 1번 2번 작업이 완료됐다면 보내기 버튼을 눌러주세요.")
    st.text(" ")
    # st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
    st.markdown('### 테스트 시작하기')

    uploaded_file, start_button, cancel_button = makeSendFile()
    st.markdown("---")
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        # st.write(file_details)
        # files = {"file": uploaded_file.getvalue() }
    if start_button:
        print("전송")
        waited = st.markdown("**이상진단 중이니 잠시만 기다려주세요.** ^____^")
        # picture_check = "0" if picture_check == "정상" else "1"

        files = {
            "file": uploaded_file.getvalue(),
        }
        item = {
            # "y_labels": picture_check,
            "threshold": str(threshold),
            "className": className,
            "modelName": modelName,
            "fileName": uploaded_file.name,
        }
        # print("Item ", item)
        response = requests.post(backendA, files=files, data=item)

        # print(response.json())
        # print(type(response.json()))
        anomaly_info = response.json()["anomaly_score"][0]
        img = response.json()["result_Image"]["path"]
        # print("이미지 경로 : ",img)
        response1 = requests.get(backendA + "/result_image", data={"result_filename": img})
        waited.empty()
        anomaly_content = " 판독결과는  {} 사진입니다.".format(anomaly_info["real_class"])
        st.markdown(fontSize(18, anomaly_content), True)
        st.write("\n")
        if anomaly_info["real_class"] =="비정상":
            st.markdown("* 해당 사진의 원인 결과는 다음과 같습니다.")
            result_image = Image.open(BytesIO(response1.content))
            st.image(result_image)
            st.markdown("---")


    elif cancel_button:
        print("비전송")
        M = st.markdown("---")
        M.empty()


### 이미지 B 기능 페이지
def ImageBpartPage():
    #### 사이드바
    className, modelName, threshold = ImageSidebar(Flag=False)

    ### 메인 컨텐츠
    st.header("다중 사진에 대한 이상진단 테스트")
    st.write("\n")
    st.markdown(fontSize(20, "사용방법"), True)
    st.markdown("1. 테스트할 폴더 구성을 다음과 같이 구성해주세요.\n"
                "   * 파일 이름은 자유롭게 지정해도 괜찮습니다. **다만, 해당 zip폴더 안에는 다음 그림과 같이 구성해야합니다.**")
    explanB = Image.open("./ImageFolder/mutiple_explan.PNG") 
    st.image(explanB)
    st.markdown("2. 왼쪽에 있는 사이드 바를 선택해주세요.\n"
                "   * 업로드할 사진들의 **해당 클래스를 선택**해주시고, 두 가지 **모델 중 하나를 선택**해주세요.\n"
                "   * 임계값이 **기본값(0.33)**입니다. `원하는 결과가 아니라면 해당 값을 낮추거나 올려주세요.`")
    st.markdown("3. 테스트할 파일을 업로드 해주세요.\n"
                "   * `Drag and drop file here` 라는 곳에 **Browse files** 라는 버튼이 있습니다.\n"
                "   * 해당 버튼을 눌러서 **테스트할 Zip 파일을 업로드** 해주세요.")
    st.markdown("3. 1번 2번 3번 작업이 완료됐다면 보내기 버튼을 눌러주세요.")

    st.text(" ")
    # st.markdown('<i class="material-icons">face</i>',unsafe_allow_html=True)
    st.markdown('### 테스트 시작하기')
    uploaded_file, start_button, cancel_button = makeSendFile()
    st.markdown("---")

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        # st.write(file_details)
        # files = {"file": uploaded_file.getvalue() }
        # print(files)
    if start_button:
        waited = st.markdown("**이상진단 중이니 잠시만 기다려주세요.** ^____^")
        print("B 전송")

        files = {
            "file": uploaded_file.getvalue(),
        }
        item = {
            "threshold": str(threshold),
            "className": className,
            "modelName": modelName,
            "fileName": uploaded_file.name,
        }
        # print("Item ", item)
        response = requests.post(backendB, files=files, data=item)

        print(response.status_code)
        print(response.json())
        content = response.json()
        result_zip = content["input_path"].split("/")[3]
        Scores = content["score"][0]
        waited.empty() # 결과가 나왔으니 삭제.
        st.markdown("### 실행 결과 성능은 다음과 같습니다.\n")
        st.write("\n")
        for key in Scores.keys():
            Score_content = "`{}` : {} 입니다.".format(key,Scores[key])
            st.markdown(f"* {Score_content}")

        st.write("\n")
        href =f'<a href={backendB_1}{result_zip} download="result.zip">다운로드</a>'
        col1, col2, col3 = st.columns([3, 0.7, 1])
        col1.markdown("판독된 결과를 다운받기 원하시면 **다운로드 버튼**을 눌러주세요.")
        col2.markdown(href,True)
        st.markdown("----")


    elif cancel_button:
        print("비전송")
        M = st.markdown("---")


######################################################################################################################
## 시계열 화면

### 시계열 메인페이지
def TimeMainPage():
    #DaisLogoCreate(img_path = "logo.png")
    st.title("시계열 이상진단 테스트")
    st.write("\n")
    st.subheader("LSTM Autoencoder 알고리즘 소개")
    DaisTimeIntroCreate(img_path = "TimeIntro.png")
    st.markdown("---")

### 시계열 A 기능 페이지
def TimeApartPage():
    st.header("시계열 이상진단 테스트")
    st.text(" ")
    time_df = pd.read_csv("final_df.csv")
    start = 0
    end = 14
    st.write(time_df.loc[start:end])
    st.text(" ")
    st.markdown(fontSize(20, "사용방법"), True)
    st.markdown("시계열 데이터를 업로드하면 그에 따른 정상 비정상 유무를 알려줍니다.")
    st.text(" ")
    #st.markdown("---")
    #message = st.text_area("데이터를 입력하세요.", " ")
    col1,col2 = st.columns([3,1])
    if col2.button("Submit", key='message'):
        time_data = message.title()
        #time_data = [float(x) for x in time_data.split()]
        Prediction = {
            "data": time_data
            }
        print(Prediction)
        response = requests.post(backendD, data=Prediction)
        state = response.json()["state"]
        st.success(state)
    st.markdown("---")



def DaisWeb():
    sidebar = st.sidebar.radio(" ", ("Home", "Image", "Time Series"))   # 사이드바
    image_sidebar_content = ["메인 화면", "단일 사진", "다중 사진"]
    time_sidebar_content = ["메인 화면", "시계열 1", "시계열 2"]

    if sidebar == "Home":
        mainHomePage()
    elif sidebar == "Image":
        select_func = st.sidebar.selectbox("이미지 이상진단 테스트", (image_sidebar_content[0],image_sidebar_content[1],image_sidebar_content[2]))
        if select_func == image_sidebar_content[0]:
            ImageMainPage()
        elif select_func == image_sidebar_content[1]:
            ImageApartPage()
        elif select_func == image_sidebar_content[2]:
            ImageBpartPage()
    elif sidebar == "Time Series":
        select_func = st.sidebar.selectbox("시계열 이상진단 테스트", (time_sidebar_content[0],time_sidebar_content[1]))
        if select_func == time_sidebar_content[0]:
            TimeMainPage()
        elif select_func == time_sidebar_content[1]:
            TimeApartPage()


if __name__ =='__main__':
    main = DaisWeb()