# Services

## Backend Services (FastAPI feature-based)

### AuthService
- **Responsibility**: 인증/인가 비즈니스 로직
- **Orchestration**: AdminUser 생성 → Store 자동 생성 (회원가입 시 트랜잭션)
- **Dependencies**: UserRepository, StoreRepository, JWT utils, bcrypt

### MenuService
- **Responsibility**: 메뉴 CRUD 비즈니스 로직
- **Orchestration**: 메뉴 데이터 검증 → 이미지 저장 → DB 저장
- **Dependencies**: MenuRepository, FileStorage

### TableService
- **Responsibility**: 테이블 및 세션 관리 비즈니스 로직
- **Orchestration**: 세션 종료 시 → 현재 주문을 OrderHistory로 이동 → 테이블 리셋
- **Dependencies**: TableRepository, OrderRepository, OrderHistoryRepository

### OrderService
- **Responsibility**: 주문 처리 및 실시간 알림
- **Orchestration**: 주문 생성 → DB 저장 → SSE 이벤트 발행
- **Dependencies**: OrderRepository, SSEManager

### SSEManager
- **Responsibility**: Server-Sent Events 연결 관리
- **Orchestration**: 매장별 클라이언트 연결 관리, 이벤트 브로드캐스트
- **Dependencies**: None (in-memory connection pool)

### FileStorageService
- **Responsibility**: 이미지 파일 로컬 저장/조회
- **Orchestration**: 파일 검증 → 저장 → URL 반환
- **Dependencies**: Local filesystem
