## docker image란
 애플리케이션 실행에 필요한 파일 시스템과 설정을 변경할 수 없다. 

 즉 실행환경을 담은 템플릿 이다.

## dockerfile 
### 도커 파일 이란?
dockerfile은 이미지를 생성하기 위한 파일이다.

### 도커 파일 만드는법

도커 파일을 만들기 위해서는 
폴더 생성이 필요하다 
```
ubuntu@gsmsv:~$ mkdir name1

ubuntu@gsmsv:~$ ls

docker-test  name1

cd name1

ubuntu@gsmsv:~/name1$

```
이렇게 폴더를 생성할 수 있고 cd name1 으로 폴더에 들어갈 수 있다

#### 이제 도커 파일을 만들 차례이다  
도커 파일을 만들기 위해서는 nano [파일이름]
이런식으로 만들면 파일이 만들어 진다.

(nano 는 파일 편집하는 도구이다.)

#### 파일 작성

파일 안에 적는 것은 코드/내용/스크립트 같은 것이다.
를 작성하고
```
FROM ubuntu

CMD ["echo", "Hello Docker"]
```
적는다 

### FROM ubuntu

ubuntu 이미지를 기반으로 새로운 이미지를 만들겠다, 이다

### CMD
  실행할 명령       이다 

##### echo
 문자열을 출력하는 명령어 이다


 ctrl o를 누르고 enter ctrl x를 누르면 저장하고 나가진다.

 ### 이미지 만들고 실행

 ```
 sudo docker build -t hello  -f testfile .
 ``` 
 라고 치게된다면 

 -t [이미지 이름] 
 
 -f[도커파일 지정]
 sudo는 관리자 권한으로 실행하는 명령어 이다.

. 은 Dockerfile이 있는  현재 폴더를 기준으로  빌드 대상으로 지정하겠다, 이다.
```
  sudo docker run hello

Hello Docker
```
이러면 실행까지 된 것이다.

## docker-compose 
Docker Compose = 여러 컨테이너를 한 번에 정의하고 실행하는 도구 이다.

하나씩 이미지를 실행해야 해서 불편함 때문에 만들어 졌다