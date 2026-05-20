# CRUD 게시판 만들기
## CRUD 게시판 이란?
### C: 생성
### R: 조회
### U: 수정
### D: 삭제
### CRUD는 가장 기초적인 틀로, CRUD로 만든 게시판을 CRUD 게시판 이라고 한다.
---
---

## 모르는 개념 정리
### Controller 
#### 사용자의 요청(URL)을 받아 처리하는 역할을 한다. 
```@GetMapping,@PostMapping    ``` 
#### 등을 사용하여 페이지 이동과 기능 실행을 처리하였다
---
### @(annotation)
#### 코드의 역할을 알려주는 표시    ```@Controller ``` 는 스프링한테 이 클래스가 요청을 처리하는 클래스 라고 전달해 준다
#### ```@RequestMapping("/board``` 공통 주소 설정 즉 
* /board/save 
* /board/update
* /board/1
#### 처럼 /board부터 시작하게 함

` 