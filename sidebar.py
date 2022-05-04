import streamlit as st

start = st.sidebar.slider("start point",0,984,1)
end = st.sidebar.slider("end point",1,984,1)
threshold = st.sidebar.slider('Threshold', 0.3, 0.4, .01)

values = st.sidebar.slider(
    'start point : end point',
    0, 984, (150, 450))

