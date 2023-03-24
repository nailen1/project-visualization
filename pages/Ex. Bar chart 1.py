import streamlit as st
import pandas as pd
import numpy as np


list_sido = [
    '전체 지역',
    '서울특별시',
    '부산광역시',
    '대구광역시',
    '인천광역시',
    '광주광역시',
    '대전광역시',
    '울산광역시',
    '세종특별자치시',
    '경기도',
    '강원도',
    '충청북도',
    '충청남도',
    '전라북도',
    '전라남도',
    '경상북도',
    '경상남도',
    '제주특별자치도']

st.header('부동산 종류 별 물건 수')

address_sido = st.selectbox('지역 선택(시도)', list_sido)

df = pd.read_csv('./database/auction-items-nonan.csv')

if address_sido != '전체 지역':
    df = df[df['address_sido'] == address_sido]

df_bar = pd.DataFrame({'Category': df['category'].value_counts(
).index, "Number": df['category'].value_counts().values})

st.bar_chart(data=df_bar, x='Category', y='Number',
             width=0, height=0, use_container_width=True)
