import streamlit as st
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# 나눔고딕 다운로드 및 적용
font_url = "https://github.com/park1200656/fonts/blob/main/NanumGothic.ttf?raw=true"
font_path = "/tmp/NanumGothic.ttf"

try:
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)

    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    print("폰트 다운로드 실패:", e)
    plt.rcParams['font.family'] = 'sans-serif'


# ✅ 데이터 불러오기
df = pd.read_csv("업종별회계.csv")

# Unnamed: 0 제거
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# 연도별 melt 변환
df_melted = df.melt(id_vars=["업종", "항목"], var_name="Year", value_name="Amount")
df_melted["Year"] = df_melted["Year"].astype(str)
df_melted = df_melted.sort_values(by="Year")

# ✅ 페이지 제목
st.title("📊 업종별 수익·비용·이익 추이 분석")

# ✅ 업종 선택
selected_industry = st.selectbox("업종 선택", df["업종"].unique())

# ✅ 항목 선택
selected_items = st.multiselect("항목 선택", ["수익", "비용", "이익"], default=["수익", "비용", "이익"])

# ✅ 데이터 필터링
filtered = df_melted[
    (df_melted["업종"] == selected_industry) &
    (df_melted["항목"].isin(selected_items))
]

# ✅ 꺾은선 그래프 출력
st.subheader(f"📈 {selected_industry}의 연도별 추이")
fig, ax = plt.subplots()
for 항목 in selected_items:
    data = filtered[filtered["항목"] == 항목]
    ax.plot(data["Year"], data["Amount"], marker="o", label=항목)

# 포맷 및 폰트 크기 설정
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.tick_params(axis='y', labelsize=9)
ax.tick_params(axis='x', labelsize=9)
ax.set_ylabel("금액")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ✅ 전체 업종 비교 그래프
st.subheader("📊 연도별 업종 비교")
selected_year = st.selectbox("연도 선택", df.columns[3:])

filtered_year = df_melted[df_melted["Year"] == selected_year]
fig2, ax2 = plt.subplots(figsize=(10, 6))
width = 0.25
x = range(len(filtered_year["업종"].unique()))

for i, 항목 in enumerate(["수익", "비용", "이익"]):
    sub = filtered_year[filtered_year["항목"] == 항목]
    ax2.bar(
        [xi + i * width for xi in x],
        sub["Amount"],
        width=width,
        label=항목
    )

ax2.set_xticks([xi + width for xi in x])
ax2.set_xticklabels(filtered_year["업종"].unique(), rotation=90, fontsize=9)
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2.set_ylabel("금액")
ax2.legend()
st.pyplot(fig2)
