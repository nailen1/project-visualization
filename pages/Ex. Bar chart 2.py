import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

data = {'다가구주택': 8277785, '아파트': 14629771, '대지': 1326169,
        '다세대': 14771646, '상가': 13064833, '임야': 55900,
        '근린시설': 7443154, '기타': 2037723, '오피스텔': 14675840,
        '연립주택': 10714156, '단독주택': 4295468, '전답': 409345}

df_areaperpy_category = pd.DataFrame.from_dict(
    data, orient='index', columns=['price per py'])
df_areaperpy_category = df_areaperpy_category.reset_index().rename(columns={
    'index': 'category'})

fig = px.bar(df_areaperpy_category, x="category",
             y="price per py")
fig.update_layout(template="simple_white")

st.subheader('물건 종류 별 평당 가격')

st.bar_chart(data=df_areaperpy_category, x='category', y='price per py',
             width=0, height=0, use_container_width=True)

st.plotly_chart(fig, theme=None, use_container_width=True)
