# Backend Code Generation Plan

## Unit Context
- **Unit**: Backend (FastAPI + MySQL + Docker Compose)
- **Workspace Root**: /Users/datapipeline-poc/Desktop/aidlc-kiro/table-order
- **Code Location**: `backend/` (Greenfield multi-unit)
- **Tech Stack**: Python, FastAPI, SQLAlchemy, MySQL, Docker Compose
- **Requirements**: FR-1, FR-2, FR-4~FR-10, NFR-2

## Steps

### Step 1: Project Structure & Configuration
- [ ] `backend/app/__init__.py`
- [ ] `backend/app/main.py` — FastAPI 앱 엔트리포인트
- [ ] `backend/app/core/__init__.py`
- [ ] `backend/app/core/config.py` — 환경 설정
- [ ] `backend/app/core/database.py` — SQLAlchemy 엔진/세션
- [ ] `backend/app/core/security.py` — JWT, bcrypt 유틸
- [ ] `backend/app/core/dependencies.py` — FastAPI 의존성 (get_db, get_current_user)
- [ ] `backend/requirements.txt`
- [ ] `backend/Dockerfile`
- [ ] `docker-compose.yml`

### Step 2: Auth Module (FR-6, FR-10, FR-1)
- [ ] `backend/app/auth/__init__.py`
- [ ] `backend/app/auth/models.py` — Store, AdminUser SQLAlchemy 모델
- [ ] `backend/app/auth/schemas.py` — Pydantic 스키마
- [ ] `backend/app/auth/repository.py` — DB 접근
- [ ] `backend/app/auth/service.py` — 비즈니스 로직
- [ ] `backend/app/auth/router.py` — API 엔드포인트

### Step 3: Menu Module (FR-2, FR-9)
- [ ] `backend/app/menu/__init__.py`
- [ ] `backend/app/menu/models.py` — Category, Menu 모델
- [ ] `backend/app/menu/schemas.py`
- [ ] `backend/app/menu/repository.py`
- [ ] `backend/app/menu/service.py`
- [ ] `backend/app/menu/router.py`

### Step 4: Table Module (FR-8)
- [ ] `backend/app/table/__init__.py`
- [ ] `backend/app/table/models.py` — Table, TableSession 모델
- [ ] `backend/app/table/schemas.py`
- [ ] `backend/app/table/repository.py`
- [ ] `backend/app/table/service.py`
- [ ] `backend/app/table/router.py`

### Step 5: Order Module (FR-4, FR-5, FR-7)
- [ ] `backend/app/order/__init__.py`
- [ ] `backend/app/order/models.py` — Order, OrderItem, OrderHistory 모델
- [ ] `backend/app/order/schemas.py`
- [ ] `backend/app/order/repository.py`
- [ ] `backend/app/order/service.py`
- [ ] `backend/app/order/sse.py` — SSEManager
- [ ] `backend/app/order/router.py`

### Step 6: Database Init Script
- [ ] `backend/init.sql` — MySQL 초기화 스크립트 (CREATE DATABASE)

### Step 7: Documentation
- [ ] `aidlc-docs/construction/backend/code/code-summary.md`
