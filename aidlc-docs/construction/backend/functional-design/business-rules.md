# Business Rules — Backend

## 인증 규칙
- BR-AUTH-01: 비밀번호는 bcrypt로 해싱 저장
- BR-AUTH-02: JWT 토큰 만료 시간 16시간
- BR-AUTH-03: JWT payload에 role 구분 (admin / table)
- BR-AUTH-04: 매장명(store_name) 유니크 제약
- BR-AUTH-05: 동일 매장 내 관리자 username 유니크 제약

## 메뉴 규칙
- BR-MENU-01: 메뉴 가격 >= 0
- BR-MENU-02: 메뉴명, 가격, 카테고리는 필수
- BR-MENU-03: 메뉴 삭제는 소프트 삭제 (is_deleted=true)
- BR-MENU-04: 삭제된 메뉴는 조회/주문 불가
- BR-MENU-05: 메뉴 노출 순서는 sort_order 기준 오름차순

## 테이블 규칙
- BR-TABLE-01: 동일 매장 내 테이블 번호 유니크
- BR-TABLE-02: 테이블당 활성 세션 최대 1개

## 세션 규칙
- BR-SESSION-01: 첫 주문 시 활성 세션 없으면 자동 생성
- BR-SESSION-02: 세션 종료 시 미완료 주문 강제 완료 처리
- BR-SESSION-03: 세션 종료 시 주문 → OrderHistory 이동 후 원본 삭제
- BR-SESSION-04: 세션 종료 후 테이블 주문 목록/총액 리셋

## 주문 규칙
- BR-ORDER-01: 주문 항목 최소 1개 이상
- BR-ORDER-02: 주문 시 메뉴 이름/가격 스냅샷 저장 (OrderItem)
- BR-ORDER-03: 상태 전이 순차적만 허용 (pending → preparing → completed)
- BR-ORDER-04: 주문 생성 시 SSE 이벤트 발행
- BR-ORDER-05: 주문 상태 변경 시 SSE 이벤트 발행
- BR-ORDER-06: 주문 삭제 시 SSE 이벤트 발행

## 이미지 규칙
- BR-IMG-01: 이미지 파일 서버 로컬 저장
- BR-IMG-02: 메뉴 수정 시 새 이미지 업로드하면 기존 파일 삭제
