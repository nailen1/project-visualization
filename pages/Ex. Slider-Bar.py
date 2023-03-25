import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 제목
st.header('감정가 별 물건 수')
st.text(' ')
# 데이터프레임 정의
df = pd.read_csv('./database/auction-items-nonan.csv')

# 필요한 상수 정의
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
price_start = 0
price_end = 1000000000
price_step = 1000000

# 박스와 슬리이더
address_sido = st.selectbox('지역(시도) 선택', list_sido)
selected_region = address_sido
price_range = st.slider("가격 범위 선택", 0, 1000000000,
                        (price_start, price_end), price_step)

df_price = df[df['price_estimate'] <= price_range[1]
              ][df['price_estimate'] >= price_range[0]]

if address_sido != '전체 지역':
    df_price = df_price[df_price['address_sido'] == address_sido]

# 가격 범위의 시작과 끝
price_min = price_range[0]
price_max = price_range[1]

# 폭 계산
range_width = price_max - price_min

# 각 구간의 폭 계산
interval_width = range_width / 19

# 20개의 원소를 가지는 리스트 초기화
price_list = [price_min]

# 각 구간의 시작 가격을 계산해서 리스트에 추가
for i in range(1, 20):
    next_price = price_min + interval_width * i
    price_list.append(next_price)


def convertPrice(price):
    if price == 0:
        return price
    if price >= 1000000 and price < 10000000:
        price = str(round(price/1000000, 1))+'백만'
        return price
    if price >= 10000000 and price < 100000000:
        price = str(round(price/10000000, 1))+'천만'
        return price
    if price > 100000000:
        price = str(round(price/100000000, 1))+'억'
        return price


st.info(
    f":white_check_mark: {selected_region} 기준, 감정가 {convertPrice(price_min)}원부터 {convertPrice(price_max)}원 사이의 물건 수 입니다.")

df_bin_estimate = df_price.groupby(
    pd.cut(df_price['price_estimate'], bins=20)).size().reset_index(name='number')
df_bin_estimate = df_bin_estimate.reset_index()
df_bin_estimate['index'] = df_bin_estimate['index']+1

fig = px.bar(df_bin_estimate, x='index', y='number', text='number')

fig.update_xaxes(tickvals=price_list)

# st.bar_chart(data=df_bin_estimate, x='index', y='number',
#              width=0, height=0, use_container_width=True)

st.plotly_chart(fig, theme=None, use_container_width=True)
