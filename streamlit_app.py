import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="나의 물 발자국 계산기 (데일리)",
    page_icon="📆",
    layout="wide"
)

# --- 데이터베이스 ---
# 각 항목별 물 발자국 데이터 (이전과 동일)
WATER_FOOTPRINT_DATA = {
    "사과 (1개)": 125,
    "바나나 (1개)": 100,
    "소고기 (100g)": 1540,
    "돼지고기 (100g)": 600,
    "닭고기 (100g)": 430,
    "계란 (1개)": 200,
    "쌀밥 (1공기)": 260,
    "식빵 (1조각)": 40,
    "라면 (1개)": 550,
    "마시는 물 (1잔, 200ml)": 0.2,
    "우유 (1잔, 200ml)": 200,
    "커피 (1잔)": 140,
    "콜라 (1캔)": 75,
    "샤워 (5분)": 60,
    "세수 (1회)": 12,
    "양치 (1회, 컵 미사용)": 6,
    "설거지 (10분)": 120,
    "세탁기 (1회)": 150,
}

# --- 상태 관리 (Session State) ---
# 사용자의 입력 기록을 저장하기 위해 세션 상태를 사용합니다.
# 'history' 리스트가 없으면 새로 초기화합니다.
if 'history' not in st.session_state:
    st.session_state.history = []


# --- 기능 함수 ---
def add_record(date, item, quantity):
    """사용자 입력을 받아 계산하고 세션 상태에 기록을 추가하는 함수"""
    if quantity > 0:
        footprint = WATER_FOOTPRINT_DATA[item] * quantity
        # 날짜를 문자열로 변환하여 저장 (Pandas 호환성)
        st.session_state.history.append({
            "날짜": str(date),
            "항목": item,
            "수량": quantity,
            "물 발자국 (L)": footprint
        })
        st.sidebar.success(f"'{item}' {quantity}개 기록 완료!")

def clear_history():
    """모든 기록을 삭제하는 함수"""
    st.session_state.history = []


# --- 사이드바 (사용자 입력 영역) ---
st.sidebar.header("📝 오늘의 활동 기록하기")

# 날짜 선택
selected_date = st.sidebar.date_input("기록할 날짜를 선택하세요")

# 항목 선택
item_options = list(WATER_FOOTPRINT_DATA.keys())
selected_item = st.sidebar.selectbox("무엇을 하셨나요?", options=item_options)

# 수량 입력
quantity = st.sidebar.number_input("몇 번 또는 몇 개를 사용했나요?", min_value=0, step=1)

# 기록 추가 버튼
st.sidebar.button(
    "기록 추가하기",
    on_click=add_record,
    args=(selected_date, selected_item, quantity)
)

# 여백 추가
st.sidebar.write("---")

# 기록 초기화 버튼
if st.sidebar.button("모든 기록 초기화하기"):
    clear_history()
    st.sidebar.warning("모든 기록이 삭제되었습니다.")


# --- 메인 화면 (결과 표시 영역) ---
st.title("💧 나의 물 발자국 계산기")
st.markdown("매일의 작은 습관이 모여 나의 물 발자국이 됩니다. 꾸준히 기록하고 변화를 만들어보세요!")
st.info("왼쪽 사이드바에서 날짜를 선택하고 활동을 기록해주세요.", icon="👈")

# 기록이 없을 경우 안내 메시지 표시
if not st.session_state.history:
    st.success("아직 기록이 없어요. 첫 번째 물 발자국을 남겨보세요!")
else:
    # 기록 데이터를 Pandas DataFrame으로 변환
    history_df = pd.DataFrame(st.session_state.history)

    # --- 요약 정보 표시 ---
    st.subheader("📊 나의 물 발자국 요약")
    
    # 선택된 날짜의 데이터 필터링
    daily_df = history_df[history_df['날짜'] == str(selected_date)]
    daily_total = daily_df['물 발자국 (L)'].sum()
    
    # 전체 누적 데이터 계산
    cumulative_total = history_df['물 발자국 (L)'].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"💧 {selected_date} 사용량", f"{daily_total:,.0f} L")
    with col2:
        st.metric("🌍 총 누적 사용량", f"{cumulative_total:,.0f} L")
    
    st.write("---")

    # --- 상세 기록 표시 ---
    st.subheader(f"🗓️ {selected_date} 상세 기록")
    if daily_df.empty:
        st.write("선택한 날짜에는 기록이 없습니다.")
    else:
        # 인덱스를 1부터 시작하도록 설정
        daily_df_display = daily_df.copy()
        daily_df_display.index = range(1, len(daily_df_display) + 1)
        st.dataframe(daily_df_display)

    st.write("---")

    # --- 전체 누적 분석 ---
    st.subheader("📈 전체 누적 사용량 분석")
    
    # 항목별로 물 발자국 합산 및 정렬
    summary_df = history_df.groupby("항목")["물 발자국 (L)"].sum().sort_values(ascending=False)
    
    st.bar_chart(summary_df)
    
    with st.expander("항목별 상세 데이터 보기"):
        st.dataframe(summary_df)