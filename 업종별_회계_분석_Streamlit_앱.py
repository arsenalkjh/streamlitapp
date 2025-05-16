import streamlit as st
import pandas as pd


# ✅ 데이터 불러오기
df = pd.read_csv("업종별회계.csv")

# Unnamed 컬럼 제거
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# 연도별 long-form 변환
df_melted = df.melt(id_vars=["업종", "항목"], var_name="Year", value_name="Amount")
df_melted["Year"] = df_melted["Year"].astype(str)

# ✅ 페이지 제목
st.title("📊 업종별 수익·비용·이익 추이 분석 대시보드")

# ✅ 업종 선택
selected_industry = st.selectbox("업종 선택", df["업종"].unique())

# ✅ 항목 선택
selected_items = st.multiselect("항목 선택", ["수익", "비용", "이익"], default=["수익", "비용", "이익"])

# ✅ 선택한 업종 필터링
filtered = df_melted[
    (df_melted["업종"] == selected_industry) & 
    (df_melted["항목"].isin(selected_items))
]

# ✅ 피벗 테이블로 연도별 꺾은선 그래프용 변환
pivot = filtered.pivot_table(index="Year", columns="항목", values="Amount")

# ✅ 꺾은선 그래프 출력
st.subheader(f"📈 {selected_industry}의 연도별 추이(1000원)")
st.line_chart(pivot)

# ✅ 연도 선택 → 업종별 막대그래프
st.subheader("📊 연도별 업종 비교")
selected_year = st.selectbox("연도 선택", df.columns[3:])

# 선택 연도 데이터 필터링
filtered_year = df_melted[df_melted["Year"] == selected_year]

# 피벗 테이블로 업종별 수익/비용/이익 비교용 변환
pivot2 = filtered_year.pivot_table(index="업종", columns="항목", values="Amount")

# ✅ 막대그래프 출력
st.bar_chart(pivot2)
