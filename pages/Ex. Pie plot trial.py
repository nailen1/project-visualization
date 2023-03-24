import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# df = pd.read_csv('../dataset-auction-items/auction-items-total.csv')
# df_seoul = df[df['address_sido'] == '서울특별시']

# df_bar = pd.DataFrame({'Category': df_seoul['category'].value_counts(
# ).index, "Number": df_seoul['category'].value_counts().values})

# st.write('부동산 종류별 물건 수: 서울특별시')

# st.bar_chart(data=df_bar, x='Category', y='Number',
#              width=0, height=0, use_container_width=True)


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

st.header(f'물건 별 비율')

df = pd.read_csv('./database/auction-items-nonan.csv')

address_sido = st.selectbox('지역 선택(시도)', list_sido)

if address_sido != '전체 지역':
    df = df[df['address_sido'] == address_sido]

a, b = st.columns(2)

with a:
    st.subheader("전체 지역")
    fig = px.pie(df, names="category")
    st.plotly_chart(fig, theme=None, use_container_width=True)

with b:
    selected_region = address_sido
    st.subheader(f"{selected_region}")
    fig = px.pie(df, names="category")

    st.plotly_chart(fig, theme=None, use_container_width=True)

# tab_a, tab_b = st.tabs("전체", "시도별")

# tab_a.write("a")
# tab_b.write("b")
