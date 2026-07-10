# Toolnet.Be 배포 매뉴얼 36~40

## 36~40. Dockerfile 작성법

### 36. Dockerfile의 역할

Dockerfile은 백엔드 앱을 어떤 환경에서 실행할지 정의하는 파일이다.

Python FastAPI 프로젝트라면 보통 다음 내용을 포함한다.

```text
1. Python 베이스 이미지
2. 컨테이너 작업 폴더
3. requirements.txt 복사
4. 패키지 설치
5. 소스 코드 복사
6. uvicorn 실행 명령어
```

### 37. 기본 Dockerfile 예시

FastAPI 기준 기본 예시는 다음과 같다.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

팀원에게 Python 버전과 실행 명령어가 맞는지 반드시 확인해야 한다.

### 38. Dockerfile 각 줄 의미

```dockerfile
FROM python:3.11-slim
```

Python 3.11 기반의 가벼운 이미지를 사용한다.

```dockerfile
WORKDIR /app
```

컨테이너 내부 작업 폴더를 `/app`으로 설정한다.

```dockerfile
COPY requirements.txt .
```

호스트의 `requirements.txt`를 컨테이너 내부 `/app`으로 복사한다.

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

필요한 Python 패키지를 설치한다.

```dockerfile
COPY . .
```

현재 프로젝트 파일 전체를 컨테이너 내부 `/app`으로 복사한다.

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

컨테이너가 실행될 때 FastAPI 서버를 실행한다.

### 39. Dockerfile 작성 후 빌드 확인

Dockerfile이 있는 폴더에서 이미지를 빌드한다.

```bash
sudo docker build -t toolnetbe_backend .
```

빌드가 성공하면 이미지 목록에서 확인한다.

```bash
sudo docker images
```

특정 이미지 이름만 확인한다.

```bash
sudo docker images | grep toolnetbe_backend
```

### 40. Dockerfile 오류 확인 방법

빌드 중 오류가 나면 보통 다음을 확인한다.

```text
1. requirements.txt 파일이 있는가
2. 패키지 이름이 잘못되지 않았는가
3. Python 버전과 패키지가 호환되는가
4. main.py에 app 객체가 있는가
5. uvicorn 실행 경로가 맞는가
```

컨테이너를 직접 실행해 확인할 수도 있다.

```bash
sudo docker run --rm -p 8000:8000 toolnetbe_backend
```
