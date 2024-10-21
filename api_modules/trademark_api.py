import requests
import xml.etree.ElementTree as ET
import xmltodict
import os
from dotenv import load_dotenv
import time

load_dotenv()

def get_trademark_info(service_key, applicant) -> list[dict] : 
    url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch"

    page = 1
    result = []

    Flag = True
    while Flag:

        # 파라미터를 딕셔너리로 변환
        request_params = {
            'ServiceKey': service_key,
            'applicantName': applicant,
            'application': 'true',
            'registration': 'true',
            'refused': 'true',
            'expiration': 'true',
            'withdrawal': 'true',
            'publication': 'true',
            'cancel': 'true',
            'abandonment': 'true',
            'character': 'true',
            'figure': 'true',
            'compositionCharacter': 'true',
            'figureComposition': 'true',
            'sound': 'true',
            'fragrance': 'true',
            'color': 'true',
            'dimension': 'true',
            'colorMixed': 'true',
            'hologram': 'true',
            'motion': 'true',
            'visual': 'true',
            'invisible': 'true',
            'pageNo': page,  # 기본 페이지 번호
            'numOfRows': 500,  # 기본 페이지당 건수
            'sortSpec': 'applicationDate',
        }


        try:
            response = requests.get(url, params=request_params)

                # 응답이 비어있는지 확인
            # if not response_content.strip():
            #     print("응답이 비어 있습니다.")
            #     return

            if response.status_code == 200:
                # XML 파싱 -> dict
                api_result = xmltodict.parse(response.content)

                header = api_result['response']['header']
                body = api_result['response']['body']['items']
                count = api_result['response']['count']
                items = body['item']

                if body == None:
                    Flag = False
                    continue

                page += 1

                for item in items:
                    result.append({
                        'index': item.get('indexNo'),
                        'title': item.get('title'),
                        'applicant': item.get('applicationName'),
                        'agent' : item.get('agentName'),
                        'appl_no': item.get('applicationNumber'),
                        'appl_date': item.get('applicationDate'),
                        'reg_no': item.get('registerNumber'),
                        'reg_date': item.get('registerDate'),
                        'pub_no': item.get('publicationNumber'),
                        'pub_date': item.get('publicationDate'),
                        'legal_status_desc': item.get('applicationStatus'),
                        'drawing': item.get('drawing'),

                    })

            else:
                print(f"HTTP 오류: {response.status_code}")
                Flag = False

        except Exception as e:
            print(f"오류 발생: {str(e)}")
            print(response)
            Flag = False
    return result

# 사용 예시
if __name__ == "__main__":

    start = time.time()
    service_key = os.getenv('SERVICE_KEY')  # 실제 서비스 키로 변경

    # 미리 정의된 파라미터 리스트
    params_list = [
            '119980005233'
    ]

    # 각 파라미터로 API 호출
    for applicant in params_list:
        print(f"검색 조건: {applicant}")
        c = get_trademark_info(service_key, applicant)

    print(len(c))
    print(time.time() - start)

    