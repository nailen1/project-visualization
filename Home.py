import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title(":house:부동산 법원경매 물건 데이터")

df = pd.read_csv('./database/auction-items-nonan.csv')

list_address_sido = df['address_sido'].unique().tolist()
list_category = df['category'].unique().tolist()

selected_sidos = st.multiselect(
    "대상 지역", options=list_address_sido, default=list_address_sido)
selected_categories = st.multiselect(
    "대상 지역", options=list_category, default=list_category)

df_selected = df[df['address_sido'].isin(selected_sidos)]

df_sido_total = df_selected.groupby(
    'address_sido').size().reset_index(name="number")
df_sido_cat = df_selected[df_selected['category'].isin(selected_categories)].groupby(
    'address_sido').size().reset_index(name="number")

list_sido = df_sido_total['address_sido'].unique().tolist()

y1 = df_sido_total['number'].values.tolist()
y2 = df_sido_cat['number'].values.tolist()

fig = go.Figure()
fig.add_trace(go.Bar(name="전체 분류", x=list_sido, y=y1))
fig.add_trace(go.Bar(name="선택 분류", x=list_sido, y=y2))

st.plotly_chart(fig, theme=None, use_container_width=True)


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(chart_data).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)
