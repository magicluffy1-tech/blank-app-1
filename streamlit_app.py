import streamlit as st
import pandas as pd
import json

# --- 1. 페이지 및 기본 설정 ---
st.set_page_config(
    page_title="물 발자국 수행평가 도구",
    page_icon="📚",
    layout="wide"
)

# --- 2. 데이터베이스 ---
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
        "고구마 (1개)": 100, "밤 (100g)": 250, "배 (1개)": 150,
    },
    "🍫 간식 & 가공식품": {
        "초콜릿 (100g)": 1700, "감자칩 (작은 봉지)": 185, "견과류(아몬드) (한 줌)": 82, "떡볶이 (1인분)": 400,
        "호두 (한 줌)": 270, "피자 (한 판)": 1200, "설탕 (100g)": 178, "아이스크림 (1개)": 150,
    },
    "🥤 음료": {
        "커피 (1잔)": 132, "차(Tea) (1잔)": 27, "탄산음료(콜라) (1캔)": 75, "마시는 물 (1잔, 250ml)": 0.25,
    },
    "👕 의류 & 생활용품": {
        "면 티셔츠 (1장)": 2700, "청바지 (1벌)": 8000, "운동화 (1켤레)": 8000,
    },
    "🏫 학용품 및 취미": {
        "종이 (A4 1장)": 10, "책 (200p)": 250, "지우개 (1개)": 20, "물감 (1개)": 100, "음반(CD 1장)": 500,
    },
    "💡 디지털 생활": {
        "스마트폰 (1대 생산)": 12000, "인터넷 검색 (1회)": 0.3, "데이터 전송 (1GB)": 7,
        "동영상 스트리밍 (1시간)": 2, "온라인 게임 (1시간)": 10, "웹툰 보기 (10분)": 0.5, "음악 스트리밍 (1시간)": 1,
    },
    "🚗 교통 및 기타 일상": {
        "버스 (1km/인)": 3, "지하철 (1km/인)": 2, "반려동물 사료 (100g)": 200,
    },
    "🚿 생활 습관": {
        "샤워 (분당)": 12, "목욕 (1회)": 200, "양치(물 끄고) (1회)": 1, "양치(물 틀고) (1회)": 6,
        "손 씻기 (1회)": 3, "설거지(기계) (1회)": 15, "설거지(손) (분당)": 8, "세탁기 (1회)": 150,
        "화장실(변기) (1회)": 6, "샴푸 (1회)": 5,
    }
}

# --- 3. 상태 관리 (Session State) ---
if 'records' not in st.session_state:
    st.session_state.records = {}
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'final_reflection' not in st.session_state:
    st.session_state.final_reflection = ""

# --- 4. 기능 함수 ---
def add_record(date, category, item, quantity):
    date_str = str(date)
    if date_str not in st.session_state.records:
        st.session_state.records[date_str] = {"journal": "", "calculations": []}
    
    footprint = CATEGORIZED_DATA[category][item] * quantity
    st.session_state.records[date_str]['calculations'].append({
        "카테고리": category, "항목": item, "수량": quantity, "물 발자국 (L)": footprint
    })
    st.sidebar.success(f"'{item}' {quantity}개 추가 완료!")

def clear_day_records(date):
    date_str = str(date)
    if date_str in st.session_state.records:
        st.session_state.records[date_str] = {"journal": "", "calculations": []}
        st.sidebar.warning(f"{date_str}의 기록이 삭제되었습니다.")

# --- 5. 사이드바 UI ---
st.sidebar.header("📝 기록 관리")
selected_date = st.sidebar.date_input("기록할 날짜를 선택하세요")
st.sidebar.subheader("💧 항목 추가하기")
category_list = list(CATEGORIZED_DATA.keys())
selected_category = st.sidebar.selectbox("1. 카테고리", category_list, key="sb_category")
item_list = list(CATEGORIZED_DATA[selected_category].keys())
selected_item = st.sidebar.selectbox("2. 세부 항목", item_list, key="sb_item")
quantity = st.sidebar.number_input("3. 수량 (개수/횟수/분/km 등)", min_value=1, step=1, key="sb_quantity")
st.sidebar.button("리스트에 추가", on_click=add_record, args=(selected_date, selected_category, selected_item, quantity))
st.sidebar.button(f"{selected_date} 기록 초기화", on_click=clear_day_records, args=(selected_date,))
st.sidebar.write("---")
st.sidebar.header("💾 데이터 저장/불러오기")
records_json = json.dumps(st.session_state.records, indent=4, ensure_ascii=False)
st.sidebar.download_button(
    label="📈 기록 저장하기",
    data=records_json,
    file_name="my_water_footprint.json",
    mime="application/json"
)
uploaded_file = st.sidebar.file_uploader("📈 기록 불러오기", type="json")
if uploaded_file is not None:
    try:
        st.session_state.records = json.load(uploaded_file)
        st.sidebar.success("데이터를 성공적으로 불러왔습니다!")
    except Exception as e:
        st.sidebar.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

# --- 6. 메인 화면 (탭 구조) ---
tab1, tab2, tab3 = st.tabs(["✍️ 물 발자국 일기", "📚 학습 자료", "📑 최종 보고서"])

with tab1:
    st.header(f"🗓️ {selected_date}의 물 발자국 일기")
    date_str = str(selected_date)
    if date_str not in st.session_state.records:
        st.session_state.records[date_str] = {"journal": "", "calculations": []}
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.subheader("📓 나의 하루 일기")
        journal_text = st.text_area(
            "오늘의 활동을 자세히 기록하고, 빠진 항목이 없는지 점검해보세요.",
            height=200,
            value=st.session_state.records[date_str].get("journal", ""),
            key=f"journal_{date_str}"
        )
        st.session_state.records[date_str]["journal"] = journal_text
    with col2:
        st.subheader("🧮 계산 결과")
        calculations = st.session_state.records[date_str].get("calculations", [])
        if not calculations:
            st.info("왼쪽 사이드바에서 오늘의 활동을 추가해주세요.")
        else:
            records_df = pd.DataFrame(calculations)
            total_footprint = records_df["물 발자국 (L)"].sum()
            st.metric(label=f"{date_str}의 총 물 발자국", value=f"{total_footprint:,.0f} L")
            st.dataframe(records_df[["항목", "수량", "물 발자국 (L)"]].style.format({"물 발자국 (L)": "{:,.0f} L"}))

with tab2:
    st.header("🌍 물 발자국, 제대로 알아보기")
    with st.expander("💧 물 발자국이란?", expanded=True):
        st.write("""
        우리가 매일 먹고, 입고, 사용하는 모든 것을 만들고 소비하는 과정에서 사용되는 **보이지 않는 물의 총량**을 의미해요.
        예를 들어, 커피 한 잔의 물 발자국에는 원두를 재배하고, 가공하고, 우리에게 오기까지의 모든 과정에 들어간 물이 포함됩니다.
        """)
        st.image("https://waterfootprint.org/media/downloads/Infographic_footprint_components_1.png", caption="물 발자국의 세 가지 종류 (출처: Water Footprint Network)")
    with st.expander("🧐 알고 계셨나요?"):
        st.info("**소고기 100g**의 물 발자국(1,540L)은 **5분짜리 샤워를 25번** 넘게 할 수 있는 양의 물과 같아요!")
        st.info("**면 티셔츠 한 장**에는 **한 사람이 3년 동안 마실 수 있는 물**에 해당하는 2,700L의 물 발자국이 숨어있어요.")
    with st.expander("👍 물 발자국 줄이기 실천 팁"):
        st.markdown("- **육류 소비 줄이기**: 일주일에 하루는 채식을 실천해보세요.\n- **음식 남기지 않기**: 버려지는 음식에는 그 음식을 만드는 데 들어간 모든 물이 함께 버려져요.\n- **절수 습관**: 양치컵 사용, 샤워 시간 줄이기 등 작은 습관이 큰 변화를 만들어요.")

with tab3:
    st.header("📑 수행평가 최종 보고서")
    st.session_state.student_name = st.text_input("이름을 입력하세요.", value=st.session_state.student_name)
    if not st.session_state.records:
        st.warning("먼저 '물 발자국 일기' 탭에서 데이터를 기록해주세요.")
    else:
        st.write("---")
        st.subheader(f"**{st.session_state.student_name} 학생의 물 발자국 탐구 보고서**")
        all_calculations = []
        for date, data in sorted(st.session_state.records.items()):
            for calc in data['calculations']:
                all_calculations.append({"날짜": date, **calc})
        if not all_calculations:
            st.error("계산 기록이 없습니다. 하나 이상의 활동을 추가해주세요.")
        else:
            full_df = pd.DataFrame(all_calculations)
            total_footprint = full_df["물 발자국 (L)"].sum()
            st.metric("💧 탐구 기간 총 물 발자국", f"{total_footprint:,.0f} L")
            st.subheader("📊 카테고리별 종합 분석")
            category_summary = full_df.groupby("카테고리")["물 발자국 (L)"].sum().sort_values(ascending=False)
            st.bar_chart(category_summary)
            st.subheader("🗓️ 일자별 기록 및 일기")
            for date, data in sorted(st.session_state.records.items()):
                with st.expander(f"**{date}**"):
                    st.write("**📝 일기 내용**")
                    st.info(data.get("journal", "작성된 일기가 없습니다."))
                    st.write("**💧 계산 목록**")
                    if data['calculations']:
                        day_df = pd.DataFrame(data['calculations'])
                        st.dataframe(day_df[["항목", "수량", "물 발자국 (L)"]])
                    else:
                        st.write("계산 기록이 없습니다.")
            st.write("---")
            st.subheader("✍️ 느낀 점 및 앞으로의 다짐")
            st.session_state.final_reflection = st.text_area(
                "이번 활동을 통해 무엇을 느끼고 배웠으며, 앞으로 물 발자국을 줄이기 위해 어떻게 노력할 것인지 자유롭게 작성해보세요.",
                height=250,
                value=st.session_state.final_reflection
            )
            st.success("보고서가 완성되었습니다! 이 화면을 인쇄하거나 PDF로 저장하여 제출하세요. (Ctrl+P 또는 Cmd+P)")
