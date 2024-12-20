from ...core.convert.KiprisXmlMapper import KiprisXmlMapper

class KiprisTrademarkXmlMapper(KiprisXmlMapper):
    def __init__(self):
        super().__init__()
        self.ipr_code = "ApplicationNumber"
        self.title = "Title"
        self.serial_no = "SerialNumber"
        self.applicant = "ApplicantName"
        self.appl_no = "ApplicationNumber"
        self.appl_date = "ApplicationDate"
        self.pub_num = "PublicNumber"
        self.pub_date = "PublicDate"
        self.legal_status_desc = "ApplicationStatus"
        self.image_path = "ThumbnailPath"

        self.agent = "AgentName"
        self.priority_no ="PriorityClaimNumber"
        self.priority_date = "PriorityClaimDate"