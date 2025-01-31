# What’s Up: AI 기반 영어 회화 챗봇 프로젝트

## 프로젝트 소개

# **What’s Up**
**"미드 프렌즈와 함께 친근하게 영어 회화를!"**  
What’s Up은 AI 기반 영어 학습 챗봇으로, 미드 *프렌즈*의 대사를 활용해 실생활 대화와 구어체를 친근하게 연습하며 영어 실력을 향상할 수 있도록 지원합니다.

- **주요 목표**: 자연스러운 영어 회화 환경 제공 및 사용자 맞춤형 학습 경험 구현.
- **핵심 가치**: 미드 *프렌즈*와 같은 친근한 대화를 통해 학습 동기를 부여하며, 실생활에서 바로 활용할 수 있는 영어 표현을 익히도록 지원.

---

## 프로젝트 핵심 목표

1. **실생활 영어 회화 학습 환경 제공**  
   - 미드 대사를 기반으로 한 다양한 대화 시나리오 제공.
   - 최신 슬랭 및 구어체를 반영한 학습 콘텐츠 구성.

2. **개인 맞춤형 학습 경험 구현**  
   - 사용자 프로필 기반 대화 스타일 커스터마이징.
   - 발음 교정 및 음성 피드백을 통한 스피킹 향상.

3. **몰입형 학습 경험 제공**  
   - Text-to-Speech(TTS) 기술로 드라마 캐릭터의 목소리를 구현해 재미와 몰입감 강화.

---

### 주요 기능
1. **개인 맞춤형 대화**: 회원가입 시 입력된 정보를 기반으로 한 맞춤형 응답 제공.
2. **음성 및 텍스트 입력 지원**: Speech-to-Text(STT)와 Text-to-Speech(TTS) 기능 지원.
3. **상황별 대화 시나리오**: 카페, 여행, 비즈니스 등 특정 상황을 선택하여 대화 연습 가능.
4. **발음 교정 기능**: 음성 입력을 분석하여 정확한 피드백 제공.
5. **미드 기반 학습**: 드라마 '프렌즈'의 대사를 바탕으로 한 자연스러운 대화 예제 제공.

---

## 프로젝트 정보

- **프로젝트 명**: What’s Up
- **개발 기간**: 2024.12.30 ~ 2025.01.31
- **팀명**: Team What’s Up
- **깃허브 주소**: [Team What’s Up GitHub](https://github.com/TeamWhatssUp/Whats_Up)

---

## 주요 기능

### 🍁 **개인 맞춤형 대화**
- 캐릭터 선택창에서 대화하고 싶은 선호 스타일을 입력받아 맞춤형 대화 제공.
- 구현 기술: 

### 🍁 **발음 교정 기능**
- 음성 입력(STT)을 분석해 발음 정확도 피드백 제공.
- 구현 기술: Speech-to-Text 모듈, Pronunciation Feedback 알고리즘.

### 🍁 **미드 기반 학습**
- *프렌즈* 대사를 크롤링하여 드라마 속 친숙한 표현 학습.
- 구현 기술: 웹 크롤링, 텍스트 정규화.

### 🍁 **채팅 저장 기능**
- 사용자와 챗봇의 대화를 저장해 학습 이력 추적 및 복습 가능.
- 구현 기술: 
---

## 서비스 아키텍처

### 1. 사용자 등록 및 로그인
- **Frontend**: 회원가입 및 로그인 UI 제공.
- **Backend**: 사용자 인증 및 데이터 저장.
- **Database**: 사용자 정보 저장.

### 2. 대화 생성
- **Frontend**: 질문 입력 UI.
- **Backend**: OpenAI API와 연동하여 응답 생성.
- **Enrichment Module**: 드라마 대본, 슬랭 데이터 활용.

### 3. 발음 교정
- **Speech-to-Text Module**: 음성 입력을 텍스트로 변환.
- **Pronunciation Feedback Engine**: 분석 후 피드백 제공.

### 4. 상황별 대화
- **Scenario Selector UI**: 상황 선택 옵션 제공.
- **Scenario Management Module**: 시나리오 생성 및 제공.

---

## 기술 스택

### 프론트엔드
- HTML5, CSS3, JavaScript
- Bootstrap5, Axios

### 백엔드
- Python, Django, Django REST Framework
- OpenAI API

### 데이터베이스
- SQLite

### 협업 및 배포
- **버전관리**: GitHub
- **협업도구**: Notion, Jira, Slack

---

## 프로젝트 와이어프레임

#### 로그인 페이지
![로그인 페이지 와이어프레임](django_project\static/images/wireframe_loginpage.jpg)

#### 챗봇 페이지
![챗봇 페이지 와이어프레임](django_project\static/images/wireframe_chatbotpage.jpg)

---

## ERD 설계

![ERD 이미지](django_project\static/images/ERD.png)

---

# 트러블슈팅


---

## 🧑‍💻 김동찬

### 🔒 비밀번호 관련 Issue
1. **문제**: 
   - 비밀번호가 평문으로 저장되어 로그인 실패.
   - 비밀번호 변경 시 성공과 실패 상태 구분 불가.
2. **해결**:
   - 비밀번호 해싱 로직 추가.
   - HTTP 상태 코드와 JSON 응답 추가.
3. **결과**:
   - 비밀번호가 안전하게 저장되고 로그인 및 변경 기능 정상 작동.

---

## 🧑‍💻 서승화

### 🔒 STT 중복 메시지 출력 Issue
1. **문제**: 
   - STT 사용 시 동일 메시지가 두 번 출력.
2. **해결**:
   - `sendMessage` 함수에 `isSTT` 매개변수 추가.
   - STT 사용 시 중복 출력 방지 조건 적용.
3. **결과**:
   - STT 입력 메시지 중복 출력 문제 해결.

---

## 🧑‍💻 정재석

### 🔒 채팅 기록 저장 Issue
1. **문제**: 
   - 사용자 ID가 서버에 전달되지 않아 대화 저장 실패.
2. **해결**:
   - 클라이언트에서 사용자 ID를 포함한 데이터 전송.
   - 서버에서 사용자 ID 기반으로 대화 저장.
3. **결과**:
   - 사용자 ID와 함께 대화 기록 정상 저장.

---

## 🧑‍💻 오태우

### 🔒 사용자 맞춤형 기능 Issue
1. **문제**:
   - 세션 기반 데이터 저장 방식으로 인해 세션 만료 시 데이터 손실.
   - 저장 버튼 클릭 시 필드 불일치 오류.
2. **해결**:
   - 데이터베이스 모델로 영구 저장 방식 전환.
   - 필드 네이밍 수정 및 JSON 데이터 파싱 로직 추가.
3. **결과**:
   - 사용자 맞춤형 데이터 영구 저장 가능.
   - 필드 불일치 오류 해결 및 저장 기능 정상 작동.


---

## 역할 분담 및 협업 방식
- 역할 분담 상세 내용은
[Notion 링크](https://teamsparta.notion.site/3b0efb5bc0e9441aa31c360702eb2298?v=b21c5abffe024bf6aa6b74447fcad0ee&pvs=4)에서 확인 가능합니다




---
## API 명세서

- API 명세서 상세 내용은 [Notion 링크](https://www.notion.so/c8e0d883de1d49b0ac4958f5611ded22?pvs=21)에서 확인 가능합니다.
---

## 성과 및 회고 