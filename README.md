## 1. 미션 요구사항 분석 & 체크리스트

---

### 1-1. 미션 요구사항 분석

---

**CLI 기반 메뉴**

메 루프마다 유저에게 보여줄 화면을 띄우고 필요하다면 유저의 입력을 받아야 한다.
메 메뉴마다 화면을 초기화 시켜줘야 한다.

**데이터 입력 기능**

직접입력과 파일선택의 2가지 입력 방법을 선택하게 한다.
입력은 사용자에게 필요한 입력을 받고 확인 후 적용한다.
파일은 자동 검색과 수동 입력을 넣고 자동의 경우 하위 디렉토리까지 검색한다.

**도서 정보 조회 기능**

사용자로부터 도서의 정보를 입력받아 상세를 출력한다.

**도서 대출 기능**

대출도서 확인과 대출 하기 선택
대출 시 도서 상태 변경

**도서 반납 기능**

대출도서 확인과 반납 하기 선택
반납 시 도서 상태 변경

**대출 정보 조회 기능**

대출 정보 출력

**종료 기능**

종료

---

### 1-2. 미션 체크리스트

---

**CLI 구현**
  
- 렌더 데이터 클래스
  
  화면에 출력할 데이터를 담을 클래스  
  페이지 목록과 상세 내용을 저장한다.  
  페이지는 문자열로 저장한다.

  - [x] 테스트 케이스 생성
  - [x] 페이지 리스트
  - [x] 선택된 페이지
  - [x] 상세 화면 데이터
  - [x] 데이터 업데이터

---

- 출력 함수

  데이터를 가지고 화면에 출력해 줄 클래스

  - [x] 테스트 케이스 생성
  - [x] 데이터를 가지고 화면 그리기
  - [x] 메번 출력

---

- 메인 컨트롤러 클래스

  루프를 돌면서 데이터를 받아 전달하고 다른 페이지를 생성해 실행하는 함수  
  겸사 겸사 키 입력을 받아 페이지에 전달

  - [x] 테스트 케이스 생성
  - [x] 출력 함수 실행
  - [x] 새 페이지 생성
  - [x] 키 입력 구현
  - [x] 뒤로가기 구현

---

**페이지 구현**

- Base Page

  페이지는 입력을 받아 로직을 실행한다.  
  페이지는 렌더 데이터 클래스를 반환할 수 있다.     
  페이지는 메인 컨트롤러에서 생성되고 실행된다.  

  - [x] 테스트 케이스 생성
  - [x] 렌더 데이터 반환
  - [x] 메인 로직 실행

- Main Page

  가장 처음에 출력되는 페이지 이다.

  - [x] 테스트 케이스 생성
  - [x] 종료 구현

- New Books Page

  새로운 책을 등록할 수 있는 페이지 이다.  
  입력 방법은 직접 입력과 파일 선택이 있다.  

  - [ ] 테스트 케이스 생성
  - [ ] 화면 출력 작성

**database api**

-- 추가 예정

## 2. 미션 진행 & 회고

---

### 2-1. 미션 진행 내용 요약

---

**CLI 계획**

우선 CLI 구현을 어떻게 할지 고민하였다. 요즘 추상화을 이해하고 있는 중이라 추상화를 적용해 보고 싶었다.

매번 화면이 지워지고 새로운 출력 결과가 생길텐데 그 하나의 화면을 page라는 단위로 추상화 하였다.

또 유저가 선택하는 경우와 입력하는 경우로 page를 나눠 추상화 하였다. 유저 입력이 없는 경우도 따로 뺄까 했지만 큰 의미가 없을 것 같았다. (추가될지도?)

ListPage를 구현할 때 각각의 선택지에 다른 로직을 어떻게 넣을지 고민이 있었다. 선택 리스트를 문자열로 받아 유저 입력을 처리하는 로직에서 입력 값으로 나눠 처리할 수도 있겠지만 그렇게 하면 코드의 중복이 늘어나고 유지보수가 어려울 것 같았다. 그래서 discordpy나 fastapi에서 사용하는 데코레이터를 참고하여 선택지를 생성하는 데코레이터를 만들어서 사용하려 하였으나 클래스 단위로 만들다 보니 잘 되지 않았다. 그래서 각각의 선택지를 ListOption 클래스를 상속받은 클래스에 답아서 구현하였다. 이렇게 하면 각각의 선택지에 다른 로직을 넣을 수 있고 유지보수도 쉬울 것 같았다.

CLI 디자인을 생각하다 보니 왼쪽에 목록 오른쪽에 상세를 보여주게 하고 싶었다.  
그래서 각각의 기능은 데이터만 전달하도록 구현하고 출력은 따로 화면을 그려줄 클래스를 만드는 게 좋을 것 같다. 그리고 화면을 직접 그리면 input을 쓰기는 어려울 듯 하니 메인 컨트롤러에서 입력을 기능에 넘겨주는 방식으로 구현해야 할 것 같다.

---

### 2-2. 회고

---

later...