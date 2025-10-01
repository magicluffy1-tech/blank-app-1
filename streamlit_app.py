import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(
    page_title="물 발자국 키워드 계산기 (종합)",
    page_icon="🌍",
    layout="centered"
)

# --- 종합 데이터베이스 ---
# 학생들이 사용할 만한 일반적인 데이터를 최대한 확장하여 추가했습니다.
WATER_FOOTPRINT_DATA = {
    # 🥩 육류/단백질
    "소고기": 1540,  # 100g 기준
    "돼지고기": 600, # 100g 기준
    "닭고기": 430,  # 100g 기준
    "계란": 200,    # 1개 기준
    "치즈": 125,    # 슬라이스 1장(25g) 기준
    "두부": 200,    # 100g 기준

    # 🍞 곡물/탄수화물
    "쌀밥": 260,     # 1공기 기준
    "식빵": 40,      # 1조각 기준
    "라면": 550,     # 1개 기준
    "햄버거": 2500,  # 1개 기준
    "파스타": 185,   # 1인분(100g) 기준

    # 🍎 과일/채소
    "사과": 125,     # 1개 기준
    "바나나": 100,    # 1개 기준
    "오렌지": 80,    # 1개 기준
    "토마토": 50,    # 1개 기준
    "감자": 25,      # 1개 기준
    "양상추": 20,    # 50g 기준

    # 🍫 간식
    "초콜릿": 1700,  # 100g 바 기준
    "감자칩": 185,   # 작은 봉지(60g) 기준
    "견과류": 240,   # 한 줌(30g) 기준 (아몬드)

    # ☕ 음료
    "물": 0.2,       # 1잔(200ml) 기준
    "우유": 200,     # 1잔(200ml) 기준
    "커피": 140,     # 1잔 기준
    "콜라": 75,      # 1캔(355ml) 기준
    "오렌지주스": 200,# 1잔(200ml) 기준
    "차": 30,        # 1잔(녹차) 기준

    # 👕 생활용품/의류
    "청바지": 10000, # 1벌 기준
    "티셔츠": 2700,   # 면 티셔츠 1장 기준
    "신발": 8000,    # 운동화 1켤레 기준
    "종이": 10,       # A4용지 1장 기준
    "공책": 200,     # 종이 20장 분량

    # 🚿 생활 습관
    "샤워": 60,      # 5분 기준
    "세수": 12,      # 물을 틀어놓고 할 경우
    "양치": 6,       # 컵을 사용하지 않을 경우
    "손 씻기": 3,   # 30초 기준
    "설거지": 120,    # 10분 기준
    "세탁기": 150,    # 1회 사용 기준
    "화장실": 8,     # 변기 물 1회 내리기
}

# --- 기능 함수 ---
def find_footprints_from_text(text):
    """입력된 텍스트에서 데이터베이스의 키워드를 찾아 물 발자국 정보를 리스트로 반환"""
    found_items = []
    # 사용자가 입력한 텍스트에서 공백을 제거하여 '면 티셔츠' 같은 키워드 대응
    processed_text = text.replace(" ", "")

    # 키워드를 길이순으로 정렬하여 긴 키워드(예: 돼지고기)가 짧은 키워드(예: 고기)보다 먼저 인식되도록 함
    sorted_keywords = sorted(WATER_FOOTPRINT_DATA.keys(), key=len, reverse=True)

    for keyword in sorted_keywords:
        processed_keyword = keyword.replace(" ", "")
        if processed_keyword in processed_text:
            # 수량 인식을 위한 간단한 로직 (예: "사과 3개")
            # 이 부분은 단순 구현으로, 복잡한 문장은 정확하지 않을 수 있음
            count = 1
            # 키워드 앞의 숫자 찾기 (미래 확장성)
            
            found_items.append({"항목": keyword, "물 발자국 (L)": WATER_FOOTPRINT_DATA[keyword] * count})
            processed_text = processed_text.replace(processed_keyword, "", 1)
            
    return found_items

# --- 앱 UI 구성 ---
st.title("🌍 물 발자국 키워드 계산기")
st.markdown("궁금한 활동이나 물건의 이름을 문장에 포함하여 입력해보세요!")
st.info("예: **'초콜릿 먹고 청바지 입기'**, **'오늘 점심은 햄버거 세트'**", icon="💡")

st.write("")

user_input = st.text_input(
    "어떤 활동을 하셨나요?",
    placeholder="여기에 활동 내용을 입력하세요. (예: 점심에 파스타 먹고 양치함)"
)

st.write("---")

if st.button("물 발자국 계산하기!"):
    if user_input:
        # '세트' 메뉴를 위한 자동 키워드 추가
        if "세트" in user_input and ("버거" in user_input or "햄버거" in user_input):
            user_input += " 감자칩 콜라"

        results = find_footprints_from_text(user_input)

        st.subheader("📊 계산 결과")
        if results:
            total_footprint = 0
            for item in results:
                total_footprint += item["물 발자국 (L)"]
                st.success(f"'{item['항목']}'의 물 발자국은 약 **{item['물 발자국 (L)']:,.0f} L** 입니다.")
            
            if len(results) > 1:
                st.write("---")
                st.metric("💧 발견된 항목들의 총합", f"{total_footprint:,.0f} L")
        else:
            st.warning("입력하신 내용에서 계산할 수 있는 항목을 찾지 못했어요.")
            with st.expander("사용 가능한 키워드 예시 보기"):
                st.write(sorted(list(WATER_FOOTPRINT_DATA.keys())))
    else:
        st.error("계산할 내용을 입력해주세요!")