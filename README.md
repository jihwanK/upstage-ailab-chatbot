[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/yoHXt_g5)
# 프로젝트 이름

푸와 친구들의 고민상담  

<br>

## 프로젝트 소개
<예시 1>
- 이 프로젝트는 증권 배당 데이터와 관련된 정보를 효율적으로 관리하고, 관련 세법에 대한 질문과 답변을 제공하는 QA(Question-Answering) 엔진을 구축하는 것입니다.
- 사용자는 이 엔진을 통해 특정 기업의 배당 정보나 세법 관련 질문에 대한 답변을 신속하게 얻을 수 있습니다.
<br>

<예시 2>
- 이 프로젝트는 유명 인물인 유재석의 페르소나를 바탕으로 한 Chatbot을 개발하는 것입니다.
- 이 Chatbot은 유재석의 말투, 스타일 등 유재석이 나온 프로그램 텍스트 대화를 반영하여 사용자와 자연스러운 대화를 나누도록 설계됩니다. 
<br>

## 팀원 구성

<div align="center">

| **김지환** | **김서현** | **최정은** | **김민수** | **박주연** |
| :------: |  :------: | :------: | :------: | :------: |
|[<img src="https://avatars.githubusercontent.com/u/17960812?v=4" height=150 width=150> <br/> @jihwanK](https://github.com/jihwanK) |[<img src="https://avatars.githubusercontent.com/u/177704202?v=4" height=150 width=150> <br/> @tjgusKim](https://github.com/tjgusKim) |[<img src="https://avatars.githubusercontent.com/u/177805026?v=4" height=150 width=150> <br/> @Insight7321](https://github.com/Insight7321) |[<img src="https://avatars.githubusercontent.com/u/175805884?v=4" height=150 width=150> <br/> @GoldDuck0108](https://github.com/GoldDuck0108) |[<img src="https://avatars.githubusercontent.com/u/40532035?v=4" height=150 width=150> <br/> @pbcs0321](https://github.com/pbcs0321) |
</div>

<br>

## 1. 개발 환경

- 주 언어 : Python
- 버전 및 이슈관리 : Git
- 협업 툴 : Slack, Notion

<br>

## 2. 채택한 개발 기술과 브랜치 전략
<예시>

### Pandas, NumPy

- Pandas
  - 기업의 배당 데이터를 Pandas DataFrame으로 불러온 후, 각 기업의 배당 수익률을 계산하고, 연도별로 그룹화하여 평균 배당 수익률을 계산합니다.
  - 필터링 조건을 적용하여 특정 기업의 배당 데이터를 분석하거나, 원하는 형태로 데이터를 변형할 수 있습니다.  

- Numpy
  - 벡터화 연산을 사용하여, 3000여개 데이터를 효율적으로 처리합니다.

### Beautifulsoup, Selenium

- Beautifulsoup
  - 네이버 증권 페이지에서 배당률, 주가 등의 정보를 포함한 HTML 테이블에서 데이터를 추출합니다.

- Selenium
  - 웹 페이지에서 동적 콘텐츠를 로드합니다.
  - 특정 종목의 배당 데이터를 얻기 위해 종목 검색 후, 관련 페이지로 이동해야 할 때, 이 과정을 자동화합니다. 

### 브랜치전략 
    
- 브랜치 전략
  - Git-flow 전략을 기반으로 main, develop 브랜치와 feature 보조 브랜치를 운용했습니다.
  - main, develop, Feat 브랜치로 나누어 개발을 하였습니다.
    - **main** 브랜치는 배포 단계에서만 사용하는 브랜치입니다.
    - **develop** 브랜치는 개발 단계에서 git-flow의 master 역할을 하는 브랜치입니다.
    - **Feat** 브랜치는 기능 단위로 독립적인 개발 환경을 위하여 사용하고 merge 후 각 브랜치를 삭제해주었습니다.


<br>

## 3. 프로젝트 구조
```
├── README.md
├── .gitignore
└── src
     ├── App.py
     ├── index.py
     ├── api
     │     └── GoogleAPI.jsx
     └── styles
           └── Globalstyled.jsx
...

```

<br>

## 4. 역할 분담

### 팀원 1
- **역할**
    - 프로젝트를 진행하며 맡은 역할 작성
- **기능**
    - 프로젝트를 진행하며 개발한 기능 작성
<br>

### 팀원 2
- **역할**
    - 프로젝트를 진행하며 맡은 역할 작성
- **기능**
    - 프로젝트를 진행하며 개발한 기능 작성
<br>

### 팀원 3
- **역할**
    - 프로젝트를 진행하며 맡은 역할 작성
- **기능**
    - 프로젝트를 진행하며 개발한 기능 작성
<br>

## 5. 개발 기간 및 작업 관리

### 개발 기간
- 전체 개발 기간 : 2024-08-12 ~ 2024-08-19
- 기능 구현 : 2024-08-00 ~ 2024-08-00
- 그외 기간 작성
  
<br>

### 작업 관리
<예시>

- 아래와 같은 오류가 발생했습니다.

```python
TypeError: FAISS.__init__() got an unexpected keyword argument 'allow_dangerous_deserialization'
```

### 설명

- langchain v0.1.0에서는 실행되지 않습니다


### 해결

- 명령 프롬프트(또는 터미널)에서 다음 명령을 실행해 langchain을 최신버전으로 업그레이드합니다.

```python
 pip install --upgrade langchain
```



<br>

## 5. 프로젝트 후기

### 팀원 1
프로젝트 후기 작성

### 팀원 2
프로젝트 후기 작성
<br>


