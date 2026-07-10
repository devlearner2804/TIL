# Toolnet.Be 배포 매뉴얼 41~45

## 41~45. docker-compose.yml 작성법

### 41. docker-compose.yml의 역할

`docker-compose.yml`은 backend, redis 같은 여러 컨테이너를 한 번에 실행하기 위한 설정 파일이다.

백엔드 배포에서는 보통 다음 내용을 관리한다.

```text
1. backend 서비스
2. redis 서비스
3. 포트 매핑
4. .env 연결
5. DB 파일 마운트
6. 컨테이너 재시작 정책
```

### 42. 기본 docker-compose.yml 예시

```yaml
version: "3.8"

services:
  backend:
    build: .
    container_name: toolnet-be-dev
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./Grape.db:/app/Grape.db
    depends_on:
      - redis
    restart: always

  redis:
    image: redis:7
    container_name: toolnet-redis-dev
    ports:
      - "6379:6379"
    restart: always
```

프로젝트마다 서비스 이름, 포트, 컨테이너 이름은 다를 수 있으므로 팀원에게 기준을 확인한다.

### 43. backend 서비스 설명

```yaml
backend:
  build: .
```

현재 폴더의 Dockerfile을 사용해 backend 이미지를 빌드한다.

```yaml
container_name: toolnet-be-dev
```

컨테이너 이름을 `toolnet-be-dev`로 지정한다.

```yaml
ports:
  - "8000:8000"
```

호스트의 8000 포트를 컨테이너의 8000 포트에 연결한다.

```yaml
env_file:
  - .env
```

`.env` 파일을 컨테이너 환경 변수로 전달한다.

### 44. DB 파일 마운트 설명

```yaml
volumes:
  - ./Grape.db:/app/Grape.db
```

호스트의 `./Grape.db` 파일을 컨테이너 내부 `/app/Grape.db` 파일로 연결한다.

주의할 점:

```text
1. 호스트에 Grape.db 파일이 있어야 한다.
2. Grape.db가 디렉터리면 안 된다.
3. Grape.db를 삭제했다면 touch Grape.db로 빈 파일을 먼저 만들어야 한다.
4. DB 구조 변경 시 기존 DB를 삭제하기 전에 백업 여부를 확인해야 한다.
```

### 45. Compose 실행 명령어

빌드와 실행을 함께 한다.

```bash
sudo docker-compose up -d --build
```

컨테이너를 내린다.

```bash
sudo docker-compose down
```

로그를 확인한다.

```bash
sudo docker-compose logs --tail=100 backend
```

실행 중인 컨테이너를 확인한다.

```bash
sudo docker ps
```
