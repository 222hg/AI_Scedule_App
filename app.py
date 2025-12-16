import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI 추천 기반 시간표 최적화", layout="centered")

st.title("📅 AI 추천 기반 시간표 최적화 시스템")

st.markdown("공부 가능 시간을 입력하면, 과목 중요도에 따라 자동으로 시간표를 추천합니다.")

sleep = st.slider("하루 수면 시간 (시간)", 4, 10, 7)

st.subheader("과목 입력")
subjects = st.text_area(
    "과목명과 중요도를 입력하세요 (예: 수학,5)",
    "수학,5\n영어,4\n과학,3"
)

study_time = 24 - sleep - 4  # 식사/휴식 4시간 고정
st.write(f"📌 하루 공부 가능 시간: **{study_time}시간**")

if st.button("시간표 생성"):
    data = []
    for line in subjects.split("\n"):
        name, weight = line.split(",")
        data.append({"과목": name.strip(), "중요도": int(weight)})

    df = pd.DataFrame(data)
    df["비율"] = df["중요도"] / df["중요도"].sum()
    df["추천 공부 시간(시간)"] = (df["비율"] * study_time).round(1)

    st.success("✅ 시간표 생성 완료!")
    st.dataframe(df)
