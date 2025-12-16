import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="AI 추천 기반 시간표 최적화", layout="centered")

st.title("📅 AI 추천 기반 시간표 최적화 시스템")
st.markdown("공부 시간과 휴식을 하루 흐름에 맞게 자동 배치합니다.")

sleep = st.slider("하루 수면 시간 (시간)", 4, 10, 7)
start_time = st.time_input("하루 시작 시간", datetime.strptime("08:00", "%H:%M").time())

subjects = st.text_area(
    "과목명과 중요도를 입력하세요 (예: 수학,5)",
    "수학,5\n영어,4\n과학,3"
)

TOTAL_REST = 4
REST_UNIT = 1
study_time = 24 - sleep - TOTAL_REST

st.write(f"📌 하루 공부 가능 시간: **{study_time}시간**")

def hour_to_delta(hour):
    return timedelta(minutes=int(hour * 60))

if st.button("시간표 생성"):
    data = []

    for line in subjects.split("\n"):
        line = line.strip()
        if not line or "," not in line:
            continue  # 잘못된 줄 무시

        name, weight = line.split(",", 1)

        try:
            weight = int(weight)
        except:
            continue

        data.append({"과목": name.strip(), "중요도": weight})

    if len(data) == 0:
        st.error("❌ 과목 입력 형식이 올바르지 않습니다.")
        st.stop()

    df = pd.DataFrame(data)
    df["비율"] = df["중요도"] / df["중요도"].sum()
    df["공부시간"] = df["비율"] * study_time

    # 📊 그래프
    st.subheader("📊 과목별 추천 공부 시간")
    st.bar_chart(df.set_index("과목")["공부시간"])

    # 🕒 시간표
    st.subheader("🕒 하루 시간표")

    schedule = []
    now = datetime.combine(datetime.today(), start_time)

    rest_labels = [
        "🍳 아침 / 휴식",
        "🍽 점심 / 휴식",
        "🍽 저녁 / 휴식",
        "🌙 자기 전 휴식"
    ]

    rest_idx = 0

    for _, row in df.iterrows():
        if rest_idx < 4:
            rest_duration = timedelta(hours=REST_UNIT)
            schedule.append({
                "시간": f"{now.strftime('%H:%M')} ~ {(now + rest_duration).strftime('%H:%M')}",
                "활동": rest_labels[rest_idx]
            })
            now += rest_duration
            rest_idx += 1

        study_duration = hour_to_delta(row["공부시간"])
        schedule.append({
            "시간": f"{now.strftime('%H:%M')} ~ {(now + study_duration).strftime('%H:%M')}",
            "활동": f"{row['과목']} 공부"
        })
        now += study_duration

    while rest_idx < 4:
        rest_duration = timedelta(hours=REST_UNIT)
        schedule.append({
            "시간": f"{now.strftime('%H:%M')} ~ {(now + rest_duration).strftime('%H:%M')}",
            "활동": rest_labels[rest_idx]
        })
        now += rest_duration
        rest_idx += 1

    st.success("✅ 시간표 생성 완료!")
    st.dataframe(pd.DataFrame(schedule))
