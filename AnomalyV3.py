import streamlit as st
import numpy as np
from PIL import Image,ImageFont,ImageDraw
from typing import List
import requests, json
import io
import base64
import time
from io import BytesIO
import pandas as pd
import pickle

backendA = "http://203.250.72.8:3677/onefile"
backendB = "http://203.250.72.8:3677/somefile"
backendB_1 = "http://203.250.72.8:3677/result_File/"
backendIntro = "http://203.250.72.8:3677/Greenlight/Intro"
testFileUrl = "http://203.250.72.8:3677/test_File/oneFile"
testMultipleUrl = "http://203.250.72.8:3677/test_File/multipleFile"

#####
backendD = "http://203.250.72.8:3675/Model_prediction"
backendE = "http://203.250.72.8:3675/Model_results"
# backendE = "http://127.0.0.1:3675/Model_results"

def threshold_path(method,class_name):
    if method == "resnet18" and len(class_name) !=0:
        # print("resnet18")
        minmaxscorePath = f"./IMAGE/model/weight/resnet18/MinMaxINFO_{class_name}.pickle"
    elif method == "wide_resnet50_2" and len(class_name) !=0:
        # print("wide_resnet50_2")
        minmaxscorePath = f"./IMAGE/model/weight/wide_resnet50_2/MinMaxINFO_{class_name}.pickle"
    elif method =="모델을 선택해주세요." or len(class_name) ==0:
        minmaxscorePath ="./etc/nothing.pickle"
    return minmaxscorePath

def best_th(path):
    with open(path, 'rb') as f:
            data = pickle.load(f)    
    return data
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
    #col1, col2, col3 = st.columns([1, 2, 1])
    area = (0, 0,2000,1340)
    logo = logo.crop(area)
    size = logo.size
    logo = logo.resize((int(size[0]*0.3),int(size[1]*0.3)))
    
    st.image(logo)

# Dais Home Intro 생성 함수 -> 인자로 image 경로를 받는다.
def DaisHomeIntroCreate(img_path):
    HomeIntro = Image.open(img_path)
    st.image(HomeIntro)

# Dais Image Intro 생성 함수 -> 인자로 image 경로를 받는다.
def DaisImageIntroCreate(img_path):
    ImageIntro = Image.open(img_path)
    st.image(ImageIntro)



######################################################################################################################
# 메인 화면
def mainHomePage():

    DaisLogoCreate(img_path = "main_page.jpg")
    #st.write(" ")
    #st.subheader("Anomaly Detection Sandbox")
    #st.markdown(fontSize(20, "제조업의 AI 기반 이상탐지를 위한 알고리즘 및 플랫폼 개발"), True)
    #st.write(" ")
    #DaisHomeIntroCreate(img_path = "./etc/HomeIntro.PNG")
    #st.write(" ")


######################################################################################################################
## 이미지 화면
### 이미지 사이드바

def ImageSidebar(Flag=True):
    DTINFO = {"해당 클래스를 선택해주세요.":"","병":"bottle", "케이블":"cable", "캡슐":"capsule", "금속 너트":"metal_nut",
              "나사":"screw", "트랜지스터":"transistor", "지퍼":"zipper"}
    if Flag:
        picture_check = st.sidebar.radio("업로드 한 사진은 정상인가요?", ("정상", "비정상"))
    className = st.sidebar.selectbox("클래스 선택",
                                     ("해당 클래스를 선택해주세요.", '병', '케이블', '캡슐', '금속 너트', '나사', '트랜지스터', '지퍼'))
    className1 = DTINFO[className]
    modelName = st.sidebar.selectbox("모델 선택", ("모델을 선택해주세요.", "resnet18", "wide_resnet50_2"))
    th_path = threshold_path(modelName,className1)
    bth = best_th(th_path)            
    if className1 == "casting" or  len(className1) == 0:
        Threshold = st.sidebar.slider('Threshold를 설정하세요.', 0.00, 1.00, 0.33)
    else:
        bthreshold = round(float(bth['threshold']),2)
        Threshold = st.sidebar.slider('Threshold를 설정하세요.', 0.00, 1.00, bthreshold)
    return [picture_check, className1, modelName, Threshold] if Flag else [className1, modelName, Threshold]
    
    
def ClassImageShow(className):
    img_path = f"etc/classpicture/{className}"
    if className == "casting":
        Normal = Image.open(img_path+"N.jpeg")
    else:
        Normal = Image.open(img_path+"N.png")
    Anomaly = Image.open(img_path+"A.jpg")
    Normal = Normal.resize((200, 200))
    Anomaly = Anomaly.resize((200, 200))
    image_size = Normal.size
    
    bg_h = 24
    pl = 0
    new_image = Image.new('RGB',(2*image_size[0]+ 3, image_size[1]+bg_h+pl), (255,0,0,))
    bg1 = Image.new('RGB',(image_size[0], bg_h), (255,255,255))
    bg2 = Image.new('RGB',(image_size[0], bg_h), (255,255,255))
    
    new_image.paste(bg1,(0,0))
    new_image.paste(bg1,(image_size[0]+3,0))
    new_image.paste(Normal,(0,bg_h+pl))
    new_image.paste(Anomaly,(image_size[0]+3,bg_h+pl))

    Font =ImageFont.truetype("fonts/nanum/NanumBarunGothic.ttf",20)
    draw =ImageDraw.Draw(new_image)
    wt = image_size[0]//3
    draw.text((wt,2),"정상 제품",(0,0,0),font=Font)
    draw.text((wt+image_size[0],2),"불량 제품",(0,0,0),font=Font)
    
    draw =ImageDraw.Draw(new_image)
    st.sidebar.markdown("선택하신 클래스에 대한 사진 정보입니다.")
    st.sidebar.image(new_image)

    
### 이미지 메인페이지
def ImageMainPage():
    #DaisLogoCreate(img_path = "./etc/small_size_logo.png")
    st.title("이미지 이상진단 테스트")
    st.write("\n\n\n")
    st.subheader("PaDim 알고리즘 소개")
    DaisImageIntroCreate(img_path = "Padim1.PNG")
    st.markdown(
            "* **`Embedding extraction(위치 정보 추출)`** : 사전 학습된 CNN 모델을 사용해 서로 다른 layer 들에서 가져온 Patch Level 정보를 연결하여 보다 넓은 의미 정보를 담아서 **Patch Embedding Vector를 생성**하고 중복되거나 필요없는 정보를 줄이기 위해 랜덤 차원 축소를 진행하여 모델의 복잡도를 줄임과 동시에 유의미한 정보 추출하게 됩니다.\n"
        "* **`Learning of the normality(정규성 학습)`** : 정상 샘플의 특성을 학습하기 위해 정상 샘플로부터 (i, j) 위치에 대한 Patch Embedding Vector가 다변량 정규 분포 $$N(μ_{ij},Σ_{ij}$$)로 부터 생성된다는 가정하에 **Patch 별 평균과 공분산을 계산**하게 됩니다.\n"
    "* **`Anomaly Score Map(이상 점수 맵)`** : 평가할 샘플의 Patch Embedding Vector 정보와 학습된 샘플들로 얻은 Patch 별 평균과 공분산 정보를 (i, j) 위치별로 마할라노비스 거리를 계산해 Patch마다 Anomaly Score를 부여하여 하나의 Anomaly Score Map을 생성하게 되며 이를 활용해 **이상 탐지** 및 **이상 영역 탐지**를 하게 됩니다."
    )
        
    # st.markdown("* One-Class Classification 방법을 사용합니다.\n"
    #             "* 사전 학습된 CNN 모델을 통해 정상 샘플에 대한 Embedding 정보를 뽑아내고, Random Dimesionality Reduction을 진행해 정상 샘플에 대한 평균과 공분산 정보를 추출합니다.\n"
    #             "* 정상 샘플이 Gaussian Distribution을 따른다는 가정하에, 테스트 데이터와 학습 데이터의 정상 샘플 간 Mahalanobis Distance를 통해 이상 여부를 판단합니다.\n")
    
    st.markdown("---")
def load_image(image_file):
    img = Image.open(image_file)
    return img

### 이미지 통합 버전 기능 페이지
def ImageApartPage():
    className, modelName, threshold = ImageSidebar(Flag=False)
    try:
        ClassImageShow(className)
    except:
        pass
    ## 메인 컨텐츠
    st.subheader("이미지 파일에 대한 이상진단 테스트")
    st.write("\n")
    st.markdown(fontSize(20, "사용방법"), True)
    st.markdown("1. 왼쪽에 있는 사이드 바를 선택해주세요.\n"
                "   * 업로드할 사진에 대해 **해당 클래스를 선택**해주시고, 두 가지 **모델 중 하나를 선택**해주세요.\n"
                "   * 자동으로 **최적의 임계값**을 선택해줍니다. `원하는 결과가 아니라면 해당 값을 낮추거나 올려주세요.`")
    st.markdown("2. 테스트할 사진을 업로드 해주세요.\n"
                "   * `Drag and drop file here` 라는 곳에 **Browse files** 라는 버튼이 있습니다.\n"
                "   * 해당 버튼을 눌러서 **테스트할 이미지 파일을 업로드** 해주세요.\n"
                "   * **`만약 테스트할 사진이 여러 개일 경우`** 아래와 같은 방법으로 압축해 ZIP파일로 업로드해주세요.\n"
               )
    explanB = Image.open("./IMAGE/ImageFolder/mutiple_explan.PNG") 
    st.image(explanB)
    st.markdown("3. 1번 2번 작업이 완료됐다면 보내기 버튼을 눌러주세요.")
    st.text(" ")
    
    st.markdown('<style>' + open('./etc/icons.css').read() + '</style>', unsafe_allow_html=True)
    st.markdown('<i class="material-icons">face 테스트시작.</i>', unsafe_allow_html=True)
    href1 =f'<a href={testFileUrl} download="bottle.png">Bottle IMG File</a>'
    href2 =f'<a href={testMultipleUrl} download="bottle.zip">Bottle ZIP File</a>'
    
    col1,col2,col3 = st.columns([2.5, 0.65,0.65])
    col1.markdown("평가할 **`병`** 클래스에 대한 데이터 다운로드")
    col2.markdown(href1,True)
    col3.markdown(href2,True)

    uploaded_file, start_button, cancel_button = makeSendFile()
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.markdown("---")
    if start_button:
        if className =="" or modelName =="모델을 선택해주세요." or uploaded_file is None:
            st.warning("구별하고자 하는 클래스와 사전학습 모델과 파일을 업로드하셨는지 확인해주세요 ^____^")
        else:
            waited = st.markdown("**이상진단 중이니 잠시만 기다려주세요.** ^____^")
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
            string = uploaded_file.name.split(".")[-1]

            if string.lower() != 'zip':
                response = requests.post(backendA, files=files, data=item)
                anomaly_info = response.json()["anomaly_score"][0]
                img = response.json()["result_Image"]["path"]
                response1 = requests.get(backendA + "/result_image", data={"result_filename": img})
                waited.empty()
                anomaly_content = " 판독결과는  {} 사진입니다.".format(anomaly_info["real_class"])
                st.markdown(fontSize(18, anomaly_content), True)
                st.write("\n")
                st.markdown("* 해당 사진의 원인 결과는 다음과 같습니다.")
                result_image = Image.open(BytesIO(response1.content))
                st.image(result_image)
                st.markdown("---")
            else:
                response = requests.post(backendB, files=files, data=item)
                content = response.json()
                result_zip = content["input_path"].split("/")[3]
                Scores = content["score"][0]
                fsize = content["fsize"]
                waited.empty() # 결과가 나왔으니 삭제.
                st.markdown(f"### {fsize}장의 실행 결과 성능은 다음과 같습니다.\n")
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
        M.empty()

    

def DaisWeb():
    sidebar = st.sidebar.radio(" ", ("Home", "Image Anomaly detection"))   # 사이드바
    image_sidebar_content = ["이미지 메인 화면", "테스트"]

    if sidebar == "Home":
        mainHomePage()
    elif sidebar == "Image Anomaly detection":
        select_func = st.sidebar.selectbox("이미지 이상진단 테스트", (image_sidebar_content[0],image_sidebar_content[1]))
        if select_func == image_sidebar_content[0]:
            ImageMainPage()
        elif select_func == image_sidebar_content[1]:
            ImageApartPage()


if __name__ =='__main__':
    main = DaisWeb()