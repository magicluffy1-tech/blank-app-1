import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(
    page_title="물 발자국 키워드 계산기",
    page_icon="🔍",
    layout="centered"
)

# --- 데이터베이스 ---
# 키워드를 중심으로 데이터 재구성. 의류 등 항목 추가
# 긴 이름보다 '청바지', '소고기' 등 핵심 단어를 키로 사용
WATER_FOOTPRINT_DATA = {
    # 의류
    "청바지": 10000,
    "면 티셔츠": 2700,
    "신발": 8000,
    # 음식
    "사과": 125,
    "바나나": 100,
    "소고기": 1540,  # 100g 기준
    "돼지고기": 600, # 100g 기준
    "닭고기": 430,  # 100g 기준
    "계란": 200,
    "쌀밥": 260,
    "식빵": 40,
    "라면": 550,
    # 음료
    "물": 0.2,
    "우유": 200,
    "커피": 140,
    "콜라": 75,
    # 생활
    "샤워": 60,
    "세수": 12,
    "양치": 6,
    "설거지": 120,
    "세탁기": 150,
}

# --- 기능 함수 ---
def find_footprints_from_text(text):
    """
    입력된 텍스트에서 데이터베이스의 키워드를 찾아
    물 발자국 정보를 리스트로 반환하는 함수
    """
    found_items = []
    # 텍스트에 어떤 키워드가 포함되어 있는지 모두 확인
    for keyword, footprint in WATER_FOOTPRINT_DATA.items():
        if keyword in text:
            found_items.append({"항목": keyword, "물 발자국 (L)": footprint})
    return found_items

# --- 앱 UI 구성 ---
st.title("🔍 물 발자국 키워드 계산기")
st.markdown("궁금한 활동이나 물건의 이름을 문장에 포함하여 입력해보세요!")
st.info("예: **'청바지 입고 커피 한 잔'**, **'오늘 저녁은 소고기'**", icon="💡")

# 여백 추가
st.write("")

# 사용자 텍스트 입력
user_input = st.text_input(
    "어떤 활동을 하셨나요?",
    placeholder="여기에 활동 내용을 입력하세요. (예: 라면 먹고 샤워함)"
)

# 논리적인 코드 블록 사이에 한 줄의 공백을 넣어 시각적으로 구분
st.write("---")

# 사용자가 버튼을 클릭했을 때만 계산 로직 실행
if st.button("물 발자국 계산하기!"):
    if user_input:
        # 입력된 텍스트에서 물 발자국 정보 찾기
        results = find_footprints_from_text(user_input)

        st.subheader("📊 계산 결과")
        # 결과가 있는지 확인
        if results:
            total_footprint = 0
            for item in results:
                total_footprint += item["물 발자국 (L)"]
                # 각 항목별 결과 표시
                st.success(f"'{item['항목']}'의 물 발자국은 약 **{item['물 발자국 (L)']:,.0f} L** 입니다.")
            
            # 2개 이상의 항목이 발견되면 총합도 보여줌
            if len(results) > 1:
                st.write("---")
                st.metric("💧 발견된 항목들의 총합", f"{total_footprint:,.0f} L")

        else:
            # 일치하는 키워드가 없을 경우
            st.warning("입력하신 내용에서 계산할 수 있는 항목을 찾지 못했어요.")
            with st.expander("사용 가능한 키워드 예시 보기"):
                # 사용 가능한 키워드 목록을 보여주어 사용자 입력 유도
                st.write(list(WATER_FOOTPRINT_DATA.keys()))
    else:
        # 아무것도 입력하지 않았을 경우
        st.error("계산할 내용을 입력해주세요!")