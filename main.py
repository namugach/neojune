from api_modules import design_api, patent_api, trademark_api
import os
from dotenv import load_dotenv
import time

load_dotenv()
service_key = os.getenv('SERVICE_KEY')

test_app = '120190582484'

start_time = time.time()

pa = patent_api.get_patent_info(service_key, test_app)
print(len(pa))
de = design_api.get_design_info(service_key, test_app)
print(len(de))
tr = trademark_api.get_trademark_info(service_key, test_app)
print(len(tr))

end_time = time.time()

print(end_time - start_time)
print(len(pa), len(de), len(tr))