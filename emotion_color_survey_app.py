# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="정서 색채 설문", layout="centered")
st.title("🎨 정서 경험 유형 및 색채 감정 설문")

# 사용자 정보 입력
name = st.text_input("이름을 입력하세요")
age = st.number_input("나이를 입력하세요", min_value=10, max_value=19)

st.header("1. 정서 경험 유형 분류")

# 정서 인식 명확성 (3문항)
clarity_q1 = st.slider("나는 내 감정을 잘 인식할 수 있다.", 1, 5)
clarity_q2 = st.slider("감정의 종류를 명확히 구별할 수 있다.", 1, 5)
clarity_q3 = st.slider("감정의 원인을 쉽게 파악할 수 있다.", 1, 5)

# 정서 강도 (1문항)
intensity_q = st.slider("감정을 느낄 때 강하게 느끼는 편이다.", 1, 5)

# 정서 경험 유형 계산
clarity_avg = (clarity_q1 + clarity_q2 + clarity_q3) / 3
clarity_sign = "+" if clarity_avg >= 3 else "-"
intensity_sign = "+" if intensity_q >= 3 else "-"

type_map = {
    "++": "격렬형",
    "--": "둔감형",
    "-+": "압도형",
    "+-": "안정형"
}

emotion_code = clarity_sign + intensity_sign
emotion_type = type_map[emotion_code]
st.success(f"👉 당신의 정서 경험 유형은 **{emotion_type}**입니다.")

# 색상 순위 입력
st.header("2. 색채 감정 순위 평가")
st.markdown("다음 12색을 1 (가장 긍정적) ~ 12 (가장 부정적) 순서로 평가해 주세요.")

color_hex = {
    "빨강": "#FF0000", "주황": "#FFA500", "노랑": "#FFFF00",
    "연두": "#ADFF2F", "초록": "#008000", "파랑": "#0000FF",
    "보라": "#800080", "분홍": "#FFC0CB", "갈색": "#A52A2A",
    "하양": "#FFFFFF", "회색": "#808080", "검정": "#000000"
}

color_rank = {}
for color, hex_code in color_hex.items():
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;">
            <div style="width:30px;height:30px;background-color:{hex_code};border:1px solid #000;margin-right:10px;"></div>
            <b>{color}</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    rank = st.number_input(f"{color}의 순위", 1, 12, key=color)
    color_rank[color] = rank

# 배쓰밤 관련
st.header("3. 배쓰밤 관련 질문")
use_bathbomb = st.radio("배쓰밤을 사용할 의향이 있나요?", ["예", "아니오"])
color_consider = st.radio("배쓰밤을 고를 때 색을 고려하나요?", ["예", "아니오"])

# 추가 설문 참여
st.header("4. 추가 설문 참여")
agree_followup = st.radio("2차 설문에 참여하시겠습니까?", ["예", "아니오"])
phone = st.text_input("전화번호를 입력해주세요") if agree_followup == "예" else ""

# 제출 및 결과 다운로드
if st.button("📥 설문 결과 제출"):
    result = {
        "제출시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "이름": name,
        "나이": age,
        "정서유형": emotion_type,
        "명확성 평균": round(clarity_avg, 2),
        "정서 강도": intensity_q,
        "배쓰밤 사용 의향": use_bathbomb,
        "배쓰밤 색 고려 여부": color_consider,
        "2차 참여": agree_followup,
        "전화번호": phone
    }

    # 색상 순위 추가
    for color in color_hex:
        result[f"{color} 순위"] = color_rank[color]

    df = pd.DataFrame([result])
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📄 CSV 파일 다운로드",
        data=csv,
        file_name=f"{name}_emotion_survey.csv",
        mime="text/csv"
    )
