import asyncio
import aiohttp
from api_modules import design_api, patent_api, trademark_api
import os
from dotenv import load_dotenv
import time
import MySQLdb
import json
from datetime import datetime  # 현재 시간 사용을 위한 모듈 추가

async def fetch_all_info(service_key, app, session, semaphore, pa_dict, de_dict, tr_dict):
    async with semaphore:
        tasks = [
            patent_api.get_patent_info(service_key, app, session),
            design_api.get_design_info(service_key, app, session),
            trademark_api.get_trademark_info(service_key, app, session),
        ]

        results = await asyncio.gather(*tasks)

        # data 부분만 추출하여 딕셔너리에 저장
        pa_dict[app], de_dict[app], tr_dict[app] = results

        # 총 데이터 수 기록
        total_count = sum(len(data) for data in results)
        print(f"{app} 총 데이터 수 : {total_count}")

# DB에서 app_no 목록을 가져오는 함수
def get_app_nos_from_db(limit=None):
    connection = db_connect()
    cursor = connection.cursor()

    query = "SELECT app_no FROM TB24_200"
    if limit is not None:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    app_nos = cursor.fetchall()
    cursor.close()
    connection.close()

    return [app_no[0] for app_no in app_nos]

# MySQL 연결 함수
def db_connect():
    connection = MySQLdb.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME')
    )
    return connection

async def main():
    load_dotenv()
    service_key = os.getenv('SERVICE_KEY')
    semaphore = asyncio.Semaphore(16)  # 동시 요청 수 조정
    limit = 50  # 테스트용 요청 개수

    test_apps = get_app_nos_from_db(limit)
    start_time = time.time()

    # 결과 저장용 딕셔너리 초기화
    pa_dict, de_dict, tr_dict = {}, {}, {}

    async with aiohttp.ClientSession() as session:
        # 모든 앱의 정보를 비동기로 가져와 딕셔너리에 저장
        tasks = []
        for app in test_apps:
            task = fetch_all_info(service_key, app, session, semaphore, pa_dict, de_dict, tr_dict)
            tasks.append(task)
        # 모든 fetch 작업 완료 대기
        await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"전체 호출 완료: {len(test_apps)}개 신청자 처리, 총 걸린 시간 : {elapsed_time:.2f}초")

    # 현재 시간 문자열 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 모든 데이터를 한 번에 JSON 파일로 저장 (파일 이름에 현재 시간 포함)
    with open(f"./save_to_json/patent_data_{timestamp}.json", "w") as pa_file, \
         open(f"./save_to_json/design_data_{timestamp}.json", "w") as de_file, \
         open(f"./save_to_json/trademark_data_{timestamp}.json", "w") as tr_file:
        json.dump(pa_dict, pa_file, ensure_ascii=False, indent=4)
        json.dump(de_dict, de_file, ensure_ascii=False, indent=4)
        json.dump(tr_dict, tr_file, ensure_ascii=False, indent=4)

    print("모든 데이터를 JSON 파일로 저장 완료")

if __name__ == '__main__':
    asyncio.run(main())
