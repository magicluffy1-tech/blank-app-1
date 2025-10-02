import streamlit as st
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="나의 하루 물 발자국 일기",
    page_icon="✍️",
    layout="wide"
)

# --- 전체 데이터베이스 (카테고리별 구성) ---
# 이전과 동일한 종합 데이터를 사용합니다.
CATEGORIZED_DATA = {
    "🥩 육류, 해산물 & 단백질": {
        "소고기 (100g)": 1540, "양고기 (100g)": 1040, "돼지고기 (100g)": 600, "닭고기 (100g)": 430,
        "연어 (양식, 100g)": 120, "새우 (양식, 100g)": 260, "참치 (통조림, 1캔)": 240,
        "계란 (1개)": 200, "치즈 (100g)": 500, "두부 (100g)": 200, "우유 (1잔, 250ml)": 255,
        "버터 (1큰술, 14g)": 78, "요거트 (1컵, 100g)": 130,
    },
    "🍞 곡물, 빵 & 면": {
        "쌀밥 (1공기)": 250, "밀(빵) (100g)": 160, "옥수수 (100g)": 122, "귀리(오트밀) (1회분, 50g)": 120,
        "파스타/스파게티 (1인분)": 185, "짜장면 (1그릇)": 600, "라면 (1개)": 550, "햄버거 (1개)": 2500,
    },
    "🍎 과일 & 채소": {
        "사과 (1개)": 82, "바나나 (1개)": 79, "오렌지 (1개)": 50, "토마토 (1개)": 21, "포도 (1kg)": 610,
        "딸기 (1개)": 4, "감자 (1개)": 25, "양배추 (1통)": 280, "오이 (1개)": 105,
        "피망/파프리카 (1개)": 55, "양상추 (한 줌)": 10, "양파 (1개)": 13, "아보카도 (1개)": 227,
    },
    "🍫 간식 & 가공식품": {
        "초콜릿 (100g)": 1700, "감자칩 (작은 봉지)": 185, "견과류(아몬드) (한 줌)": 82,
        "호두 (한 줌)": 270, "피자 (한 판)": 1200, "설탕 (100g)": 178, "올리브 오일 (100ml)": 1440,
        "케첩 (1병)": 5, "마요네즈 (1병)": 25,
    },
    "🥤 음료": {
        "커피 (1잔)": 132, "차(Tea) (1잔)": 27, "맥주 (1잔, 250ml)": 74, "와인 (1잔, 125ml)": 120,
        "오렌지 주스 (1잔)": 200, "탄산음료(콜라) (1캔)": 75, "마시는 물 (1잔, 250ml)": 0.25,
    },
    "👕 의류 & 생활용품": {
        "면 티셔츠 (1장)": 2700, "청바지 (1벌)": 8000, "운동화 (1켤레)": 8000, "가죽 신발 (1켤레)": 14500,
        "종이 (A4 1장)": 10, "책 (200p)": 250, "타이어 (1개)": 2000, "스마트폰 (1대)": 12000,
    },
    "🚿 생활 습관 및 서비스": {
        "샤워 (분당)": 12, "목욕 (1회)": 200, "양치(물 끄고) (1회)": 1, "양치(물 틀고) (1회)": 6,
        "손 씻기 (1회)": 3, "설거지(기계) (1회)": 15, "설거지(손) (분당)": 8, "세탁기 (1회)": 150,
        "화장실(변기) (1회)": 6,
    }
}

# --- 상태 관리 (Session State) ---
if 'daily_records' not in st.session_state:
    st.session_state.daily_records = []
if 'journal_text' not in st.session_state:
    st.session_state.journal_text = ""

# --- 기능 함수 ---
def add_record(category, item, quantity):
    if quantity > 0:
        footprint = CATEGORIZED_DATA[category][item] * quantity
        st.session_state.daily_records.append({
            "카테고리": category, "항목": item, "수량": quantity, "물 발자국 (L)": footprint
        })
        st.sidebar.success(f"'{item}' {quantity}개 추가 완료!")

def clear_all():
    st.session_state.daily_records = []
    st.session_state.journal_text = ""

# --- 사이드바 (사용자 입력) ---
st.sidebar.header("💧 항목 추가하기")
category_list = list(CATEGORIZED_DATA.keys())
selected_category = st.sidebar.selectbox("1. 카테고리를 선택하세요.", category_list)

if selected_category:
    item_list = list(CATEGORIZED_DATA[selected_category].keys())
    selected_item = st.sidebar.selectbox("2. 세부 항목을 선택하세요.", item_list)

quantity = st.sidebar.number_input("3. 수량 (개수/횟수/분 등)을 입력하세요.", min_value=1, step=1)
st.sidebar.button("리스트에 추가하기", on_click=add_record, args=(selected_category, selected_item, quantity))
st.sidebar.write("---")
if st.sidebar.button("오늘 기록 초기화"):
    clear_all()
    st.sidebar.warning("오늘의 모든 기록이 삭제되었습니다.")

# --- 메인 화면 ---
st.title("✍️ 나의 하루 물 발자국 일기")
st.markdown("오늘 하루 어떤 활동을 했고 무엇을 먹었는지 간단하게 일기를 작성한 후, 계산 목록과 비교해보세요!")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("📓 나의 하루 일기")
    st.session_state.journal_text = st.text_area(
        "일기 작성",
        height=200,
        placeholder="예: 아침에 사과 1개를 먹고 5분간 샤워했다. 점심에는 라면을 먹었고, 저녁에는 친구와 피자 한 판을 나눠 먹었다.",
        value=st.session_state.journal_text
    )

    if st.button("✅ 내 일과 점검하기!"):
        if not st.session_state.journal_text:
            st.error("먼저 일기를 작성해주세요!")
        else:
            journal_text = st.session_state.journal_text
            
            # 1. 일기에서 키워드 추출
            mentioned_keywords = set()
            for category_data in CATEGORIZED_DATA.values():
                for item_name in category_data.keys():
                    # '소고기 (100g)' -> '소고기' 처럼 기본 단어만 추출하여 비교
                    base_keyword = item_name.split(" ")[0].split("(")[0]
                    if base_keyword in journal_text:
                        mentioned_keywords.add(base_keyword)

            # 2. 계산 목록에서 키워드 추출
            logged_keywords = set()
            for record in st.session_state.daily_records:
                base_keyword = record['항목'].split(" ")[0].split("(")[0]
                logged_keywords.add(base_keyword)
            
            # 3. 두 목록 비교
            matched = logged_keywords.intersection(mentioned_keywords)
            forgotten = mentioned_keywords - logged_keywords
            extra = logged_keywords - mentioned_keywords

            with st.expander("🔍 점검 결과 보기", expanded=True):
                st.write("작성한 일기와 계산 목록을 비교한 결과입니다.")
                if forgotten:
                    st.warning(f"**🤔 혹시 빠뜨렸나요?**\n\n일기에는 있지만, 계산 목록에 없는 항목: **{', '.join(forgotten)}**")
                else:
                    st.success("**🎉 완벽해요!**\n\n일기에 언급된 모든 항목이 계산 목록에 포함되었습니다.")
                
                if extra:
                    st.info(f"**확인해보세요**\n\n계산 목록에는 있지만, 일기에 없는 항목: **{', '.join(extra)}**")
                
                if matched:
                    st.write(f"**일치하는 항목:** {', '.join(matched)}")


with col2:
    st.subheader("🧮 계산 결과")
    if not st.session_state.daily_records:
        st.info("왼쪽 사이드바에서 항목을 추가하고, 일기를 작성한 후 점검해보세요.")
    else:
        records_df = pd.DataFrame(st.session_state.daily_records)
        total_footprint = records_df["물 발자국 (L)"].sum()

        st.metric(label="오늘의 총 물 발자국 (L)", value=f"{total_footprint:,.0f} L")
        st.info(f"1.5L 생수병 약 **{total_footprint/1.5:,.0f}개** 분량의 물입니다!", icon="💧")
        
        st.write("---")
        st.write("**상세 기록**")
        st.dataframe(records_df[["항목", "수량", "물 발자국 (L)"]].style.format({"물 발자국 (L)": "{:,.0f} L"}))
        
        st.write("**카테고리별 분석**")
        category_summary = records_df.groupby("카테고리")["물 발자국 (L)"].sum().sort_values(ascending=False)
        st.bar_chart(category_summary)