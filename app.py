import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="AI 추천 기반 시간표 최적화", layout="centered")

st.title("📅 AI 추천 기반 시간표 최적화 시스템")
st.markdown("과목 중요도를 기반으로 공부 시간과 하루 시간표를 자동 생성합니다.")

# --------------------
# 입력 영역
# --------------------
sleep = st.slider("하루 수면 시간 (시간)", 4, 10, 7)

start_time_str = st.time_input("하루 시작 시간", value=datetime.strptime("08:00", "%H:%M").time())

subjects = st.text_area(
    "과목명과 중요도를 입력하세요 (예: 수학,5)",
    "수학,5\n영어,4\n과학,3"
)

# 고정 휴식 시간
rest_time = 4
study_time = 24 - sleep - rest_time

st.write(f"📌 하루 공부 가능 시간: **{study_time}시간**")
st.write(f"🍚 휴식/식사 시간: **{rest_time}시간**")

# --------------------
# 유틸 함수
# --------------------
def hour_to_hm(hour):
    total_min = int(hour * 60)
    return total_min // 60, total_min % 60

# --------------------
# 버튼 클릭 시 실행
# --------------------
if st.button("시간표 생성"):
    # 과목 데이터 처리
    data = []
    for line in subjects.split("\n"):
        name, weight = line.split(",")
        data.append({"과목": name.strip(), "중요도": int(weight)})

    df = pd.DataFrame(data)
    df["비율"] = df["중요도"] / df["중요도"].sum()
    df["공부시간(시간)"] = df["비율"] * study_time

    # --------------------
    # 1️⃣ 막대 그래프
    # --------------------
    st.subheader("📊 과목별 추천 공부 시간")
    chart_df = df.set_index("과목")["공부시간(시간)"]
    st.bar_chart(chart_df)

    # --------------------
    # 2️⃣ 실제 시간표 생성
    # --------------------
    st.subheader("🕒 하루 시간표")

    schedule = []
    current_time = datetime.combine(datetime.today(), start_time_str)

    # 공부 시간 배치
    for _, row in df.iterrows():
        h, m = hour_to_hm(row["공부시간(시간)"])
        duration = timedelta(hours=h, minutes=m)

        schedule.append({
            "시간": f"{current_time.strftime('%H:%M')} ~ {(current_time + duration).strftime('%H:%M')}",
            "활동": f"{row['과목']} 공부"
        })

        current_time += duration

    # 휴식 시간 추가
    rest_duration = timedelta(hours=rest_time)
    schedule.append({
        "시간": f"{current_time.strftime('%H:%M')} ~ {(current_time + rest_duration).strftime('%H:%M')}",
        "활동": "🍽 식사 / 휴식"
    })

    schedule_df = pd.DataFrame(schedule)

    st.success("✅ 시간표 생성 완료!")
    st.dataframe(schedule_df)
