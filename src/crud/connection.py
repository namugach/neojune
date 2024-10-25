import os

from dotenv import load_dotenv
import MySQLdb

# .env 파일에서 DB 연결 정보를 로드
load_dotenv()

def db_connect():
    # MySQL 연결 설정
    connection = MySQLdb.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME')
    )
    return connection
