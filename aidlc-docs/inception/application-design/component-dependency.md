# Component Dependencies

## Dependency Matrix

```
                auth  store  menu  table  order  SSE  FileStorage
auth             -     W      -     -      -     -      -
store            -     -      -     -      -     -      -
menu             -     R      -     -      -     -      W
table            -     R      -     -      R/W   -      -
order            -     R      R     R      -     W      -
customer-views   R     -      R     -      R/W   -      -
admin-views      R     R      R/W   R/W    R/W   R      -
```

R = Read, W = Write, R/W = Read+Write

## Communication Patterns

### Backend Internal
- Router → Service → Repository → Database (레이어 패턴)
- OrderService → SSEManager (이벤트 발행)
- TableService → OrderRepository (세션 종료 시 주문 이력 이동)
- AuthService → StoreRepository (회원가입 시 매장 자동 생성)

### Frontend → Backend
- REST API (HTTP): 모든 CRUD 작업
- SSE (HTTP streaming): 관리자 실시간 주문 모니터링

### Data Flow

```
[Customer Vue App] --REST--> [FastAPI] --SQLAlchemy--> [MySQL]
                                |
[Admin Vue App] ---REST--> [FastAPI]
                  <--SSE---    |
                          [SSEManager]
```
