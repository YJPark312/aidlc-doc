# Component Methods

> Note: 상세 비즈니스 로직은 Functional Design(CONSTRUCTION) 단계에서 정의

## auth

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| register_admin | username, password, store_name | AdminUser + Store | 관리자 회원가입 + 매장 자동 생성 |
| login_admin | store_identifier, username, password | JWT token | 관리자 로그인 |
| login_table | store_id, table_number, password | JWT token | 테이블 태블릿 로그인 |
| verify_token | JWT token | user/table info | 토큰 검증 |

## store

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| get_store | store_id | Store | 매장 정보 조회 |

## menu

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| create_menu | store_id, menu_data, image_file? | Menu | 메뉴 등록 |
| update_menu | menu_id, menu_data, image_file? | Menu | 메뉴 수정 |
| delete_menu | menu_id | void | 메뉴 삭제 |
| get_menus_by_category | store_id, category? | List[Menu] | 카테고리별 메뉴 조회 |
| update_menu_order | store_id, menu_orders | void | 메뉴 노출 순서 변경 |
| upload_image | image_file | image_url | 이미지 파일 로컬 저장 |

## table

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| setup_table | store_id, table_number, password | Table | 테이블 초기 설정 |
| get_tables | store_id | List[Table] | 테이블 목록 조회 |
| complete_table_session | table_id | void | 테이블 이용 완료 (세션 종료) |

## order

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| create_order | store_id, table_id, session_id, items | Order | 주문 생성 |
| get_orders_by_session | session_id | List[Order] | 현재 세션 주문 조회 (고객) |
| get_orders_by_table | table_id | List[Order] | 테이블별 현재 주문 조회 (관리자) |
| update_order_status | order_id, status | Order | 주문 상태 변경 |
| delete_order | order_id | void | 주문 삭제 (관리자) |
| get_order_history | table_id, date_filter? | List[OrderHistory] | 과거 주문 내역 조회 |
| stream_orders | store_id | SSE stream | 실시간 주문 알림 (SSE) |
