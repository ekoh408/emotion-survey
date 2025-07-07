# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_sortables import sort_items

st.set_page_config(page_title="정서 색채 설문", layout="centered")
st.title("🎨 정서 경험 유형 및 색채 감정 설문")

# 사용자 정보 입력
name = st.text_input("이름을 입력하세요")
age = st.number_input("나이를 입력하세요", min_value=10, max_value=19)

st.header("1. 정서 경험 유형 분류")

# 점수 표시용 라벨
labels = ["1 - 매우 아니다", "2 - 약간 아니다", "3 - 보통이다", "4 - 약간 그렇다", "5 - 매우 그렇다"]

# 정서 인식 명확성 (3문항)
clarity_q1 = st.radio("나는 평소 내가 느끼는 감정에 관심을 기울이는 편이다.", list(range(1, 6)), format_func=lambda x: labels[x-1])
clarity_q2 = st.radio("나는 지금 내가 어떤 감정을 느끼는지 스스로 명확히 말할 수 있다.", list(range(1, 6)), format_func=lambda x: labels[x-1])
clarity_q3 = st.radio("나는 언제든지 내 감정을 조절할 수 있다고 믿는다.", list(range(1, 6)), format_func=lambda x: labels[x-1])

# 정서 강도 (1문항)
intensity_q1 = st.radio("특정 감정을 느끼면 쉽게 잊지 못하고 오래 지속된다.", list(range(1, 6)), format_func=lambda x: labels[x-1])

# 정서 경험 유형 계산
clarity_avg = (clarity_q1 + clarity_q2 + clarity_q3) / 3
intensity_avg = intensity_q1

clarity_sign = "+" if clarity_avg >= 3 else "-"
intensity_sign = "+" if intensity_avg >= 3 else "-"

type_map = {
    "++": "격렬형",
    "--": "둔감형",
    "-+": "압도형",
    "+-": "안정형"
}

emotion_code = clarity_sign + intensity_sign
emotion_type = type_map[emotion_code]
st.success(f"👉 당신의 정서 경험 유형은 **{emotion_type}**입니다.")

# 색상 순위 입력 (텍스트 기반 드래그 + 별도 시각화)
st.header("2. 색채 감정 순위 평가")
st.markdown("아래 색상들을 **가장 긍정적인 색부터 차례대로 드래그하세요.**")

color_hex = {
    "빨강": "#FF0000", "주황": "#FFA500", "노랑": "#FFFF00",
    "연두": "#ADFF2F", "초록": "#008000", "파랑": "#0000FF",
    "보라": "#800080", "분홍": "#FFC0CB", "갈색": "#A52A2A",
    "하양": "#FFFFFF", "회색": "#808080", "검정": "#000000"
}

# 드래그용 텍스트 리스트
items = [f"{color} ({color_hex[color]})" for color in color_hex]
sorted_items = sort_items(items, direction="vertical")
sorted_colors = [item.split()[0] for item in sorted_items]
color_rank = {color: idx + 1 for idx, color in enumerate(sorted_colors)}

# 시각적 보조 표시
st.markdown("### 선택한 순서:")
for color in sorted_colors:
    st.markdown(
        f"<div style='display:flex;align-items:center;margin-bottom:4px;'>"
        f"<div style='width:25px;height:25px;background-color:{color_hex[color]};border:1px solid #000;margin-right:10px;'></div>"
        f"<b>{color}</b></div>",
        unsafe_allow_html=True
    )

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
        "정서 강도": intensity_avg,
        "배쓰밤 사용 의향": use_bathbomb,
        "배쓰밤 색 고려 여부": color_consider,
        "2차 참여": agree_followup,
        "전화번호": phone
    }

    for color in color_hex:
        result[f"{color} 순위"] = color_rank.get(color, "")

    df = pd.DataFrame([result])
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📄 CSV 파일 다운로드",
        data=csv,
        file_name=f"{name}_emotion_survey.csv",
        mime="text/csv"
    )
