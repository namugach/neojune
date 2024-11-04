import os, asyncio, aiohttp
from lxml import etree
from dotenv import load_dotenv
from .KiprisFetchData import KiprisFetchData
from .KiprisParams import KiprisParams
load_dotenv()
service_key = os.getenv('SERVICE_KEY')



class KiprisApplicantInfoFetcher:
    def __init__(self, url:str, param:KiprisParams):
        self.result = []
        self.url = url
        self.max_pages = 0
        self.success_count = 0
        self.fail_count = 0
        self.session = None
        self.params = param

    async def open_session(self):
        """ClientSession을 열어서 여러 요청에서 공유"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        """ClientSession을 닫음"""
        if self.session:
            await self.session.close()
            self.session = None

    async def _fetch_content(self, page: int) -> str:
        """API 호출 후 페이지 내용 반환"""
        self.params.docsStart = page
        async with self.session.get(self.url, params=self.params.get_dict(), timeout=20) as response:
            return await response.text()


    
    def __get_total_count(self, content: str) -> int:
        """lxml을 사용하여 XML 응답에서 totalCount 또는 TotalSearchCount 값을 추출"""
        root = etree.fromstring(content.encode("utf-8"))

        for tag in ["totalCount", "TotalSearchCount"]:
            element = root.find(f".//{tag}")
            if element is not None and element.text.isdigit():
                return int(element.text)

        print("totalCount와 TotalSearchCount를 찾을 수 없습니다.")
        return 0

    def _calculate_max_pages(self, total_count: int):
        """총 페이지 수 계산"""
        self.max_pages = (total_count // self.params.docsCount) + (1 if total_count % self.params.docsCount else 0)

    async def _handle_response(self, page: int) -> bool:
        """응답 처리 및 성공 여부 반환"""
        try:
            content = await self._fetch_content(page)
            if page == 1:  # 첫 페이지는 totalCount 추출
                total_count = self.__get_total_count(content)
                if total_count == -1:
                    return False # totalCount 추출 실패시 함수 종료
                self._calculate_max_pages(total_count)
                print(f"총 검색 건수: {total_count}, 총 페이지 수: {self.max_pages}")
            self.result.append(content)
            self.success_count += 1
            print(f"{self.params.app_no} 페이지 {page} 호출 성공")
            return True
        except asyncio.TimeoutError:
            print(f"{self.params.app_no} 페이지 {page}에서 시간 초과 오류")
            self.fail_count += 1
            return False
        except Exception as e:
            print(f"{self.params.app_no} 페이지 {page}에서 오류: {e}")
            self.fail_count += 1
            return False

    async def _increment_page(self, page: int) -> int:
        """페이지 증가 및 지연 적용"""
        # await asyncio.sleep(0.02)
        return page + 1

    async def fetch_initial(self):
        """첫 요청으로 totalCount 추출 및 첫 페이지 결과 저장"""
        success = await self._handle_response(1)
        if not success:
            print("첫 페이지 요청 실패")


    async def fetch_pages(self):
        # 동시에 최대 10개의 페이지 요청을 보내도록 제한하기 위해 세마포어 사용
        semaphore = asyncio.Semaphore(10)
        
        tasks = []
        # 페이지 번호 2부터 self.max_pages까지 반복
        for page in range(2, self.max_pages + 1):
            # _handle_response 메서드를 호출하고, 각 요청을 tasks 리스트에 추가
            task = self._handle_response(page)
            tasks.append(task)
        
        # 세마포어를 사용하여 동시에 최대 10개의 요청만 보내도록 asyncio.gather로 모은 모든 task를 실행
        async with semaphore:
            await asyncio.gather(*tasks)

        # 최종 결과 출력
        total_requests = self.success_count + self.fail_count
        print(f"총 호출 횟수: {total_requests}, 성공: {self.success_count}, 실패: {self.fail_count}")


    async def get_info(self) -> KiprisFetchData:
        await self.open_session()  # 세션 열기
        await self.fetch_initial()
        await self.fetch_pages()
        await self.close_session()  # 세션 닫기
        
        return KiprisFetchData(self.params.app_no, self.params.applicant_id, self.result)



async def main():
    applicant = "120140558200"
    kipris_applicant_info_fetcher = KiprisApplicantInfoFetcher()
    async with aiohttp.ClientSession() as session:
        result = await kipris_applicant_info_fetcher.get_info(applicant, session)

if __name__ == "__main__":
    asyncio.run(main())
