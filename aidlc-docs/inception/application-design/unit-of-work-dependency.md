# Unit of Work Dependencies

## Dependency Matrix

| Unit | Depends On | Communication | Notes |
|------|-----------|---------------|-------|
| Backend | - | - | 독립적, 외부 의존성 없음 |
| Frontend | Backend | REST API (HTTP), SSE (HTTP streaming) | Backend API 완성 후 개발 |

## Development Sequence

```
[Unit 1: Backend] ──────> [Unit 2: Frontend]
  (FastAPI + MySQL +         (Vue.js SPA)
   Docker Compose)
```

- Backend가 선행 (API 엔드포인트 제공)
- Frontend는 Backend API에 의존
- Docker Compose는 Backend 유닛에 포함
