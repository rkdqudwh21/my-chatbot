#app/pages/chat_page.py

import os
import streamlit as st

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda

_api_key=st.secrets.get("OPENAI_API_KEY","")
if _api_key:
    os.environ.setdefault("OPENAI_API_KEY", _api_key)
else:
    st.warning("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

st.subheader("💭AI 챗봇")

# 1)세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages=[]
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory={}

SESSION_ID="chapter6"

def get_memory(session_id):
    session_key=session_id or SESSION_ID
    chat_memories=st.session_state.chat_memory
    if session_key not in chat_memories:
        chat_memories[session_key]=InMemoryChatMessageHistory()
    return chat_memories[session_key]

# 2) 범용 답변용 구성요소 정의와 체인 생성
prompt=ChatPromptTemplate(
    [
        (
            "system",
            """
            너는 친근한 음식 추천 도우미야

            사용자의 감정 상태(스트레스,우울함,피곤함 등)를 파악하고
            한국인이 일상적으로 먹는 음식 위주로 추천해라.

            사용자의 감정 상태에 따라 추천 방향을 다르게 해야 한다.

            - 스트레스: 매운 음식, 자극적인 음식
            - 우울: 달달하거나 부드러운 음식
            - 피곤: 간단하거니 부담없는 음식
            - 기분 좋음: 즐길 수 있는 음식

            반드시 아래의 형식을 지켜라
            1. 2~3개의 메뉴만 추천 
            2. 특정 음식 종류(한식)에 치우치지 말고, 한식, 양식, 패스트푸드 등 다양한 메뉴를 섞어서 추천할 것 
            3.너무 가벼운 음식(요거트,샐러드)만 반복하지 말 것
            4.상황에 맞게 다양하게 추천할 것
            5.각 메뉴마다 이유를 설명할 것

            답변은 너무 길지 않게,자연스럽고 부담없는 말투로 작성하라.
            """,
        ),
        MessagesPlaceholder("history"),
        ("human","{question}"),
    ]
)

model=ChatOpenAI(model="gpt-5-nano")
output_parser=StrOutputParser()

#범용 답변 체인 생성
chain=prompt|model|output_parser

general_chain=RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="question",
    history_messages_key="history",
)


router_keywords={
    "스트레스":["스트레스","짜증","열받","화남"],
    "우울":["우울","기분 안좋","슬퍼","다운"],
    "피곤":["피곤","지침","힘듦","귀찮"],
    "기쁨":["기분 좋","행복","신남"],
}

def classify_topic(question):
    for key, values in router_keywords.items():
        if any(keyword in question for keyword in values):
            return key
    return"기타"
    
def router_step(inputs):
    question=inputs["question"]
    topic=classify_topic(question)
    return {"question":question,"topic":topic}

router_chain=RunnableLambda(router_step)

def route(info):
    topic=info["topic"]
    question=info["question"]
    
    if topic == "스트레스":
        return general_chain.invoke(
            {"question":f"사용자는 스트레스를 받고 있다. 매운 음식이나 자극적인 음식 위주로 추천해줘. 질문:{question}"},
            config={"session_id":SESSION_ID},
        )
    
    if topic == "우울":
        return general_chain.invoke(
            {"question":f"사용자는 기분이 우울하다. 달달하거나 부드럽고 위로가 되는 음식을 추천해줘. 질문:{question}"},
            config={"session_id":SESSION_ID},
        )
    
    if topic =="피곤":
        return general_chain.invoke(
            {"question":f"사용자는 많이 피곤한 상태다. 기름지거나 자극적인 음식은 피하고, 간단하고 소화가 편한 따뜻한 음식 위주로 추천해줘. 질문:{question}"},
            config={"session_id":SESSION_ID}
        )
    
    if topic =="기쁨":
        return general_chain.invoke(
            {"question":f"사용자는 기분이 좋은 상태다. 평소보다 더 즐길 수 있는 음식이나 보상 느낌이 나는 메뉴 위주로 추천해줘. 질문:{question}"},
            config={"session_id":SESSION_ID}
        )
    
    
    return general_chain.invoke(
        {"question":info["question"]},
        config={"session_id":SESSION_ID},
    )

# 3) 최종 체인 구성
full_chain=(
    router_chain
    |RunnableLambda(route)
)

#4) 사용자 입력
prompt=st.chat_input("무엇을 도와드릴까요?")

#5) 들어온 값 저장
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.spinner("AI가 응답을 생성하는 중입니다..."):
        response=full_chain.invoke({"question":prompt})
    
    st.session_state.messages.append({"role":"assistant","content":response})

#6) 출력
for message in st.session_state.messages:
    speaker="user" if message["role"]== "user" else "assistant"

    with st.chat_message(speaker):
        st.markdown(message["content"])