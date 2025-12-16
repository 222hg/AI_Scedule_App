import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI 추천 기반 시간표 최적화 시스템")
st.write("개인의 집중도와 과목 특성을 기반으로 하루 시간표를 추천합니다.")

st.divider()

sleep_hours = st.slider("수면 시간 (시간)", 4, 10, 7)

subjects = []
st.subheader("과목 정보 입력")

for i in range(3):
    name = st.text_input(f"과목 {i+1} 이름", key=f"name{i}")
    importance = st.slider("중요도", 1, 5, 3, key=f"imp{i}")
    difficulty = st.slider("난이도", 1, 5, 3, key=f"diff{i}")

    if name:
        subjects.append({
            "name": name,
            "importance": importance,
            "difficulty": difficulty
        })

def focus_level(hour, sleep):
    focus = 0.6
    if 9 <= hour <= 11:
        focus += 0.3
    if 13 <= hour <= 15:
        focus -= 0.2
    if hour >= 21:
        focus -= 0.3
    focus += (sleep - 7) * 0.05
    return max(0.1, min(focus, 1.0))

def score(subject, hour):
    return subject["importance"] * subject["difficulty"] * focus_level(hour, sleep_hours)

hours = list(range(8, 23))

if st.button("시간표 생성"):
    if not subjects:
        st.warning("과목을 하나 이상 입력하세요.")
    else:
        schedule = []
        for hour in hours:
            best = max(subjects, key=lambda s: score(s, hour))
            schedule.append({"시간": f"{hour}:00", "과목": best["name"]})

        df = pd.DataFrame(schedule)
        st.dataframe(df)

        focus_values = [focus_level(h, sleep_hours) for h in hours]
        fig = plt.figure()
        plt.plot(hours, focus_values)
        st.pyplot(fig)
