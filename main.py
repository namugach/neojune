import asyncio,sys
from src.test import test

from src.test.save_to_xml import save_to_xml
# from src.test.xml_to_dict import xml_to_dict
# from src.test.dict_to_db import dict_to_db

# asyncio.run(save_to_xml.main('TB24_200'))
# xml_to_dict.main()
# dict_to_db.main()

test.run()
