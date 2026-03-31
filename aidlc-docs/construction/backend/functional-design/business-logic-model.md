# Business Logic Model — Backend

## Auth

### register_admin(username, password, store_name)
1. store_name 유니크 검증 → 중복 시 에러
2. 비밀번호 bcrypt 해싱
3. 트랜잭션: Store 생성 → AdminUser 생성
4. 반환: AdminUser + Store 정보

### login_admin(store_name, username, password)
1. store_name으로 Store 조회 → 없으면 에러
2. store_id + username으로 AdminUser 조회 → 없으면 에러
3. bcrypt 비밀번호 검증 → 불일치 시 에러
4. JWT 토큰 발급 (payload: user_id, store_id, role="admin", exp=16h)

### login_table(store_id, table_number, password)
1. store_id + table_number로 Table 조회 → 없으면 에러
2. bcrypt 비밀번호 검증 → 불일치 시 에러
3. JWT 토큰 발급 (payload: table_id, store_id, role="table", exp=16h)

## Menu

### create_menu(store_id, data, image_file?)
1. 필수 필드 검증 (name, price, category_id)
2. price >= 0 검증
3. category_id가 해당 store 소속인지 검증
4. image_file 있으면 → 로컬 저장, image_url 설정
5. Menu 생성 (is_deleted=false)

### update_menu(menu_id, data, image_file?)
1. Menu 조회 (is_deleted=false) → 없으면 에러
2. 필드 검증
3. image_file 있으면 → 기존 파일 삭제, 새 파일 저장
4. Menu 업데이트

### delete_menu(menu_id)
1. Menu 조회 → 없으면 에러
2. is_deleted = true (소프트 삭제)

### get_menus_by_category(store_id, category?)
1. is_deleted=false 필터
2. category 지정 시 해당 카테고리만
3. sort_order 기준 정렬

## Table

### setup_table(store_id, table_number, password)
1. store_id + table_number 중복 검증
2. 비밀번호 bcrypt 해싱
3. Table 생성

### complete_table_session(table_id)
1. 활성 세션 조회 (is_active=true) → 없으면 에러
2. 해당 세션의 미완료 주문 전체 → status='completed'로 강제 변경
3. 주문 + OrderItem → OrderHistory로 이동 (items_json에 스냅샷)
4. 해당 세션의 Order, OrderItem 삭제
5. TableSession.is_active=false, completed_at 설정

## Order

### create_order(store_id, table_id, session_id, items)
1. items 비어있으면 에러
2. 각 item의 menu_id 유효성 검증 (is_deleted=false)
3. 활성 세션 없으면 → 새 TableSession 자동 생성 (첫 주문 시 세션 시작)
4. Order 생성 (status='pending')
5. OrderItem 생성 (menu_name, menu_price 스냅샷 저장)
6. total_amount 계산
7. SSE 이벤트 발행 (store_id 대상)

### update_order_status(order_id, new_status)
1. Order 조회 → 없으면 에러
2. 상태 전이 검증: pending→preparing→completed (순차적만 허용)
3. 상태 업데이트
4. SSE 이벤트 발행

### delete_order(order_id)
1. Order 조회 → 없으면 에러
2. Order + OrderItem 삭제
3. SSE 이벤트 발행

### stream_orders(store_id)
1. SSEManager에 클라이언트 연결 등록
2. 매장의 주문 이벤트 스트리밍 (new_order, status_change, order_deleted)
