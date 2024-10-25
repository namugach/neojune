FROM namugach/ubuntu-basic:24.04-kor
WORKDIR /root

RUN apt-get update

# Nginx, MySQL 서버, 및 MySQL 개발 라이브러리 설치
RUN apt-get install -y nginx mysql-server pkg-config libmysqlclient-dev

# 데이터 분석 및 데이터베이스 연결을 위한 Python 라이브러리 설치
RUN pip install pandas mysqlclient numpy openpyxl requests xmltodict python-dotenv

#### 여기부터 SSH 
RUN mkdir /var/run/sshd

# root password 변경, $PASSWORD를 변경한다.
RUN echo 'root:$PASSWORD' |  chpasswd

# ssh 설정 변경
# root 계정으로의 로그인을 허용한다.
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/^#Port 22/Port 22/' /etc/ssh/sshd_config
RUN sed -ri 's/^#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config

# SSH 키 생성
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -N ""

# SSH 설정
RUN mkdir -p /root/.ssh && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys && \
    chmod 700 /root/.ssh

# ssh 최초 접속시 yes 생략
RUN echo "Host server*\n \
 StrictHostKeyChecking no\n \
 UserKnownHostsFile=/dev/null" >> /root/.ssh/config

# MySQL 초기화 설정
RUN chown -R mysql:mysql /var/run/mysqld
RUN chmod 755 /var/run/mysqld

RUN sed -ri 's/^#.+port.+= 3306/port = 3306/' /etc/mysql/mysql.conf.d/mysqld.cnf
RUN sed -ri 's/^bind-address.+= 127.0.0.1/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

RUN service mysql start && \
    mysql -e "CREATE DATABASE IF NOT EXISTS neojune; \
    CREATE USER 'ubuntu'@'%' IDENTIFIED BY '1234'; \
    GRANT ALL PRIVILEGES ON *.* TO 'ubuntu'@'%' WITH GRANT OPTION; \
    FLUSH PRIVILEGES;"

RUN echo "[mysqld]\n \
    character-set-server=utf8\n \
    collation-server=utf8_general_ci\n \
    \n \
    [client]\n \
    default-character-set=utf8\n \
    \n \
    [mysql]\n \
    default-character-set=utf8" >> /etc/mysql/mysql.conf.d/mysqld.cnf
    

# nginx, SSH, MySQL 동시에 실행하기 위한 커맨드
CMD [ \
  "/bin/bash", "-c", \
  "service nginx start && service mysql start && /usr/sbin/sshd -D" \
]
