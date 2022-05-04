import streamlit as st

col1,col2 = st.columns([3,1])
col1.success("First COlumn")
col2.button("Hello From Col2")