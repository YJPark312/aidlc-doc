# Integration Test Instructions

## 목적
Backend API와 Frontend가 올바르게 연동되는지 수동 통합 테스트

## 사전 준비
```bash
docker-compose up --build -d
```

## 테스트 시나리오

### Scenario 1: 관리자 회원가입 → 로그인
1. `http://localhost:5173/admin/register` 접속
2. 매장명: `테스트매장`, 사용자명: `admin`, 비밀번호: `admin123` 입력
3. 회원가입 성공 확인
4. `http://localhost:5173/admin/login`에서 로그인
5. **Expected**: 대시보드 화면 표시

### Scenario 2: 메뉴 관리 (CRUD)
1. 관리자 로그인 후 메뉴관리 페이지 이동
2. 카테고리 생성 → 메뉴 등록 (이름, 가격, 설명, 이미지)
3. 메뉴 수정, 삭제 테스트
4. **Expected**: CRUD 모두 정상 동작, 이미지 표시

### Scenario 3: 테이블 설정 → 고객 로그인
1. 관리자: 테이블관리에서 테이블 번호 1, 비밀번호 1234 설정
2. 고객: `http://localhost:5173/customer/login`에서 매장ID, 테이블 1, 비밀번호 1234 로그인
3. **Expected**: 메뉴 화면 표시, 카테고리별 메뉴 조회 가능

### Scenario 4: 주문 생성 → 실시간 알림
1. 브라우저 탭 2개: 관리자 대시보드 + 고객 메뉴 화면
2. 고객: 메뉴 선택 → 장바구니 → 주문하기
3. **Expected**: 관리자 대시보드에 실시간으로 주문 표시 (SSE)

### Scenario 5: 주문 상태 변경
1. 관리자: 주문 카드에서 "준비" 클릭 → "완료" 클릭
2. **Expected**: 상태가 순차적으로 변경 (대기중→준비중→완료)

### Scenario 6: 주문 삭제
1. 관리자: 주문 상세에서 "삭제" 클릭
2. **Expected**: 주문 삭제, 테이블 총 주문액 재계산

### Scenario 7: 테이블 이용 완료
1. 관리자: 테이블관리에서 "이용완료" 클릭
2. **Expected**: 미완료 주문 강제 완료, 주문 이력으로 이동, 테이블 리셋
3. 과거 내역 조회로 이동된 주문 확인

## Cleanup
```bash
docker-compose down -v
```
