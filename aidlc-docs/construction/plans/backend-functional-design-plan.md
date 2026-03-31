# Backend Functional Design Plan

## 계획

- [x] 도메인 엔티티 및 관계 정의
- [x] 비즈니스 로직 모델 설계
- [x] 비즈니스 규칙 및 검증 로직 정의
- [x] 설계 완전성 검증

---

## Functional Design 질문

각 `[Answer]:` 태그 뒤에 선택지 알파벳을 입력해 주세요.

## Question 1
주문 상태 변경 흐름에서 "준비중" 상태를 건너뛰고 바로 "완료"로 변경할 수 있어야 하나요?

A) 순차적으로만 가능 (대기중 → 준비중 → 완료)
B) 건너뛰기 허용 (대기중 → 완료 가능)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
테이블 세션 종료(이용 완료) 시, 아직 "대기중" 또는 "준비중"인 주문이 있으면 어떻게 처리하나요?

A) 모든 주문을 강제로 "완료" 처리 후 세션 종료
B) 미완료 주문이 있으면 세션 종료 불가 (에러 반환)
C) 미완료 주문 상태 그대로 이력으로 이동
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
관리자 회원가입 시 동일한 매장명 중복을 허용하나요?

A) 매장명 중복 허용 (매장 식별은 자동 생성 ID로)
B) 매장명 중복 불허 (유니크 제약)
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 4
메뉴 삭제 시 해당 메뉴가 포함된 기존 주문은 어떻게 처리하나요?

A) 소프트 삭제 (is_deleted 플래그) — 기존 주문에서 메뉴 정보 유지
B) 하드 삭제 — 기존 주문의 메뉴 정보는 주문 시점 스냅샷으로 보존
C) Other (please describe after [Answer]: tag below)

[Answer]: A
