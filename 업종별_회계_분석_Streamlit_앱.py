import streamlit as st
import pandas as pd
import altair as alt

# 📂 CSV 불러오기
df = pd.read_csv("업종별회계.csv")
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# melt 변환
df_melted = df.melt(id_vars=["업종", "항목"], var_name="Year", value_name="Amount")
df_melted["Year"] = df_melted["Year"].astype(str)

st.title("📊 업종별 항목 분석: 막대 + 꺾은선 그래프 통합")

# 📅 연도 선택
selected_year = st.selectbox("연도 선택", sorted(df_melted["Year"].unique()))

# 🔘 항목 선택
selected_items = st.multiselect("표시할 항목 선택", ["수익", "비용", "이익"], default=["수익", "비용", "이익"])

# 🧮 피벗: 이익 기준 정렬용
pivot = df_melted[df_melted["Year"] == selected_year].pivot_table(
    index="업종", columns="항목", values="Amount", fill_value=0
)
sorted_industries = pivot.sort_values(by="이익", ascending=False).index.tolist()

# 🎨 막대그래프용 데이터
filtered_bar = df_melted[
    (df_melted["Year"] == selected_year) &
    (df_melted["항목"].isin(selected_items)) &
    (df_melted["업종"].isin(sorted_industries))
]

# 📈 꺾은선그래프용 업종 선택
selected_industry_for_line = st.selectbox("꺾은선 그래프로 볼 업종 선택", df["업종"].unique())

filtered_line = df_melted[
    (df_melted["업종"] == selected_industry_for_line) &
    (df_melted["항목"].isin(selected_items))
]

# 🎨 Altair 막대그래프 (연도 선택)
bar_chart = alt.Chart(filtered_bar).mark_bar().encode(
    x=alt.X("업종:N", sort=sorted_industries, axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("Amount:Q", title="금액"),
    color=alt.Color("항목:N", legend=alt.Legend(title="항목")),
    tooltip=["업종", "항목", "Amount"]
).properties(
    width=900,
    height=450,
    title=f"📊 {selected_year}년 업종별 {'/'.join(selected_items)} 분포 (이익 기준 정렬)"
)

st.altair_chart(bar_chart, use_container_width=True)

# 🎨 Altair 꺾은선 그래프 (업종 선택)
line_chart = alt.Chart(filtered_line).mark_line(point=True).encode(
    x=alt.X("Year:O", title="연도"),
    y=alt.Y("Amount:Q", title="금액"),
    color=alt.Color("항목:N", legend=alt.Legend(title="항목")),
    tooltip=["Year", "항목", "Amount"]
).properties(
    width=900,
    height=400,
    title=f"📈 {selected_industry_for_line}의 연도별 {'/'.join(selected_items)} 추이"
)

st.altair_chart(line_chart, use_container_width=True)
