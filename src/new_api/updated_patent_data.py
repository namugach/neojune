import os, asyncio, aiohttp
from dotenv import load_dotenv
from datetime import datetime
import time

async def get_patent_info(service_key, application_number, session, semaphore) -> dict:
    url = "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/applicationNumberSearchInfo"
    result = []
    success_count = 0
    fail_count = 0
    docs_count = 500  # 페이지당 최대 결과 수

    # 첫 요청으로 총 항목 수 확인
    request_params = {
        'accessKey': service_key,
        'applicationNumber': application_number,
        'docsStart': 1,
        'docsCount': docs_count,
        'patent': 'true',
        'utility': 'true',
        'lastvalue': '',
    }

    async with session.get(url, params=request_params, timeout=10) as response:
        content = await response.text()
        try:
            # 문자열 검색으로 totalCount 추출
            start = content.find("<TotalSearchCount>") + len("<TotalSearchCount>")
            end = content.find("</TotalSearchCount>")
            total_count = int(content[start:end].strip())
            max_pages = (total_count // docs_count) + (1 if total_count % docs_count else 0)
            print(f"총 검색 건수: {total_count}, 총 페이지 수: {max_pages}")
            # totalCount가 0이 아닐 경우에만 결과를 추가
            if total_count > 0:
                result.append(content)
            else:
                print(f"{application_number}의 검색 결과가 없습니다.")
                return {application_number: "No results found"}
            success_count += 1
        except ValueError:
            print("totalCount를 찾을 수 없습니다.")
            return {application_number: result}

    # 전체 페이지 순회
    page = 2
    while page <= max_pages:
        request_params['docsStart'] = page
        try:
            async with session.get(url, params=request_params, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    print(f"{application_number} 페이지 {page} 호출 성공")
                    result.append(content)
                    success_count += 1
                    page += 1
                    # 요청을 보낸 후 0.02초 지연
                    await asyncio.sleep(0.02)
                else:
                    print(f"{application_number} 페이지 {page} HTTP 오류: {response.status}")
                    fail_count += 1
                    break
        except asyncio.TimeoutError:
            print(f"{application_number} 페이지 {page}에서 시간 초과 오류, 재시도 중...")
            await asyncio.sleep(1)
            fail_count += 1
            continue
        except Exception as e:
            print(f"{application_number} 페이지 {page}에서 오류: {e}")
            fail_count += 1
            break

    if result:
        return {application_number: result}
    else:
        return {application_number: "No results found"}

async def main():
    service_key = os.getenv('SERVICE_KEY')
    limit = 200  # 테스트용 요청 개수
    
    test_apps = [{'2020040031672': 4719}, {'2020210000007': 1696}, {'1020220021103': 6841}]
    test_apps = [{'1020220175029': 1}, {'1020230022997': 302}, {'1020220163314': 321}, {'1020140035677': 275}] # 대학
    start_time = time.time()
    
    # 결과 저장용 딕셔너리 초기화
    de_dict = {}
    semaphore = asyncio.Semaphore(20)

    async with aiohttp.ClientSession() as session:
        # 모든 앱의 정보를 비동기로 가져와 딕셔너리에 저장
        tasks = []
        for app in test_apps:
            for application_number, code in app.items():
                await asyncio.sleep(0.02)
                task = asyncio.create_task(get_patent_info(service_key, application_number, session, semaphore))
                tasks.append(task)

        # 모든 fetch 작업 완료 대기
        de_dict = await asyncio.gather(*tasks)
    

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"전체 호출 완료: {len(test_apps)}개 신청자 처리, 총 걸린 시간 : {elapsed_time:.2f}초")
    print(de_dict)


# asyncio 이벤트 루프 실행
if __name__ == "__main__":
    asyncio.run(main())