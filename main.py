from api_modules import design_api, patent_api, trademark_api
import os
from dotenv import load_dotenv
import time

load_dotenv()
service_key = os.getenv('SERVICE_KEY')

test_apps = ['120140558200', '120090359981', '120100466769']

start_time = time.time()

for app in test_apps:
    pa = patent_api.get_patent_info(service_key, app)
    de = design_api.get_design_info(service_key, app)
    tr = trademark_api.get_trademark_info(service_key, app)

    print("총 데이터 수 : ", len(pa) + len(de) + len(tr))

end_time = time.time()

print("총 걸린 시간 : ",  end_time - start_time)

# print("총 데이터 수 : ", len(pa) + len(de) + len(tr))
# print("특/실 데이터 수 : " , len(pa))
# print("디자인 데이터 수 : ", len(de))
# print("상표 데이터 수 : ", len(tr))