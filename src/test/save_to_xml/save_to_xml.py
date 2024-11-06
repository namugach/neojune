import asyncio
from ...db.mysql import Mysql
from ...kipris.parsing.xml.KiprisXmlDataGenerator import KiprisXmlDataGenerator
from ...kipris.parsing.fetcher.KiprisPatentFetcher import KiprisPatentFetcher
from ...kipris.parsing.fetcher.KiprisDesignFetcher import KiprisDesignFetcher
from ...kipris.parsing.fetcher.KiprisTrademarkFetcher import KiprisTrademarkFetcher
from ...util import util

mysql = Mysql()



async def main(table_name):
    patent, design, trademark = None, None, None
    
    async def get_info():
        nonlocal patent, design, trademark  # 바깥 스코프 변수에 접근

        _applicant_numbers = mysql.get_all_app_no_and_applicant_id(table_name)

        # p3: 120080091393,  p23: 120070509242
        # _applicant_numbers = [[120070509242, 10],[120080091393, 20]]


        patent_fetcher = KiprisPatentFetcher(_applicant_numbers)
        patent = await patent_fetcher.get_infos()

        # design_fetcher = KiprisDesignFetcher(_applicant_numbers)
        # design = await design_fetcher.get_infos()

        # trademark_fetcher = KiprisTrademarkFetcher(_applicant_numbers)
        # trademark = await trademark_fetcher.get_infos()

    await util.get_run_time(get_info , f"전체 호출 완료: 3개 신청자 처리")
    
    

    async def save_xml():
        kipris_xml_dataGenerator = KiprisXmlDataGenerator(patent)
        kipris_xml_dataGenerator.apply()
        kipris_xml_dataGenerator.save("patent")

        # kipris_xml_dataGenerator.append_data_lists(design)
        # kipris_xml_dataGenerator.apply()
        # kipris_xml_dataGenerator.save("design")

        # kipris_xml_dataGenerator.append_data_lists(trademark)
        # kipris_xml_dataGenerator.apply()
        # kipris_xml_dataGenerator.save("trademark")

    await util.get_run_time(save_xml , "patent_data 저장 완료")






if __name__ == '__main__':
    asyncio.run(main())