import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# CSV 파일 불러오기
df = pd.read_csv("회계년도통합.csv", encoding="utf-8-sig")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")
df["년도"] = df["년도"].astype(str)

# 비용 항목 그룹
cost_parts = [
    "생산관리비(천원)", "연료비(천원)", "어구,선구비 (천원)", "미끼비(천원)", "수선비(천원)",
    "얼음비(천원)", "어상자비(천원)", "소모품비(천원)", "용선비 (천원)", "기타(천원).3"
]

# ✅ Streamlit 앱 제목
st.title("업종별 회계 시각화 대시보드")

# ✅ 사이드바 메뉴 선택
page = st.sidebar.radio("📂 보고서 메뉴 선택", ["연도별 수익/비용/이익 시계열", "비용 항목 비율 (원형)", "업종별 평균 바차트"])

# ✅ 공통 필터: 업종 선택

# ✅ 시계열 그래프
if page == "연도별 수익/비용/이익 시계열":
    st.subheader("연도별 수익 · 비용 · 이익 추이")
    selected_industry = st.selectbox("🔍 업종 선택", df["주어업1"].unique())

    industry_df = df[df["주어업1"] == selected_industry]

    columns_to_plot = ["총수익(천원)", "총비용(천원)", "어업이익(천원)"]

    if not set(columns_to_plot).issubset(df.columns):
        st.error("필요한 데이터가 누락되었습니다.")
    else:
        plot_df = industry_df[["년도"] + columns_to_plot].copy()
        plot_df = plot_df.groupby("년도").mean().round().reset_index()
        fig = px.line(
            plot_df,
            x="년도",
            y=columns_to_plot,
            markers=True,
            title=f"{selected_industry} 업종의 연도별 수익/비용/이익 추이"
        )
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig)

# ✅ 원형 차트: 특정 연도별 비용 항목
elif page == "비용 항목 비율 (원형)":
    st.subheader("특정 연도별 비용 구성 비율")

    year = st.selectbox("년도 선택", sorted(df["년도"].unique()), key="year_select_pie")
    totalList = list(df["주어업1"].unique()) + ["전체"]
    category = st.selectbox("업종 선택", totalList, key="industry_select_pie")

    if category == "전체":
        year_category_df = df[df["년도"] == year]
    else:
        year_category_df = df[(df["년도"] == year) & (df["주어업1"] == category)]

    if not year_category_df.empty:
        pie_df = year_category_df[cost_parts].mean().round().reset_index()
        pie_df.columns = ["항목", "금액"]
        fig2 = px.pie(pie_df, names="항목", values="금액", title=f"{year}년 {category} 비용 항목 비율")
        st.plotly_chart(fig2)
    else:
        st.warning("해당 조건에 맞는 데이터가 없습니다.")

# ✅ 바차트: 연도별 업종 평균
elif page == "업종별 평균 바차트":
    st.subheader("연도별 업종간 평균 비교 (수익, 비용, 이익)")

    selected_year = st.selectbox("년도 선택", sorted(df["년도"].unique(), reverse=True), key="year_select_bar")
    year_df = df[df["년도"] == selected_year]

    metrics = ["어업이익(천원)", "총수익(천원)", "총비용(천원)"]
    grouped_df = year_df.groupby("주어업1")[metrics].mean().round().reset_index()
    sorted_order = grouped_df.sort_values(by="어업이익(천원)", ascending=False)["주어업1"].tolist()
    melted_df = grouped_df.melt(id_vars="주어업1", var_name="항목", value_name="금액")
    melted_df["주어업1"] = pd.Categorical(melted_df["주어업1"], categories=sorted_order, ordered=True)

    bar_chart = alt.Chart(melted_df).mark_bar().encode(
        x=alt.X("주어업1:N", sort=sorted_order, title="업종"),
        y=alt.Y("금액:Q", title="평균 금액 (천원)"),
        color="항목:N",
        tooltip=["주어업1", "항목", "금액"]
    ).properties(
        width=800,
        height=500,
        title=f"{selected_year}년 업종별 평균 수익·비용·이익 비교"
    )

    st.altair_chart(bar_chart, use_container_width=True)
