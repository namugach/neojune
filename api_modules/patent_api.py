import requests
import xml.etree.ElementTree as ET
import xmltodict
import os
from dotenv import load_dotenv
import time

def get_patent_info(service_key, applicant) -> list[dict] : 
    url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"

    page = 1
    result = []

    Flag = True
    while Flag:

        # 파라미터를 딕셔너리로 변환
        request_params = {
            'ServiceKey': service_key,
            'applicant': applicant,
            'pageNo': page,  # 기본 페이지 번호
            'numOfRows': 500,  # 최대 페이지당 건수
        }

        try:
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                
                # XML 파싱 -> dict
                api_result = xmltodict.parse(response.content)

                header = api_result['response']['header']
                body = api_result['response']['body']['items']
                count = api_result['response']['count']
                
                # data가 없을때의 에러처리 
                if not body:
                    Flag = False
                    continue

                items = body['item']
                for item in items:
                    result.append({
                        'index': item.get('indexNo'),
                        'title': item.get('inventionTitle'),
                        'applicant': item.get('applicationName'),
                        'appl_no': item.get('applicationNumber'),
                        'appl_date': item.get('applicationDate'),
                        'open_no' : item.get('openNumber'),
                        'open_date' : item.get('openDate'),
                        'reg_no': item.get('registerNumber'),
                        'reg_date': item.get('registerDate'),
                        'pub_no': item.get('publicationNumber'),
                        'pub_date': item.get('publicationDate'),
                        'legal_status_desc': item.get('registerStatus'),
                        'drawing': item.get('drawing'),

                    })
                page += 1

            else:
                print(f"HTTP 오류: {response.status_code}")
                Flag = False

        except requests.exceptions.Timeout:
            print(f"Timeout 오류 발생, page: {page}. 재시도 중...")
            time.sleep(2)  # 재시도하기 전에 일정 시간 대기
            continue    

        except Exception as e:
            print(f"오류 발생: {str(e)}, page: {page}" ) 
            Flag = False
    return result

# 사용 예시
if __name__ == "__main__":

    start = time.time()
    load_dotenv()

    service_key = os.getenv('SERVICE_KEY')

    # 미리 정의된 파라미터 리스트
    params_list = [
            '120160255942'
    ]

    # 각 파라미터로 API 호출
    for applicant in params_list:
        print(f"검색 조건: {applicant}")
        result = get_patent_info(service_key, applicant)

    print(len(result))
    print(time.time() - start)

    