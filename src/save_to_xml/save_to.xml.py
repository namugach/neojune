import asyncio
import aiohttp
from api_modules import design_api, patent_api, trademark_api
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import xml.etree.ElementTree as ET
from crud import save_xml_db_crud

# # XML 저장 함수
def save_data_as_xml(data_dict, file_name):
    root = ET.Element("responseData")

    for applicant_id, data in data_dict.items():
        response_elem = ET.SubElement(root, "response")

        # <applicant> 태그 추가
        applicant_tag = ET.SubElement(response_elem, "applicant_id")
        applicant_tag.text = str(applicant_id)

        # <header> 태그 추가 (결과 코드와 메시지를 포함)
        header = ET.SubElement(response_elem, "header")
        ET.SubElement(header, "resultCode")
        ET.SubElement(header, "resultMsg")

        # <body> 태그 추가 및 그 안에 <items> 데이터 삽입
        body = ET.SubElement(response_elem, "body")
        items_elem = ET.SubElement(body, "items")
        # data 내부에 있는 XML 콘텐츠를 <items>에 추가
        for content in data:
            original_data = ET.fromstring(content)

            # 기존 XML에서 <items> 내부 태그들만 추가
            items = original_data.find(".//items")
            if items is not None:
                for elem in items:
                    items_elem.append(elem)

    # XML 파일로 저장
    tree = ET.ElementTree(root)
    file_path = f"src/save_to_xml/output/{file_name}.xml"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    print(f"{file_path} 저장 완료")




async def fetch_all_info(service_key, app_no, applicant_id, session, semaphore, pa_dict, de_dict, tr_dict):
    async with semaphore:
        result_patent = await patent_api.get_patent_info(service_key, app_no, session)
        result_design = await design_api.get_design_info(service_key, app_no, session)
        result_trademark = await trademark_api.get_trademark_info(service_key, app_no, session)

        pa_dict[applicant_id] = result_patent
        de_dict[applicant_id] = result_design
        tr_dict[applicant_id] = result_trademark

        print(f"{app_no} 총 데이터 수 : {len(pa_dict) +len(de_dict) + len(tr_dict) }")

async def main():
    load_dotenv()
    service_key = os.getenv('SERVICE_KEY')
    semaphore = asyncio.Semaphore(50)
    limit = 1
    test_apps = save_xml_db_crud.fetch_data_from_db('TB24_200',['app_no', 'applicant_id'],limit)
      
    
    start_time = time.time()

    pa_dict, de_dict, tr_dict = {}, {}, {}

    async with aiohttp.ClientSession() as session:
        tasks = []
        for app_no, applicant_id in test_apps:
            task = asyncio.create_task(fetch_all_info(service_key, app_no, applicant_id, session, semaphore, pa_dict, de_dict, tr_dict))
            tasks.append(task)
        await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"전체 호출 완료: {len(test_apps)}개 신청자 처리, 총 걸린 시간 : {elapsed_time:.2f}초")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    start = time.time()
    # data 부분만 XML 파일로 저장
    save_data_as_xml(pa_dict, f"patent_data_{timestamp}")
    save_data_as_xml(de_dict, f"design_data_{timestamp}")
    save_data_as_xml(tr_dict, f"trademark_data_{timestamp}")
    print("모든 데이터를 XML 파일로 저장 완료")
    end = time.time()
    elapsed_time = end - start
    print(f"걸린 시간: {elapsed_time}")
if __name__ == '__main__':
    asyncio.run(main())