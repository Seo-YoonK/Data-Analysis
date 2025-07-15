import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# 데이터 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 원본 데이터 출력
st.subheader("📄 원본 데이터")
st.dataframe(df)

# 필요한 열만 추출: '2025년05월_계_'로 시작하는 열
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
region_column = df.columns[0]  # 첫 번째 열이 '행정구역(시군구)별'일 가능성 큼

# 연령 숫자만 추출한 새 열 이름
new_age_columns = [col.replace("2025년05월_계_", "") for col in age_columns]

# 총인구수 열 추출
total_pop_column = "2025년05월_계_총인구수"
df['총인구수'] = df[total_pop_column]

# 연령별 인구 데이터만 별도로 추출
age_df = df[[region_column, total_pop_column] + age_columns].copy()
age_df.columns = [region_column, "총인구수"] + new_age_columns

# 총인구수 기준 상위 5개 지역 선택
top5 = age_df.sort_values("총인구수", ascending=False).head(5)

# 연령별 인구 데이터를 재구성 (그래프용)
graph_df = top5.set_index(region_column).drop(columns="총인구수").T
graph_df.index.name = "연령"
graph_df = graph_df.astype(int)

# 선 그래프 출력
st.subheader("📊 상위 5개 지역의 연령별 인구 분포")
st.line_chart(graph_df)

# 상위 5개 지역 데이터 출력
st.subheader("🏙️ 총인구수 기준 상위 5개 행정구역")
st.dataframe(top5[[region_column, "총인구수"]])
