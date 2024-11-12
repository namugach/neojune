from ...core.parsing.KiprisChangeInfoFetcher import KiprisChangeInfoFetcher
from ...core.parsing.KiprisParamChange import KiprisParamChange

class KiprisTrademarkChangeFetcher(KiprisChangeInfoFetcher):
    def __init__(self):
        self.url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getChangeInfoSearch"
        self.params = KiprisParamChange().set_params()
        super().__init__(self.url, self.params)