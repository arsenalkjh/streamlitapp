import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import matplotlib.ticker as ticker  # 상단에 추가


# ✅ 한글 폰트 설정
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# 이후 시각화 코드...

# 데이터 불러오기 및 전처리
df = pd.read_csv("업종별회계.csv")

# 불필요한 인덱스 열 제거 (Unnamed: 0)
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# melt 변환
df_melted = df.melt(id_vars=["업종", "항목"], var_name="Year", value_name="Amount")

# 페이지 타이틀
st.title("Industry-wise Revenue, Cost, and Profit Trends")

# 업종 선택
selected_industry = st.selectbox("Select Industry", df["업종"].unique())

# 항목 선택
selected_items = st.multiselect("Select Item(s)", ["수익", "비용", "이익"], default=["수익", "비용", "이익"])

# 필터링
filtered = df_melted[
    (df_melted["업종"] == selected_industry) &
    (df_melted["항목"].isin(selected_items))
]

# 라인 그래프
st.subheader(f"Trend by Year for {selected_industry}")
fig, ax = plt.subplots()
for item in selected_items:
    data = filtered[filtered["항목"] == item]
    ax.plot(data["Year"], data["Amount"], marker="o", label=item)
    
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.tick_params(axis='y', labelsize=9)  # Y축 숫자 폰트 크기 줄임
ax.tick_params(axis='x', labelsize=9)  # X축 연도 폰트 크기 줄임

ax.set_ylabel("Amount")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 연도별 전체 업종 비교 막대 그래프
st.subheader("Comparison Across Industries by Year")
selected_year = st.selectbox("Select Year", df.columns[3:])
filtered_year = df_melted[df_melted["Year"] == selected_year]

fig2, ax2 = plt.subplots(figsize=(10, 6))
width = 0.25
x = range(len(filtered_year["업종"].unique()))
for i, item in enumerate(["수익", "비용", "이익"]):
    sub = filtered_year[filtered_year["항목"] == item]
    ax2.bar(
        [xi + i * width for xi in x],
        sub["Amount"],
        width=width,
        label=item
    )
ax2.set_xticks([xi + width for xi in x])
ax2.set_xticklabels(filtered_year["업종"].unique(), rotation=90)
ax2.set_ylabel("Amount")
ax2.legend()
st.pyplot(fig2)
