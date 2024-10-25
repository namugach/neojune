import os
import sys

import time
from dotenv import load_dotenv
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crud.connection import db_connect
from crud.db_crud import * 
from api_modules.biz_api import *


start = time.time()


connection = db_connect()
cursor = connection.cursor()
service_key = os.getenv('SERVICE_KEY')

page = 1
total_data = []
page_size=50

while True:
    rows = fetch_data_by_page(cursor, 'TB24_100', page=page, page_size=page_size)
    if rows:
        result = asyncio.run(process_applicants(service_key,rows))
        total_data.extend(result)
        page += 1
    else:
        break


insert_data_to_db(cursor, 'TB24_200',total_data, True )
connection.commit()

cursor.close()
connection.close()

end = time.time()

print(end - start)