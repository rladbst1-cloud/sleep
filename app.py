import random
import pandas as pd
import streamlit as st

# 1. 제목 설정
st.title("😴 수면 피로도 측정기")
st.write("수면 시간과 기상 후 컨디션을 선택하고 나의 피로도와 맞춤 회복 활동을 확인해보세요!")
st.divider()

# 입력 리스트 정의 (3~12시간)
sleep_hours_list = list(range(3, 13))
condition_list = ["찌뿌둥함", "평범함", "개운함"]

# 1- 수면시간 입력 (리스트 사용, 기본값 7시간)
sleep_hours = st.selectbox("1. 어젯밤 수면 시간을 선택하세요 (시간)", sleep_hours_list, index=4)

# 2- 기상 후 컨디션 입력 (리스트 사용)
condition = st.selectbox("2. 기상 후 컨디션은 어떤가요?", condition_list)

st.write("")

# 버튼 클릭 시 결과 출력
if st.button("피로도 측정 및 활동 추천받기", type="primary"):
    
    # 이차함수 수식 계산: y = 2.5(수면시간 - 8)^2 + 30
    fatigue_score = int(2.5 * ((sleep_hours - 8) ** 2) + 30)
    
    # random 라이브러리 활용 (약간의 랜덤 변동값 추가, 0~100점 사이로 제한)
    fatigue_score += random.randint(0, 5)
    fatigue_score = max(0, min(100, fatigue_score))

    st.divider()
    
    # 수정된 조건: 5시간 이하(수면 부족) 또는 11시간 이상(과수면)일 때 피로도 높음!
    if sleep_hours <= 5 or sleep_hours >= 11:
        status_msg = "🚨 피로도가 높습니다. 충분한 휴식과 이완이 필요해요!"
        activities = [
            {"활동명": "전신 스트레칭", "시간": "10분", "효과": "뭉친 근육 이완 및 개운해짐"},
            {"활동명": "가벼운 산책", "시간": "15분", "효과": "무거운 몸 깨우기 및 활력 충전"}
        ]
    elif sleep_hours <= 7 or sleep_hours == 10:
        status_msg = "⚠️ 피로도가 보통입니다. 가벼운 리프레시가 도움이 됩니다."
        activities = [
            {"활동명": "시원한 물 한 잔 마시기", "시간": "3분", "효과": "신진대사 활성화 및 잠 깨우기"},
            {"활동명": "목·어깨 마사지", "시간": "5분", "효과": "상체 긴장 완화 및 개운함"}
        ]
    else:  # 8~9시간 적정 수면을 잤을 때
        status_msg = "✨ 피로도가 낮고 개운한 상태입니다! 활기찬 하루를 보내세요."
        activities = [
            {"활동명": "가벼운 유산소 운동", "시간": "20분", "효과": "체력 증진 및 활력 유지"},
            {"활동명": "명상 및 심호흡", "시간": "5분", "효과": "맑은 정신 유지"}
        ]

    # 추천 활동 2개를 랜덤 순서로 섞기
    selected_activities = random.sample(activities, 2)

    # --- 결과 출력 화면 ---
    # 1) 강조 수치
    st.metric(label="현재 나의 피로도 점수", value=f"{fatigue_score} 점")
    
    # 2) 텍스트 메시지 출력
    if sleep_hours <= 5 or sleep_hours >= 11:
        st.error(status_msg)
    elif sleep_hours <= 7 or sleep_hours == 10:
        st.warning(status_msg)
    else:
        st.success(status_msg)

    # 3) 테이블/표 출력 (활동명 / 시간 / 효과)
    st.subheader("💡 추천 피로 회복 활동")
    df = pd.DataFrame(selected_activities)
    st.table(df)
