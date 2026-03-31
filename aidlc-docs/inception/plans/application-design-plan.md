# Application Design Plan

## 설계 계획

- [x] 컴포넌트 식별 및 책임 정의
- [x] 컴포넌트 메서드 시그니처 정의
- [x] 서비스 레이어 설계
- [x] 컴포넌트 의존성 및 통신 패턴 정의
- [x] 설계 완전성 검증

---

## 설계 관련 질문

아래 질문에 답변해 주세요. 각 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

## Question 1
FastAPI 백엔드의 프로젝트 구조를 어떤 방식으로 구성하시겠습니까?

A) 기능별 분리 (feature-based) — auth/, menu/, order/, table/ 등 기능 단위 디렉토리
B) 레이어별 분리 (layer-based) — models/, routers/, services/, repositories/ 등 계층 단위 디렉토리
C) Other (please describe after [Answer]: tag below)

[Answer]:  A

## Question 2
Vue.js 프론트엔드에서 고객용 화면과 관리자용 화면을 어떻게 구성하시겠습니까?

A) 단일 Vue 앱에서 라우팅으로 분리 (고객: /customer/*, 관리자: /admin/*)
B) 별도의 Vue 앱 2개로 분리 (customer-app, admin-app)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
API 엔드포인트 URL 설계 스타일은 어떤 것을 선호하시나요?

A) RESTful 리소스 기반 — /api/v1/stores/{storeId}/menus, /api/v1/orders 등
B) 기능 기반 단순 경로 — /api/menus, /api/orders 등 (버전 없이)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4
데이터베이스 접근 방식은 어떤 것을 사용하시겠습니까?

A) SQLAlchemy ORM (객체-관계 매핑)
B) Raw SQL 쿼리 직접 작성
C) Tortoise ORM (async 네이티브)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5
관리자 회원가입 시 매장(Store) 생성 방식은 어떻게 하시겠습니까?

A) 회원가입 시 매장도 함께 생성 (1 관리자 = 1 매장 자동 생성)
B) 매장을 먼저 생성하고, 관리자가 매장 코드로 가입
C) Other (please describe after [Answer]: tag below)

[Answer]: A
