# Git Flow란?
## Git Flow는 프로젝트를 체계적으로 관리하기 위한 브랜치 전략이다.

예를 들자면
```
main
│
└── develop
    │
    ├── feature/login
    ├── feature/comment-fix
    ├── feature/signup
    └── feature/board
```
이런 구조를 말한다.

## main 
* 최종 배포 버전
* 가장 안정적인 코드 보관
* 함부로 작업하지 않음
### 즉 메인 브랜치는  최종 코드(배포 코드)를 관리하는 브랜치 이다.

## develop 
* 개발 내용 모으는 브랜치
* feature 브랜치들이 최종적으로 합쳐지는 곳
```
feature/login
      ↓
develop
      ↑
feature/signup
```
### 즉 develop 브랜치는 개발 중인 코드를 통합하여 관리하는 브랜치 이다.

## feature 
* 새로운 기능을 추가
```
feature/기능명
```
```
feature/login
feature/signup
feature/comment
feature/comment-fix
feature/post
feature/search
```
### feature 브랜치는 새로운 기능을 개발하기 위해 사용하는 브랜치 이다.

## release
* 배포 준비용 
```
release/1.0
release/2.0
```
```
develop
    ↓
release/1.0
    ↓
main
```
### 배포 직전 테스트를 하는 브랜치 이다.

## hotfix

### 긴급 버그를 수정하는 브랜치로
```
hotfix/login-error
hotfix/security-fix
```
### 상황으로는
```
main
 ↓
hotfix/login-error
 ↓
main
``` 
서비스 중 오류가 발생했을 때 hotfix 브랜치를 쓴다.


# 주의 할 점


### github에서 기본 브랜치(Default Branch)를 main 으로 설정해진 건지 확인하기

### 브랜치를 생성하기 전에 현재 어떤 브랜치에 있는지 확인 하기
```
git branch
```

### 브랜치를 병합(Merge)할 때는 병합 대상 브랜치를 정확히 확인해야 한다.

### 작업 후 변경 내용을 Commit하고 원격 저장소에 Push 했는지 확인해야 한다.