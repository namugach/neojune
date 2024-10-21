import requests
import xml.etree.ElementTree as ET
import xmltodict
import os
from dotenv import load_dotenv
import time

load_dotenv()

def get_design_info(service_key, applicant) -> list[dict] : 
    url = "http://plus.kipris.or.kr/kipo-api/kipi/designInfoSearchService/getAdvancedSearch"

    page = 1
    result = []

    Flag = True
    while Flag:

        # 파라미터를 딕셔너리로 변환
        request_params = {
            'ServiceKey': service_key,
            'applicantName': applicant,
            'pageNo': page,  # 기본 페이지 번호
            'numOfRows': 500,  # 최대 페이지당 건수
            'open': 'true',
            'rejection': 'true',
            'destroy': 'true',
            'cancle': 'true',
            'notice': 'true',
            'registration': 'true',
            'invalid': 'true',
            'abandonment': 'true',
            'simi': 'true',
            'part': 'true',
            'etc': 'true',
            'sortSpec': 'applicationDate',
        }


        try:
            response = requests.get(url, params=request_params)

            if response.status_code == 200:
                
                # XML 파싱 -> dict
                api_result = xmltodict.parse(response.content)

                header = api_result['response']['header']
                body = api_result['response']['body']['items']
                count = api_result['response']['count']
                

                if body == None:
                    Flag = False
                    continue

                items = body['item']
                for item in items:
                    result.append({
                        'index': item.get('number'),
                        'title': item.get('articleName'),
                        'applicant': item.get('applicationName'),
                        'inventor' : item.get('inventorname'),
                        'agent' : item.get('agentName'),
                        'appl_no': item.get('applicationNumber'),
                        'appl_date': item.get('applicationDate'),
                        'open_no' : item.get('openNumber'),
                        'open_date' : item.get('openDate'),
                        'reg_no': item.get('registerNumber'),
                        'reg_date': item.get('registerDate'),
                        'pub_no': item.get('publicationNumber'),
                        'pub_date': item.get('publicationDate'),
                        'legal_status_desc': item.get('applicationStatus'),
                        'drawing': item.get('imagePath'),

                    })
                page += 1

            else:
                print(f"HTTP 오류: {response.status_code}")
                Flag = False

        except Exception as e:
            print(f"오류 발생: {str(e)}, page: {page}")
            Flag = False
    return result

# 사용 예시
if __name__ == "__main__":

    start = time.time()
    service_key = os.getenv('SERVICE_KEY')  # 실제 서비스 키로 변경

    # 미리 정의된 파라미터 리스트
    params_list = [
            '420100417169'
    ]

    # 각 파라미터로 API 호출
    for applicant in params_list:
        print(f"검색 조건: {applicant}")
        c = get_design_info(service_key, applicant)

    print(len(c))
    print(time.time() - start)

    