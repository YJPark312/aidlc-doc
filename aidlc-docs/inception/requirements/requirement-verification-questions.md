# Requirements Verification Questions

기존 요구사항 문서(table-order-requirements.md, constraints.md)를 분석했습니다.
기능 요구사항은 상세하게 정의되어 있으나, 기술적 결정과 비기능 요구사항에 대해 확인이 필요합니다.

각 질문의 [Answer]: 태그 뒤에 선택한 알파벳을 입력해주세요.

---

## Question 1
백엔드 프레임워크로 어떤 기술을 사용하시겠습니까?

A) Node.js + Express
B) Node.js + NestJS
C) Python + FastAPI
D) Java + Spring Boot
E) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 2
프론트엔드 프레임워크로 어떤 기술을 사용하시겠습니까?

A) React (Vite)
B) Next.js
C) Vue.js
D) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 3
데이터베이스로 어떤 기술을 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) SQLite (개발/MVP용 경량 DB)
D) DynamoDB (AWS NoSQL)
E) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 4
프로젝트 아키텍처 구조를 어떻게 구성하시겠습니까?

A) 모노레포 (프론트엔드 + 백엔드를 하나의 저장소에서 관리)
B) 분리된 저장소 (프론트엔드와 백엔드를 별도 프로젝트로 관리)
C) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 5
배포 환경은 어디를 대상으로 하시겠습니까?

A) AWS (EC2, ECS, Lambda 등)
B) 로컬 서버 / 온프레미스
C) Docker 컨테이너 (배포 환경 미정, 컨테이너화만 우선)
D) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 6
프로그래밍 언어 타입 시스템 선호도는 어떻게 되시나요? (JavaScript 기반 선택 시)

A) TypeScript (정적 타입, 권장)
B) JavaScript (동적 타입)
C) 해당 없음 (JavaScript 기반이 아닌 기술 스택 선택)
D) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 7
관리자용 메뉴 관리 기능이 MVP 범위에 포함되어야 합니까? (요구사항 정의서 3.2.4에 정의되어 있으나 MVP 범위(섹션 4)에는 명시되지 않았습니다)

A) Yes — MVP에 메뉴 관리(CRUD) 포함
B) No — MVP에서는 제외하고 시드 데이터로 메뉴 제공
C) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 8: Security Extensions
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
C) Other (please describe after [Answer]: tag below)

[Answer]: 

## Question 9: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)
B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)
C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)
D) Other (please describe after [Answer]: tag below)

[Answer]: 
