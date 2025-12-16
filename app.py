import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="AI 추천 기반 시간표 최적화", layout="centered")

st.title("📅 AI 추천 기반 시간표 최적화 시스템")
st.markdown("공부 시간과 휴식을 하루 흐름에 맞게 자동 배치합니다.")

# --------------------
# 입력
# --------------------
sleep = st.slider("하루 수면 시간 (시간)", 4, 10, 7)
start_time = st.time_input("하루 시작 시간", datetime.strptime("08:00", "%H:%M").time())

subjects = st.text_area(
    "과목명과 중요도를 입력하세요 (예: 수학,5)",
    "수학,5\n영어,4\n과학,3"
)

TOTAL_REST = 4  # 휴식 총 시간
REST_UNIT = 1   # 1시간씩 분할
study_time = 24 - sleep - TOTAL_REST

st.write(f"📌 하루 공부 가능 시간: **{study_time}시간**")
st.write("🍽 휴식은 아침 / 점심 / 저녁 / 자기 전으로 분산됩니다")

# --------------------
# 유틸
# --------------------
def hour_to_delta(hour):
    minutes = int(hour * 60)
    return timedelta(minutes=minutes)

# --------------------
# 실행
# --------------------
if st.button("시간표 생성"):
    # 과목 처리
    data = []
    for line in subjects.split("\n"):
        name, weight = line.split(",")
        data.append({"과목": name.strip(), "중요도": int(weight)})

    df = pd.DataFrame(data)
    df["비율"] = df["중요도"] / df["중요도"].sum()
    df["공부시간"] = df["비율"] * study_time

    # --------------------
    # 📊 그래프
    # -------------------
