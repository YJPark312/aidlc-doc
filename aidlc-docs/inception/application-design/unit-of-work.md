# Unit of Work

## Unit 1: Backend (backend)
- **Type**: Service (FastAPI + MySQL + Docker Compose)
- **Responsibilities**:
  - FastAPI REST API 전체 (auth, store, menu, table, order)
  - SQLAlchemy ORM + MySQL 데이터 모델
  - SSE 실시간 주문 알림
  - 이미지 파일 로컬 저장
  - JWT 인증/인가
  - Docker Compose 인프라 설정 (FastAPI, MySQL, Nginx)
- **Development Order**: 1st (API 완성 후 Frontend 개발)

### Code Organization (Greenfield)
```
backend/
  app/
    main.py              # FastAPI 앱 엔트리포인트
    auth/
      router.py, service.py, repository.py, schemas.py, models.py
    store/
      router.py, service.py, repository.py, schemas.py, models.py
    menu/
      router.py, service.py, repository.py, schemas.py, models.py
    table/
      router.py, service.py, repository.py, schemas.py, models.py
    order/
      router.py, service.py, repository.py, schemas.py, models.py
    core/
      database.py, config.py, dependencies.py, security.py
    uploads/             # 이미지 파일 저장
  requirements.txt
  Dockerfile
docker-compose.yml
```

## Unit 2: Frontend (frontend)
- **Type**: Module (Vue.js SPA)
- **Responsibilities**:
  - 고객용 화면 (메뉴 조회, 장바구니, 주문, 주문 내역)
  - 관리자용 화면 (로그인, 회원가입, 대시보드, 메뉴 관리, 테이블 관리)
  - SSE 수신 (관리자 실시간 모니터링)
  - localStorage 장바구니/자동 로그인
- **Development Order**: 2nd (Backend API 완성 후)

### Code Organization (Greenfield)
```
frontend/
  src/
    views/
      customer/          # 고객용 페이지
      admin/             # 관리자용 페이지
    components/          # 공통 컴포넌트
    stores/              # Pinia 상태 관리
    router/              # Vue Router
    api/                 # Axios API 모듈
    assets/              # 정적 리소스
  package.json
  Dockerfile
```
