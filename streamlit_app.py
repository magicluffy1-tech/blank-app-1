import streamlit as st
import re

# --- 페이지 설정 ---
st.set_page_config(
    page_title="물 발자국 지능형 계산기",
    page_icon="🧠",
    layout="centered"
)

# --- 지능형 데이터베이스 ---
# 표시 이름, 키워드(유의어/동의어), 기본값, 단위 정보를 포함하는 리스트 구조로 변경
WATER_FOOTPRINT_DATA = [
    # 음식
    {'name': '파스타/스파게티 (1인분)', 'keywords': ['파스타', '스파게티'], 'value': 185, 'unit': '인분'},
    {'name': '짜장면 (1그릇)', 'keywords': ['짜장면', '자장면'], 'value': 600, 'unit': '그릇'},
    {'name': '탕수육 (1인분)', 'keywords': ['탕수육'], 'value': 700, 'unit': '인분'},
    {'name': '양장피 (1인분)', 'keywords': ['양장피'], 'value': 400, 'unit': '인분'},
    {'name': '스프 (1그릇)', 'keywords': ['스프', '수프'], 'value': 100, 'unit': '그릇'},
    {'name': '소고기 (100g)', 'keywords': ['소고기', '소'], 'value': 1540, 'unit': 'g'},
    {'name': '돼지고기 (100g)', 'keywords': ['돼지고기', '돼지'], 'value': 600, 'unit': 'g'},
    {'name': '햄버거 (1개)', 'keywords': ['햄버거', '버거'], 'value': 2500, 'unit': '개'},
    {'name': '라면 (1개)', 'keywords': ['라면'], 'value': 550, 'unit': '개'},

    # 음료
    {'name': '주스 (1잔)', 'keywords': ['주스', '쥬스'], 'value': 150, 'unit': '잔'},
    {'name': '커피 (1잔)', 'keywords': ['커피'], 'value': 140, 'unit': '잔'},
    {'name': '우유 (1잔)', 'keywords': ['우유'], 'value': 200, 'unit': '잔'},

    # 의류
    {'name': '면 티셔츠 (1장)', 'keywords': ['티셔츠', '면티'], 'value': 2700, 'unit': '장'},
    {'name': '바지 (1벌)', 'keywords': ['바지', '슬랙스', '슬렉스', '청바지'], 'value': 8000, 'unit': '벌'},

    # 생활 습관
    {'name': '샤워 (분당)', 'keywords': ['샤워'], 'value': 12, 'unit': '분'},
    {'name': '양치 (1회)', 'keywords': ['양치'], 'value': 6, 'unit': '회'},
]

# --- 기능 함수 ---
def find_footprints_intelligent(text):
    """텍스트에서 키워드와 숫자를 함께 분석하여 물 발자국을 계산하는 지능형 함수"""
    found_items = []
    
    # 중복 계산을 피하기 위해 처리된 텍스트
    processed_text = text
    
    for item in WATER_FOOTPRINT_DATA:
        for keyword in item['keywords']:
            # 텍스트 전체에서 키워드 검색
            if keyword in processed_text:
                # 숫자 및 단위 검색 (예: 3분, 2개, 500ml 등)
                # 키워드 주변의 숫자를 찾기 위한 정규표현식
                pattern = r'(\d+)\s*(?:' + item['unit'] + r'|개|회|분|L|ml|g)?'
                
                # 키워드 앞/뒤 5글자 범위에서 숫자 탐색
                search_range_start = max(0, text.find(keyword) - 5)
                search_range_end = text.find(keyword) + len(keyword) + 5
                search_text = text[search_range_start:search_range_end]
                
                match = re.search(pattern, search_text)
                
                quantity = 1
                if match:
                    quantity = int(match.group(1))

                # 단위별 계산 로직
                calculated_footprint = 0
                if item['unit'] == '분': # 분당 계산
                    calculated_footprint = item['value'] * quantity
                    display_name = f"{item['name'].split(' ')[0]} ({quantity}분)"
                else: # 개당/회당 계산
                    calculated_footprint = item['value'] * quantity
                    display_name = f"{item['name'].split(' ')[0]} ({quantity}{item['unit']})"

                found_items.append({
                    "항목": display_name,
                    "물 발자국 (L)": calculated_footprint
                })

                # 처리된 키워드는 텍스트에서 제거하여 중복 방지 (예: '돼지고기'와 '고기'가 중복 인식되는 것 방지)
                processed_text = processed_text.replace(keyword, "", 1)
                break # 다음 데이터 항목으로 넘어감
    return found_items

# --- 앱 UI 구성 ---
st.title("🧠 물 발자국 지능형 계산기")
st.markdown("이제 문장 속의 **수량이나 시간**까지 똑똑하게 인식하여 계산해요!")
st.info("예: **'오늘 샤워 10분 하고, 티셔츠 1장 세탁기에 돌렸어'**", icon="💡")

st.write("")
user_input = st.text_input(
    "어떤 활동을 하셨나요?",
    placeholder="여기에 활동 내용을 자유롭게 입력해보세요."
)
st.write("---")

if st.button("계산하기!"):
    if user_input:
        results = find_footprints_intelligent(user_input)
        st.subheader("📊 계산 결과")
        if results:
            total_footprint = 0
            for item in results:
                total_footprint += item["물 발자국 (L)"]
                st.success(f"'{item['항목']}'의 물 발자국은 약 **{item['물 발자국 (L)']:,.0f} L** 입니다.")
            
            if len(results) > 1:
                st.write("---")
                st.metric("💧 총합", f"{total_footprint:,.0f} L")
        else:
            st.warning("입력하신 내용에서 계산할 수 있는 항목을 찾지 못했어요.")
            with st.expander("사용 가능한 키워드 예시 보기"):
                st.write([item['name'] for item in WATER_FOOTPRINT_DATA])
    else:
        st.error("계산할 내용을 입력해주세요!")