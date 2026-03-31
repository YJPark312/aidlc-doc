# Components

## Backend Components (FastAPI)

### 1. auth
- **Purpose**: 인증/인가 처리
- **Responsibilities**:
  - 관리자 회원가입 (매장 자동 생성)
  - 관리자 로그인 (JWT 발급, 16시간 세션)
  - 테이블 태블릿 로그인 (테이블 비밀번호 기반)
  - JWT 토큰 검증 미들웨어

### 2. store
- **Purpose**: 매장 정보 관리
- **Responsibilities**:
  - 매장 정보 조회/수정

### 3. menu
- **Purpose**: 메뉴 CRUD 및 카테고리 관리
- **Responsibilities**:
  - 메뉴 등록/수정/삭제/조회
  - 카테고리별 메뉴 조회
  - 메뉴 이미지 파일 업로드 (로컬 저장)
  - 메뉴 노출 순서 관리

### 4. table
- **Purpose**: 테이블 및 세션 관리
- **Responsibilities**:
  - 테이블 초기 설정 (번호, 비밀번호)
  - 테이블 세션 시작/종료 (이용 완료)
  - 테이블 목록 조회

### 5. order
- **Purpose**: 주문 처리 및 실시간 알림
- **Responsibilities**:
  - 주문 생성
  - 주문 상태 변경 (대기중→준비중→완료)
  - 주문 삭제 (관리자)
  - 현재 세션 주문 조회 (고객)
  - 테이블별 주문 조회 (관리자)
  - 과거 주문 내역 조회
  - SSE 실시간 주문 알림

## Frontend Components (Vue.js)

### 6. customer views
- **Purpose**: 고객용 화면
- **Responsibilities**:
  - 테이블 로그인/자동 로그인
  - 메뉴 조회 (카테고리별 카드 레이아웃)
  - 장바구니 관리 (localStorage)
  - 주문 생성 및 확인
  - 주문 내역 조회

### 7. admin views
- **Purpose**: 관리자용 화면
- **Responsibilities**:
  - 회원가입/로그인
  - 실시간 주문 모니터링 대시보드 (SSE)
  - 테이블 관리 (설정, 주문 삭제, 이용 완료, 과거 내역)
  - 메뉴 관리 (CRUD, 이미지 업로드)
