# Toolnet.Be 배포 매뉴얼 51~55

## 51~55. GitHub Actions CI/CD 작성법

### 51. workflow 파일 생성 위치

GitHub Actions workflow는 다음 폴더에 만든다.

```bash
mkdir -p .github/workflows
```

예시 파일명:

```bash
touch .github/workflows/backend-deploy.yml
```

파일명은 팀 기준에 맞춰 정한다.

### 52. 기본 CI workflow 예시

Python 의존성 설치와 테스트만 하는 기본 예시는 다음과 같다.

```yaml
name: Backend CI

on:
  pull_request:
    branches:
      - develop
  push:
    branches:
      - develop

jobs:
  ci:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest
```

테스트가 아직 없다면 `pytest` step은 팀원과 상의해서 제외하거나 대체한다.

### 53. Docker 빌드 workflow 예시

Docker 이미지 빌드만 확인하는 예시는 다음과 같다.

```yaml
name: Backend Docker Build

on:
  pull_request:
    branches:
      - develop

jobs:
  docker-build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t toolnetbe_backend .
```

이 workflow는 PR 단계에서 Dockerfile이 정상 빌드되는지 확인하는 용도로 사용할 수 있다.

### 54. 배포 workflow는 팀 기준 확인 후 작성

서버 배포 workflow는 서버 접속 정보, SSH key, secret, 배포 브랜치가 필요하다.

따라서 임의로 만들면 안 되고 팀원에게 확인해야 한다.

확인할 것:

```text
1. 배포 서버 IP
2. 서버 접속 계정
3. SSH private key secret 이름
4. 배포할 서버 폴더 경로
5. 배포 브랜치
6. docker-compose 명령어
7. 서버에서 sudo 비밀번호 없이 docker 실행 가능한지
```

### 55. SSH 배포 workflow 예시

팀 기준이 SSH 접속 후 서버에서 `git pull`과 `docker-compose up`을 실행하는 방식이라면 예시는 다음과 같다.

```yaml
name: Backend Deploy

on:
  push:
    branches:
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.BE_SERVER_HOST }}
          username: ${{ secrets.BE_SERVER_USER }}
          key: ${{ secrets.BE_SERVER_SSH_KEY }}
          script: |
            cd /path/to/toolnet-be
            git checkout develop
            git pull origin develop
            sudo docker-compose down
            sudo docker-compose up -d --build
            sudo docker ps
```

위 값은 예시이므로 secret 이름과 서버 경로는 팀원에게 받은 값으로 바꿔야 한다.
