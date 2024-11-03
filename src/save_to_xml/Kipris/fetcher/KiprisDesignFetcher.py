from ..core.KiprisFetcher import KiprisFetcher
from ..params.KiprisDesignPrams import KiprisDesignPrams

class KiprisDesignFetcher(KiprisFetcher):
    def __init__(self, params:list[KiprisDesignPrams]):
        super().__init__(params=params)
        self.url = "http://plus.kipris.or.kr/openapi/rest/designInfoSearchService/applicantNameSearchInfo"
        self.set_params(params)
        
    def set_params(self, params_list:list[str|int]):
        super().set_params(params_list, KiprisDesignPrams)