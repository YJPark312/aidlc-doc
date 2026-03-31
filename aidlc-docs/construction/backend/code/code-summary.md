# Backend Code Summary

## Generated Files

### Core (backend/app/core/)
- `config.py` — 환경 설정 (DB URL, JWT 설정, 업로드 경로)
- `database.py` — SQLAlchemy async 엔진/세션, Base 클래스
- `security.py` — bcrypt 해싱, JWT 생성/검증
- `dependencies.py` — FastAPI 의존성 (인증 미들웨어)

### Auth Module (backend/app/auth/)
- `models.py` — Store, AdminUser 엔티티
- `schemas.py` — 요청/응답 Pydantic 스키마
- `repository.py` — DB 접근 레이어
- `service.py` — 회원가입(매장 자동 생성), 관리자 로그인, 테이블 로그인
- `router.py` — POST /register, /login, /table-login

### Menu Module (backend/app/menu/)
- `models.py` — Category, Menu 엔티티 (소프트 삭제)
- `schemas.py` — CRUD 스키마
- `repository.py` — DB 접근 레이어
- `service.py` — 메뉴 CRUD, 이미지 업로드/삭제, 순서 변경
- `router.py` — 카테고리/메뉴 CRUD 엔드포인트

### Table Module (backend/app/table/)
- `models.py` — Table, TableSession 엔티티
- `schemas.py` — 설정/응답 스키마
- `repository.py` — DB 접근 레이어
- `service.py` — 테이블 설정, 세션 완료 (강제 완료 + OrderHistory 이동)
- `router.py` — 테이블 설정/조회/이용완료 엔드포인트

### Order Module (backend/app/order/)
- `models.py` — Order, OrderItem, OrderHistory 엔티티
- `schemas.py` — 주문 생성/응답 스키마
- `repository.py` — DB 접근 레이어
- `service.py` — 주문 생성(세션 자동 시작), 상태 변경(순차적), 삭제, SSE 발행
- `sse.py` — SSEManager (매장별 in-memory 연결 관리)
- `router.py` — 주문 CRUD + SSE 스트림 엔드포인트

### Infrastructure
- `backend/Dockerfile` — Python 3.12 slim
- `backend/requirements.txt` — FastAPI, SQLAlchemy, asyncmy, bcrypt, PyJWT 등
- `backend/init.sql` — MySQL 초기화
- `docker-compose.yml` — backend + MySQL 서비스
