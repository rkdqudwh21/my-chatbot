#app/pages/index_page.py
import streamlit as st

st.title("🍽감정 기반 메뉴 추천 챗봇")

#전체 요소를 가운데  정렬. 비율 1:10:1
_, main, _=st.columns([1,10,1])

with main:
    #이미지를 가운데 정렬. 비율 1:1:1
    _, image, _=st.columns([1,1,1])

with image:
    st.image("static/logo.svg",width=150)

    #로고 아래 설명문구 작성
    st.markdown(
        """
        ### 오늘 기분에 맞는 음식을 추천드립니다.
        - 스트레스,피곤함,우울함,기분 좋은 날까지 상황에 맞게 메뉴를 추천받아 보세요. 
        """
    )