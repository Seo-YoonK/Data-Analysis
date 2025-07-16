import streamlit as st
import pandas as pd

st.title("2025년 5월 연령별 인구 현황 분석")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='euc-kr')

        st.subheader("📄 원본 데이터")
        st.dataframe(df)

        # 연령별 인구 열 추출
        age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
        region_column = df.columns[0]
        total_pop_column = "2025년05월_계_총인구수"

        # 중복 방지를 위해 총인구수 컬럼이 있다면 제거
        if "총인구수" in df.columns:
            df = df.drop(columns=["총인구수"])

        # '총인구수' 열 생성
        df["총인구수"] = df[total_pop_column]

        # 연령 숫자만 남기기
        new_age_columns = [col.replace("2025년05월_계_", "") for col in age_columns]

        # 필요한 열만 추출
        age_df = df[[region_column, total_pop_column] + age_columns].copy()
        age_df.columns = [region_column, "총인구수"] + new_age_columns

        # 상위 5개 행정구역
        top5 = age_df.sort_values("총인구수", ascending=False).head(5)

        # 선 그래프용 데이터 재구성
        graph_df = top5.set_index(region_column).drop(columns="총인구수").T
        graph_df.index.name = "연령"
        graph_df = graph_df.astype(int)

        # 시각화
        st.subheader("📊 상위 5개 지역의 연령별 인구 분포")
        st.line_chart(graph_df)

        st.subheader("🏙️ 총인구수 기준 상위 5개 행정구역")
        st.dataframe(top5[[region_column, "총인구수"]])

    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {e}")

else:
    st.info("📎 왼쪽 사이드바에서 CSV 파일을 업로드해주세요.")
