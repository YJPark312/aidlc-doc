# Requirements Verification Questions

기존 요구사항 문서(`requirements/table-order-requirements.md`, `requirements/constraints.md`)를 분석한 결과, 아래 항목들에 대한 확인이 필요합니다.
각 질문의 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1
백엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) Java + Spring Boot
B) Node.js + Express/NestJS
C) Python + FastAPI/Django
D) Go + Gin/Echo
E) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 2
프론트엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) React (JavaScript/TypeScript)
B) Vue.js
C) Next.js (React 기반 풀스택)
D) Angular
E) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 3
데이터베이스로 어떤 것을 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) DynamoDB (AWS NoSQL)
D) MongoDB
E) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 4
배포 환경은 어떻게 계획하고 계십니까?

A) AWS (EC2, ECS, Lambda 등)
B) 로컬 개발 환경만 (Docker Compose 등)
C) Kubernetes (EKS, 자체 클러스터)
D) 서버리스 (AWS Lambda + API Gateway)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 5
메뉴 이미지 관리 방식은 어떻게 하시겠습니까? (요구사항에 이미지 URL 언급)

A) 외부 이미지 URL 직접 입력 (별도 업로드 없음)
B) S3 등 클라우드 스토리지에 업로드
C) 서버 로컬 파일 시스템에 업로드
D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 6
관리자 계정 관리 방식은 어떻게 하시겠습니까?

A) 사전 설정된 관리자 계정 (DB 시드 데이터)
B) 관리자 회원가입 기능 포함
C) 환경 변수로 초기 관리자 설정 후 관리자 페이지에서 추가
D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 7
동시 접속 규모는 어느 정도를 예상하십니까? (NFR 판단 기준)

A) 소규모 — 단일 매장, 테이블 10개 이하
B) 중규모 — 단일 매장, 테이블 10~50개
C) 대규모 — 다중 매장, 테이블 50개 이상
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 8: Security Extensions
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 9: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)
B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)
C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)
D) Other (please describe after [Answer]: tag below)

[Answer]: C
