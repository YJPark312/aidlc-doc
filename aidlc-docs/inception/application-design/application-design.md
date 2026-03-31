# Application Design — 테이블오더 시스템

## Overview
- **Architecture**: FastAPI (feature-based) + Vue.js (SPA, 라우팅 분리) + MySQL (SQLAlchemy ORM)
- **API Style**: RESTful (/api/v1/...)
- **Real-time**: SSE (Server-Sent Events)
- **Deployment**: Docker Compose (backend + frontend + mysql)

## Backend Structure (Feature-based)
```
backend/
  app/
    auth/        # 인증 (회원가입, 로그인, JWT)
    store/       # 매장 관리
    menu/        # 메뉴 CRUD, 이미지 업로드
    table/       # 테이블/세션 관리
    order/       # 주문 처리, SSE
    core/        # 공통 (DB, config, dependencies)
```

각 feature 디렉토리: router.py, service.py, repository.py, schemas.py, models.py

## Frontend Structure (Single Vue App)
```
frontend/
  src/
    views/
      customer/  # 고객용 (메뉴, 장바구니, 주문)
      admin/     # 관리자용 (대시보드, 메뉴관리, 테이블관리)
    components/  # 공통 컴포넌트
    stores/      # Pinia 상태 관리
    router/      # Vue Router (customer/*, admin/*)
    api/         # API 호출 모듈
```

## API Endpoints (RESTful)

### Auth
- POST /api/v1/auth/register — 관리자 회원가입 + 매장 생성
- POST /api/v1/auth/login — 관리자 로그인
- POST /api/v1/auth/table-login — 테이블 로그인

### Menu
- GET /api/v1/stores/{storeId}/menus — 메뉴 조회
- POST /api/v1/stores/{storeId}/menus — 메뉴 등록
- PUT /api/v1/menus/{menuId} — 메뉴 수정
- DELETE /api/v1/menus/{menuId} — 메뉴 삭제
- PATCH /api/v1/stores/{storeId}/menus/order — 메뉴 순서 변경

### Table
- POST /api/v1/stores/{storeId}/tables — 테이블 설정
- GET /api/v1/stores/{storeId}/tables — 테이블 목록
- POST /api/v1/tables/{tableId}/complete — 이용 완료

### Order
- POST /api/v1/tables/{tableId}/orders — 주문 생성
- GET /api/v1/sessions/{sessionId}/orders — 세션 주문 조회 (고객)
- GET /api/v1/tables/{tableId}/orders — 테이블 주문 조회 (관리자)
- PATCH /api/v1/orders/{orderId}/status — 주문 상태 변경
- DELETE /api/v1/orders/{orderId} — 주문 삭제
- GET /api/v1/tables/{tableId}/order-history — 과거 내역
- GET /api/v1/stores/{storeId}/orders/stream — SSE 실시간 알림

## Key Design Decisions
1. 회원가입 시 매장 자동 생성 (1 관리자 = 1 매장)
2. 테이블 세션은 첫 주문 시 자동 시작, 관리자가 이용 완료 처리 시 종료
3. SSE는 매장 단위로 연결 관리 (SSEManager in-memory)
4. 장바구니는 클라이언트 localStorage에서 관리
5. 이미지는 서버 로컬 파일 시스템에 저장, static file serving
