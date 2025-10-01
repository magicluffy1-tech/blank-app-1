import streamlit as st
import pandas as pd

# --- 페이지 설정 ---
# 모든 Streamlit 앱의 시작은 st.set_page_config()로 시작합니다.
# 페이지 제목(page_title)과 아이콘(page_icon)을 설정합니다.
st.set_page_config(
    page_title="나의 물 발자국 계산기",
    page_icon="💧",
    layout="wide"
)

# --- 데이터베이스 ---
# 각 항목별 물 발자국 데이터를 딕셔너리 형태로 관리합니다.
# 출처에 따라 값은 다를 수 있으며, 교육용으로 대표적인 값을 사용했습니다.
# key: (표시될 이름, 단위), value: 단위당 물 발자국 (리터)
WATER_FOOTPRINT_DATA = {
    # 음식 (1개 또는 1kg 기준)
    "사과": (("사과 (1개, 약 150g)", "개"), 125),
    "바나나": (("바나나 (1개, 약 120g)", "개"), 100),
    "소고기": (("소고기 (100g)", "인분(100g)"), 1540),
    "돼지고기": (("돼지고기 (100g)", "인분(100g)"), 600),
    "닭고기": (("닭고기 (100g)", "인분(100g)"), 430),
    "계란": (("계란 (1개, 약 60g)", "개"), 200),
    "쌀밥": (("쌀밥 (1공기, 약 210g)", "공기"), 260),
    "빵": (("식빵 (1조각)", "조각"), 40),
    "라면": (("라면 (1개)", "개"), 550),

    # 음료 (1잔 또는 1L 기준)
    "물": (("마시는 물 (200ml)", "잔"), 0.2), # 직접 소비
    "우유": (("우유 (200ml)", "잔"), 200),
    "커피": (("커피 (1잔, 약 125ml 원두 기준)", "잔"), 140),
    "콜라": (("콜라 (1캔, 355ml)", "캔"), 75),

    # 생활 습관 (1회 기준)
    "샤워": (("샤워 (5분)", "회"), 60),
    "세수": (("세수 (물 틀어놓고)", "회"), 12),
    "양치": (("양치 (컵 사용 안 함)", "회"), 6),
    "설거지": (("설거지 (10분, 물 틀어놓고)", "회"), 120),
    "빨래": (("세탁기 사용", "회"), 150),
}


# --- 기능 분리: 계산 로직 ---
# 복잡한 로직은 별도의 함수로 만들어 재사용성과 가독성을 높입니다.
def calculate_footprint(user_inputs):
    """
    사용자 입력을 바탕으로 물 발자국 총량과 항목별 내역을 계산하는 함수
    """
    total_footprint = 0
    details = {}

    for key, (label_tuple, footprint_per_unit) in WATER_FOOTPRINT_DATA.items():
        label = label_tuple[0]
        quantity = user_inputs.get(label, 0)
        if quantity > 0:
            item_footprint = quantity * footprint_per_unit
            total_footprint += item_footprint
            details[label] = item_footprint

    return total_footprint, details


# --- 앱 제목 및 설명 ---
st.title("💧 나의 일주일 물 발자국 계산기")
st.markdown("우리가 먹고 쓰는 모든 것에는 '보이지 않는 물'이 숨어있어요.")
st.markdown("지난 일주일 동안의 생활을 돌아보며 나의 물 발자국을 계산해보고, 물의 소중함을 함께 느껴봐요!")
st.info("각 항목에 일주일 동안 소비한 **총 횟수**나 **개수**를 입력해주세요.", icon="💡")


# --- 사용자 입력 ---
# 화면을 st.columns를 활용하여 체계적으로 구성합니다.
user_inputs = {}
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🍚 음식")
    user_inputs[WATER_FOOTPRINT_DATA["사과"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["사과"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["바나나"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["바나나"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["소고기"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["소고기"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["돼지고기"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["돼지고기"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["닭고기"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["닭고기"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["계란"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["계란"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["쌀밥"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["쌀밥"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["빵"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["빵"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["라면"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["라면"][0][0], min_value=0, step=1)

with col2:
    st.header("🥤 음료")
    user_inputs[WATER_FOOTPRINT_DATA["물"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["물"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["우유"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["우유"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["커피"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["커피"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["콜라"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["콜라"][0][0], min_value=0, step=1)

with col3:
    st.header("🧼 생활 습관")
    user_inputs[WATER_FOOTPRINT_DATA["샤워"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["샤워"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["세수"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["세수"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["양치"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["양치"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["설거지"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["설거지"][0][0], min_value=0, step=1)
    user_inputs[WATER_FOOTPRINT_DATA["빨래"][0][0]] = st.number_input(label=WATER_FOOTPRINT_DATA["빨래"][0][0], min_value=0, step=1)


# 논리적인 코드 블록 사이에 한 줄의 공백을 넣어 시각적으로 구분합니다.
st.write("---")


# --- 계산 실행 및 결과 표시 ---
# 사용자가 버튼을 클릭했을 때만 계산 로직이 실행되도록 하여 불필요한 재실행을 막습니다.
if st.button("💧 나의 일주일 물 발자국 계산하기!"):
    # 예외 처리: 입력값이 없는 경우를 대비합니다.
    if not any(user_inputs.values()):
        st.warning("항목을 하나 이상 입력해주세요!")
    else:
        # 함수를 호출하여 계산을 수행합니다.
        total_footprint, details = calculate_footprint(user_inputs)

        # 계산 결과를 시각적으로 보여줍니다.
        st.subheader("📊 나의 일주일 물 발자국 계산 결과")
        st.metric(
            label="총 물 사용량 (L)",
            value=f"{total_footprint:,.0f} L"
        )
        st.info(f"이것은 1.5L 생수병 약 **{total_footprint/1.5:,.0f}개**에 해당하는 엄청난 양의 물이에요!", icon="😮")

        # 논리적인 블록을 시각적으로 구분합니다.
        st.write("---")

        st.subheader("상세 분석: 어디에 물을 가장 많이 썼을까요?")

        # 상세 결과를 데이터프레임으로 변환하여 보여줍니다.
        # pandas를 사용하면 데이터를 다루고 시각화하기 편리합니다.
        details_df = pd.DataFrame(
            list(details.items()),
            columns=["항목", "물 사용량 (L)"]
        ).sort_values(by="물 사용량 (L)", ascending=False).set_index("항목")

        # 막대 그래프로 시각화하여 학생들이 직관적으로 이해하도록 돕습니다.
        st.bar_chart(details_df)

        with st.expander("자세한 사용량 보기"):
            st.dataframe(details_df.style.format("{:,.0f} L"))

        # 논리적인 블록을 시각적으로 구분합니다.
        st.write("---")

        # --- 추가 정보 및 실천 방안 ---
        st.subheader("🌍 물 발자국을 줄이기 위한 작은 실천")
        st.markdown("""
            * **육류 소비 줄이기:** 소고기 대신 닭고기를 선택하는 것만으로도 많은 물을 아낄 수 있어요.
            * **음식 남기지 않기:** 음식을 버리는 것은 그 음식을 만드는 데 들어간 모든 물을 버리는 것과 같아요.
            * **절수 습관 기르기:** 양치할 때 컵 사용하기, 샤워 시간 1분 줄이기 등 작은 습관이 큰 변화를 만들어요.
            * **물건 아껴 쓰기:** 옷이나 공책 한 권을 만드는 데도 많은 물이 필요해요. 물건을 아껴 쓰는 것도 물을 절약하는 방법이에요.
        """)