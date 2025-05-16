import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ 데이터 불러오기
df = pd.read_csv("업종별회계.csv")

# Unnamed 컬럼 제거
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# ✅ long-form으로 변환
df_melted = df.melt(id_vars=["업종", "항목"], var_name="Year", value_name="Amount")
df_melted["Year"] = df_melted["Year"].astype(str)

# ✅ 업종 선택에 따른 꺾은선 그래프는 그대로 유지
st.title("📊 업종별 수익·비용·이익 추이 분석 대시보드")
selected_industry = st.selectbox("업종 선택", df["업종"].unique())
selected_items = st.multiselect("항목 선택", ["수익", "비용", "이익"], default=["수익", "비용", "이익"])

filtered = df_melted[
    (df_melted["업종"] == selected_industry) & 
    (df_melted["항목"].isin(selected_items))
]
pivot = filtered.pivot_table(index="Year", columns="항목", values="Amount")
st.subheader(f"📈 {selected_industry}의 연도별 추이(1000원)")
st.line_chart(pivot)

# ✅ 여기부터 Plotly 기반 막대그래프
st.subheader("📊 연도별 업종 비교")
selected_year = st.selectbox("연도 선택", df.columns[3:], key="year_select")

filtered_year = df_melted[df_melted["Year"] == selected_year]

# ✅ Plotly 그래프
fig = px.bar(
    filtered_year,
    x="업종",
    y="Amount",
    color="항목",
    barmode="group",  # 그룹형 막대그래프
    title=f"{selected_year}년 업종별 수익·비용·이익 비교",
    labels={"Amount": "금액(천 원)", "업종": "업종", "항목": "항목"}
)

fig.update_layout(
    xaxis_tickangle=-30,
    plot_bgcolor='white',
    yaxis=dict(showgrid=True, gridcolor='lightgray'),
    legend=dict(title="항목", orientation="h", y=-0.2)
)

st.plotly_chart(fig, use_container_width=True)
