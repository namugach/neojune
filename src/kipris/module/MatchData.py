from .core.KiprisObject import KiprisObject

class MatchData(KiprisObject):
    def __init__(self):
        """
        KIPRIS API에서 반환된 다양한 지식재산권 데이터를 표준화된 형식으로 변환하는 역할을 합니다.
        이 클래스는 특허, 상표, 디자인 등 여러 종류의 지식재산권 정보에 대한 필드를 매핑하고,
        API 응답 데이터를 일관된 구조로 변환하여 쉽게 처리할 수 있게 해줍니다.
        주요 기능으로는 데이터 필드 매핑, 단일 항목 변환, 여러 항목 일괄 변환 등이 있습니다.
        """
        super().__init__()
        self.index = ['number', 'indexNo'] # 인덱스 또는 번호
        self.title = ['articleName', 'inventionTitle', 'title'] # 발명의 제목 또는 상품의 명칭
        self.applicant = ['applicationName'] # 출원인
        self.inventor = ['inventorname'] # 발명자
        self.agent = ['agentName'] # 대리인
        self.appl_no = ['applicationNumber'] # 출원 번호
        self.appl_date = ['applicationDate'] # 출원 일자
        self.open_no = ['openNumber'] # 공개 번호
        self.open_date = ['openDate'] # 공개 일자
        self.reg_no = ['registerNumber'] # 등록 번호
        self.reg_date = ['registerDate'] # 등록 일자
        self.pub_no = ['publicationNumber'] # 공고 번호
        self.pub_date = ['publicationDate'] # 공고 일자
        self.legal_status_desc = ['applicationStatus', 'registerStatus'] # 법적 상태 설명
        self.drawing = ['imagePath', 'drawing'] # 도면 또는 이미지 경로
        self.ipcNumber = ["ipcNumber"] # 국제 특허 분류

    def get_all_keys(arg):
        """
        객체의 모든 속성 이름을 리스트로 반환하는 함수
        
        이 함수는 주어진 객체의 모든 속성 중에서 메서드가 아니고
        언더스코어로 시작하지 않는 속성 이름만을 추출하여 리스트로 반환합니다.
        
        :param arg: 속성을 추출할 객체
        :return: 객체의 유효한 속성 이름들의 리스트
        """
        return [attr for attr in dir(arg) if not callable(getattr(arg, attr)) and not attr.startswith("__")]
    
    def get_convert_data(self, items: dict) -> dict:
        """
        단일 아이템 딕셔너리를 MatchData 클래스의 구조에 맞게 변환하는 함수
        
        :param items: 변환할 원본 데이터 딕셔너리
        :return: MatchData 구조에 맞게 변환된 데이터 딕셔너리
        """
        data = {}
        for key in self.get_all_keys():
            data[key] = {}
            for k in getattr(self, key):
                if k in items:
                    data[key] = items[k]
        return data

    def get_convert_datas(self, items: list | dict) -> list:
        """
        단일 아이템 또는 아이템 리스트를 MatchData 구조로 변환하는 함수
        
        :param items: 변환할 원본 데이터 (딕셔너리 또는 딕셔너리 리스트)
        :return: MatchData 구조로 변환된 데이터 리스트
        """
        res = []
        if type(items) == dict:
            res.append(self.get_convert_data(items))
        else:
            for item in items:
                res.append(self.get_convert_data(item))
        return res
