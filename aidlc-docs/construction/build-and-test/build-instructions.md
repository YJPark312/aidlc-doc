# Build Instructions

## Prerequisites
- Docker & Docker Compose
- (선택) Node.js 20+ — 로컬 프론트엔드 개발 시

## Build Steps

### 1. 전체 서비스 빌드 및 실행
```bash
cd table-order
docker-compose up --build -d
```

### 2. 서비스 확인
- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:5173
- MySQL: localhost:3306

### 3. 빌드 성공 확인
```bash
docker-compose logs --tail 5
```
- Backend: `Application startup complete.` 출력 확인
- Frontend: `Local: http://localhost:5173/` 출력 확인
- DB: `ready for connections` 출력 확인

### 4. 종료
```bash
docker-compose down
```

### 5. 데이터 초기화 (DB 볼륨 삭제)
```bash
docker-compose down -v
```

## Troubleshooting

### Backend 시작 실패 — DB 연결 오류
- MySQL 초기화에 시간이 걸림. docker-compose healthcheck가 자동 대기
- `docker-compose down && docker-compose up --build -d`로 재시작

### Frontend 프록시 오류
- Backend가 먼저 실행되어야 함. `docker-compose logs backend`로 상태 확인
