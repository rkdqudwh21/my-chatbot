# 🍽️ 감정 기반 음식 추천 챗봇

## 📌 소개
사용자의 감정 상태(스트레스, 우울, 피곤, 기분 좋음 등)를 기반으로
상황에 맞는 음식을 추천해주는 챗봇입니다.

단순 메뉴 추천이 아니라, 감정에 따라 추천 방향을 다르게 설정하여
보다 자연스러운 사용자 경험을 제공하도록 구현했습니다.

---

## 🚀 주요 기능

- 감정 키워드 기반 사용자 상태 분류
- 감정별 음식 추천 로직 적용
- 2~3개의 메뉴와 추천 이유 제공
- Streamlit 기반 채팅형 인터페이스

---

## 🛠️ 사용 기술

- Python
- Streamlit
- LangChain
- OpenAI API

---

## ⚙️ 사전 준비물

- Python 3.14 이상
- OpenAI API Key
- git, pip 사용 가능 환경

---

## 📦 설치 방법

### 프로젝트 클론

```bash
git clone https://github.com/rkdqudwh21/my-chatbot.git
cd my-chatbot
가상환경 생성 및 활성화 (Windows)
python -m venv .venv
.venv\Scripts\activate
필요한 패키지 설치
pip install -r requirements.txt
🔑 API 키 설정

.streamlit/secrets.toml 파일을 생성한 후 아래 내용을 추가합니다.

OPENAI_API_KEY = "여기에_API_KEY_입력"
▶️ 실행 방법
streamlit run app.py
📂 프로젝트 구조
app/
 └─ pages/
    ├─ index_page.py
    ├─ login_page.py
    └─ chat_page.py
app.py
requirements.txt
README.md
⚡ 동작 흐름

사용자 입력 → 감정 키워드 분류 → 감정별 프롬프트 적용 → AI 응답 생성

💡 예시 질문
오늘 너무 스트레스 받아
기분이 좀 우울해
너무 피곤해서 아무것도 하기 싫어
오늘 기분 좋은데 뭐 먹지?
🎯 구현 포인트
감정 상태에 따라 음식 추천 기준을 다르게 설정
특정 음식 유형에 치우치지 않도록 다양성 확보
사용자 선택을 돕기 위해 추천 개수를 제한 (2~3개)
