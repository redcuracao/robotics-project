# 두산 협동로봇(M0609) 기반 칵테일 제조 로봇 프로젝트

![Tumbnail](/bottail_monitoring/public/Tumbnail.PNG)
![Tumbnail](/bottail_monitoring/public/ui.png)

<br>

## 🗂️ 목차

### 1. [프로젝트 개요](#-프로젝트-개요)

### 2. [팀 구성 및 역할](#-팀-구성-및-역할)

### 3. [사용 기술](#-사용-기술)

### 4. [Flow Chart](#-Flow-Chart)

### 5. [System Architecture](#-System-Architecture)

### 6. [Node Architecture](#-Node-Architecture)

### 7. [시연 영상](#-시연-영상)

### 8. [평가 및 피드백](#-평가-및-피드백)

<br>

## 📃 프로젝트 개요

### 칵테일 제조 바텐더 로봇 (Bottail)

웹에서 칵테일을 주문하면 즉시 만들어드립니다!!
원하는 메뉴를 선택하면 알맞은 레시피 방식으로 칵테일을 만들어줍니다.

#### 📆 개발 기간 : 2025년 12월 08일 ~ 2025년 12월 19일

#### 📜 관련 문서 노션 링크: [노션링크](https://kaput-promise-bd0.notion.site/1-F3-2c3f99f5d39380a5a056cf10c2b780c3?source=copy_link)

<br>

## 🧑‍🤝‍🧑 팀 구성 및 역할

|  조원  | 역할 |                             담당 업무                              |
| :----: | :--: | :----------------------------------------------------------------: |
| 김갑민 | 팀장 | 모니터링 UI 제작, UI-로봇 동작 기능 연결 통합, 로봇 이동 모션 제작 |
| 권수인 | 팀원 |                              PPT 제작                              |
| 백수안 | 팀원 |                       동작 노드 제작 및 통합                       |
| 이용우 | 팀원 |               shaking, stirring 모션 제작, PPT 제작                |

<br>

## 🕹️ 사용 기술

|     항목      |            내용            |
| :-----------: | :------------------------: |
|   운영 체제   |      Ubuntu 22.04 LTS      |
|      ROS      |        ROS 2 Humble        |
| 협동로봇 모델 |        Doosan m0609        |
|   개발 언어   | Python 3.10.12, Javascript |
|  프레임워크   |     ROS2 bridge, Vuejs     |
|      DB       |          firebase          |

<br>

## 🎞️ Flow Chart

![flow-chart](/bottail_monitoring/public/flow_chart.png)

<br>

## 📝 System Architecture

![SA](/bottail_monitoring/public/system_architecture.png)

<br>

## 🔖 Node Architecture

![SA](/bottail_monitoring/public/system_architecture.png)

<br>

## 🎥 시연 영상

[![영상 제목](/bottail_monitoring/public/Tumbnail.PNG)](https://youtu.be/DPY0LymRcAk?si=c5qC5KyUh3cyv2LY)

<br>

## 🛠️ 평가 및 피드백

### 완성도 평가

- 쉐이킹 모션 및 자동화, UI, 로봇 제어, 복구 모드 등 모든 기능 구현

### 추후 개선점 및 보완할 점

- 음료 디스펜서 자동화 필요
- 쉐이커 홀더의 안정성 저하로 개선 필요
- 메뉴 다양화

### 우리 팀이 잘한 부분 / 아쉬운 점

- 모든 기능 구현 완료
- 실사용 가능한 수준의 UI 구성
- 그리퍼 및 시스템 한계로 동작의 완성도 저하

### 느낌 점 및 경험한 성과

- 협동 로봇 및 공간 좌표계에 대한 이해도 향상
