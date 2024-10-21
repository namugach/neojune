from api_modules import design_api, patent_api, trademark_api
import os
from dotenv import load_dotenv
import time

load_dotenv()
service_key = os.getenv('SERVICE_KEY')

test_app = '120140558200'

start_time = time.time()

pa = patent_api.get_patent_info(service_key, test_app)
de = design_api.get_design_info(service_key, test_app)

# tr = trademark_api.get_trademark_info(service_key, test_app)
# print(len(tr))

end_time = time.time()

print("총 걸린 시간 : ",  end_time - start_time)
print("총 데이터 수 : ", len(pa) + len(de))
print("특/실 데이터 수 : " , len(pa))
print("디자인 데이터 수 : ", len(de))