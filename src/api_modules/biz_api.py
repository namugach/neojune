import requests
import xmltodict
import os
import logging
from dotenv import load_dotenv
import time
import aiohttp
import asyncio
import traceback

## 사업자 등록번호 -> 특허 고객번호
async def get_applicant_no(service_key, applicant_info: tuple) -> dict:
    url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV3"
    company_seq, biz_no, corp_no, biz_type, company_name = applicant_info

    request_params = {
        'accessKey': service_key,
        'BusinessRegistrationNumber': biz_no
    }

    result = []
    retries = 3  # 재시도 횟수

    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=request_params, timeout=10) as response:
                    if response.status == 200:
                        api_result = xmltodict.parse(await response.text())

                        header = api_result['response']['header']
                        body = api_result['response']['body']['items']

                        if body is None:
                            return None

                        bs_info = body.get('corpBsApplicantInfo')

                        if type(bs_info) != list :
                            bs_info = [bs_info]

                        for info in bs_info:
                            if info.get('CorporationNumber'): # 법인번호가 있는 데이터만 저장 (법인만 저장)
                                result.append({
                                    'app_no': info['ApplicantNumber'],
                                    'compay_name': info['ApplicantName'],
                                    'corp_no': info['CorporationNumber'],
                                    'biz_no': info['BusinessRegistrationNumber'],
                                    'company_seq': company_seq
                                })

                        return result
                    else:
                        print(f"HTTP 오류: {response.status}")
                        break  # HTTP 오류가 발생하면 재시도하지 않음

        except asyncio.TimeoutError:
            print("Timeout 오류 발생")
            await asyncio.sleep(2)  # 재시도하기 전에 일정 시간 대기

        except Exception as e:
            print(f"오류 발생: {str(e)}")
            print(traceback.format_exc()) 
            print(body.get('corpBsApplicantInfo') if body else 'No body available')
            print(applicant_info)

        # 재시도 대기 시간
        if attempt < retries - 1:
            print(f"재시도 {attempt + 1}/{retries}...")
            await asyncio.sleep(2)  # 재시도 간 대기

    return result

# 여러 회사 정보를 비동기로 처리하는 함수
async def process_applicants(service_key, applicant_info_list: list):
    tasks = []
    for applicant_info in applicant_info_list:
        tasks.append(get_applicant_no(service_key, applicant_info))

    results = await asyncio.gather(*tasks)

    total_result = []

    for result in results:
        if result :
            total_result.extend(result)

    return total_result

if __name__ == "__main__":
    load_dotenv()

    service_key = os.getenv('SERVICE_KEY')
    result = asyncio.run(process_applicants(service_key, [(1, '220-88-87953', '110111-5518240', '법인', '(주)준소프트웨어')]))
    print(result)