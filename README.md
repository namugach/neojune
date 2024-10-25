## Ubuntu 24.04 기반 LEMP 스택 데이터 분석 환경 (SSH 포함)

### 개요

이 Docker 이미지는 Ubuntu 24.04 (한국어 지원)를 기반으로 Nginx 웹 서버, MySQL 데이터베이스, Python 데이터 분석 라이브러리, SSH 서버를 포함하는 데이터 분석 환경을 제공합니다. 한국어 로케일과 글꼴을 지원하며, SSH를 통해 안전하게 컨테이너에 접속하여 데이터 분석 작업을 수행하고 관리할 수 있습니다. 

### 주요 기능

* **웹 서버:** Nginx
* **데이터베이스:** MySQL 8
* **데이터 분석:** Pandas, NumPy, Openpyxl
* **KIPRIS API 연동:** requests, xmltodict, python-dotenv
* **운영 체제:** Ubuntu 24.04 (한국어 지원)
* **원격 접속:** SSH 서버 (root 계정 접속, SSH 키 기반 인증 지원)

### 설치 방법

1. **Docker 이미지 빌드:**

```bash
chmod +x install.sh
./install.sh
```

2. **Docker 컨테이너 실행:** `install.sh` 스크립트 실행 시 자동으로 컨테이너가 실행됩니다.

```bash
docker container run -itd -p 80:8080 -v ./:/root/work --name neojune ubuntu-neojune:24.04-kor-nmp
```

- `-p 80:8080`: 호스트 시스템의 80번 포트를 컨테이너의 8080번 포트로 연결 (웹 서버 접속)
- `-v ./:/root/work`: 현재 디렉토리를 컨테이너의 `/root/work` 디렉토리에 마운트 (호스트와 컨테이너 간 파일 공유)
- `--name neojune`: 컨테이너 이름을 `neojune`으로 설정

3. **MySQL 데이터베이스 초기화:** `install.sh` 스크립트 실행 시 자동으로 SQL 파일을 이용하여 데이터베이스를 초기화합니다.

```bash
docker container exec -i test mysql -u root neojune < res/sql/neojune_2024-10-25_133204.sql
```

- `docker container exec`: 실행 중인 컨테이너 내부에서 명령어 실행
- `mysql -u root neojune < res/sql/neojune_2024-10-25_133204.sql`: `neojune` 데이터베이스에 SQL 파일 (res/sql/neojune_2024-10-25_133204.sql)을 import

### 사용 방법

* **웹 서버 접속:** 브라우저에서 `http://localhost`로 접속합니다. 
* **MySQL 접속:**
- 호스트 시스템에서 MySQL 클라이언트를 사용하여 `localhost:3306`에 접속합니다.
- 사용자 이름: `ubuntu`, 비밀번호: `1234`
* **SSH 접속:** 터미널에서 `ssh root@localhost` 명령어를 사용하여 SSH로 접속합니다.
- 비밀번호: Dockerfile에서 설정한 `$PASSWORD` (Dockerfile 내 `echo 'root:$PASSWORD' | chpasswd` 부분에서 `$PASSWORD`를 원하는 비밀번호로 변경해야 합니다.)
* **데이터 분석:** 컨테이너 내부에서 Python 스크립트를 실행하여 데이터 분석 작업을 수행할 수 있습니다. `/root/work` 디렉토리에 Python 스크립트를 저장하면 호스트 시스템에서 해당 스크립트에 접근하고 수정할 수 있습니다.

### 환경 설정

* **root 비밀번호:** Dockerfile에서 `$PASSWORD`를 원하는 비밀번호로 변경합니다.
* **MySQL 데이터베이스:**  `neojune` 데이터베이스가 기본적으로 생성됩니다. 필요에 따라 추가 데이터베이스를 생성할 수 있습니다.
* **MySQL 사용자:**  `ubuntu` 사용자가 모든 권한을 가지고 생성됩니다. 필요에 따라 사용자를 추가하거나 권한을 수정할 수 있습니다.

### 추가 정보

* **SSH 키 기반 인증:**  Dockerfile에서 생성된 SSH 키를 사용하여 비밀번호 없이 SSH 접속을 설정할 수 있습니다.
* **Nginx 설정:** `/etc/nginx` 디렉토리에서 Nginx 설정 파일을 수정할 수 있습니다.
* **MySQL 설정:** `/etc/mysql/mysql.conf.d/mysqld.cnf` 파일에서 MySQL 설정을 변경할 수 있습니다.

### 라이선스

MIT License 
