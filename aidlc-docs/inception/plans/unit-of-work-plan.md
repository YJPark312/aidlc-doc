# Unit of Work Plan

## 계획

- [x] 유닛 정의 및 책임 범위 결정
- [x] 유닛 간 의존성 매트릭스 생성
- [x] 요구사항-유닛 매핑 생성
- [x] 코드 조직 전략 문서화
- [x] 유닛 경계 및 의존성 검증

---

## 유닛 분해 관련 질문

각 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

## Question 1
시스템을 어떤 단위로 분해하시겠습니까?

A) 3개 유닛 — Backend(FastAPI), Frontend(Vue.js), Infrastructure(Docker Compose/MySQL)
B) 2개 유닛 — Backend+Infrastructure를 하나로, Frontend를 하나로
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 2
유닛 간 개발 순서를 어떻게 하시겠습니까?

A) Backend 먼저 → Frontend → Infrastructure 순서 (API 완성 후 UI 개발)
B) Infrastructure 먼저 → Backend → Frontend 순서 (환경 구축 후 개발)
C) Backend + Frontend 동시 개발 (Mock API 활용)
D) Other (please describe after [Answer]: tag below)

[Answer]: A
