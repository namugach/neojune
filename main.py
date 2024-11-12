from src.test import test


# test.run()
import asyncio

from src.test.save_to_xml.save_to_xml import daliy
asyncio.run(daliy())
exit()


####### new api 실험
import asyncio
from src.new_api.change_data import fetch_content
from src.new_api.applicantNumber import get_applicantNumber
from src.util.util import get_timestamp
from src.db.mysql import Mysql
from tqdm import tqdm

base_url = "http://plus.kipris.or.kr/kipo-api/kipi/{type}/getChangeInfoSearch"

url_dict = {
    "patent" : "patUtiModInfoSearchSevice",
    "design" : "designInfoSearchService",
    "trademark" : "trademarkInfoSearchService"
}

from time import time

start = time()

url = base_url.format(type = url_dict['patent'])
applicationNumber_list = asyncio.run(fetch_content(url))

print("변동정보 추출" , time() - start )

start = time()
base_url = "http://plus.kipris.or.kr/openapi/rest/{type}"

url_type = {
    "patent" : "patUtiModInfoSearchSevice/patentApplicantInfo",
    "design" : "designInfoSearchService/getApplicantInfo",
    "trademark" : "trademarkInfoSearchService/applicationNumberSearchInfo"
}


####### 출원번호 -> 특허 고객 번호 알아내기 
url = base_url.format(type = url_type['patent'])
datas = asyncio.run(get_applicantNumber(url, applicationNumber_list))
print("변동 출원번호로 특허고객 번호 알아내기 ", time() - start )
# print(len(result))

# asyncio.run(get_applicantNumber(url, applicationNumber_list[:2]))
# execute_with_time("get_applicantNumber", )


# data = "1020190149218|1020230020170|1020237020473|1020217004391|1020230067853|1020200182634|1020220148184|1020200077407|1020190089039|1020200189102|1020190079391|1020210134565|1020150186330|1020210030916|1020217041006|1020190029970|1020230113669|1020220133550|1020190058031|1020220002516|1020200099333|1020110114621|1020210190381|1020220118987|1020180001429|1020120000269|1020230128926|1020120086214|1020150146066|1020220067560|1020247036215|1020240061883|1020160168819|1020227001401|1020237017596|1020220184067|1020210130007|1020200125786|1020237031774|1020160155638|1020247022441|1020200175884|2020220002020|1020190011026|1020190144018|1020230058456|1020230056968|1020200129171|1020220083131|1020230003430|1020190133241|1020237008788|1020230158511|1020230056965|1020170049950|1020237013304|1020200155851|1020237031356|1020220095590|1020227014906|1020227041622|1020220077572|1020230124867|1020220184102|1020227026492|1020200184761|1020220057773|1020247036600|1020230044071|2020230000867|1020227035916|1020247035601|1020200010772|1020247032593|1020180003458|1020247030996|1020247035512|1020220162870|1020220163892|1020230118668|1020160182140|1020190116149|1020210085916|1020230001992|1020237002202|1020190133204|1020130152393|1020227017210|1020230092285|1020190016378|1020220175860|1020220107066|1020220018705|1020160057528|1020200167822|1020230192224|1020190020952|1020247031088|1020200141149|1020230009334|1020210155157|1020180126055|1020230057314|1020160008734|1020237025530|2019960010890|1020220122352|1020190107919|1020247033019|1020110074679|1020247033570|1020230086822|1020220161170|1020230058705|1020210092548|1020150032136|1020180017556|1020240129352|1020207024755|1020217014174|1020230058733|1020180167713|1020247027843|1020180133024|1020220113073|1020170112647|1020247021830|1020210065454|1020150012613|1020230050712|1020190009746|1020140193106|1020230005422|1020230025807|1020230057416|1020210155054|1020180172481|1020240000550|1020240057317|1020240097917|1020130013634|1020190164748|1020240061887|1020210019095|1020187007796|1020100049160|1020220087092|1020120154654|1020227007913|1020220117133|1020210177901|1020120059311|1020240152410|1020227016062|1020180128777|1020230169230|1020227021337|1020190012660|1020200045096|1020220057892|1020200088912|1020220148478|1020170156124|1020187010753|1020220113190|1020110092290|1020247033455|1020217033777|1020230049467|1020190161440|1020230058687|1020190047388|1020210094011|1020187002186|1020230057498|1020237039627|1020200047970|1020210121487|1020220149281|1020150017346|1020230057266|1020227010509|1020230053211|1020160023709|1020227017196|1020237045177|1020180013347|1020220161942|1020217026710|1020150067894|1020200108247|1020110059402|1020220092548|1020230057509|1020227025233|1020210013185|1020220164183|1020160015876|1020190165700|1020090135090|1020190169321|1020227043548|1020170078628|1020200075318|1020237034755|1020220001139|1020190145661|1020247035085|1020210128035|1020237019428|1020120008723|1020230058682|1020150067895|1020200159090|1020247036547|1020210001173|1020080085658|1020210160197|1020140022755|1020200156163|1020247036762|1020220113603|1020170022364|1020220077377|1020220144408|1020200055982|1020220173329|1020220008793|1020230056836|1020230016341|1020220102918|1020240129353|1020230058805|1020160155919|1020180135705|1020210069812|1020210160086|1020140111380|1020190032660|1020230058300|1020180051199|1020230058817|1020220157615|1020230004009|1020230021222|1020237002614|1020237016918|1020220136868|1020220112539|1020210175360|1020210178016|1020230095461|1020190023102|1020247034031|1020210136945|1020190084744|1020200045785|1020240152002|1020210029711|1020200146667|1020160025465|1020247023644|1020210176334|1020230052337|1020237022427|1020227041271|1020210053540|1020220158743|1020140195339|1020217016308|1020247031107|1020220133561|1020220101228|1020200015458|1020230174661|1020150036884|1020227027931|1020247036130|1020247034062|1020230058501|1020200073314|1020220030496|1020220048287|1020227024846|1020220189706|1020180013348|1020230057688|1020180144995|1020220054558|1020240072691|1020237020597|1020220151704|1020170152881|1020160013189|1020140143238|1020247033421|1020220106006|1020220079543|1020210192497|1020230182768|1020230058373|1020237000312|1020190088883|1020180093043|1020190120960|1020217013568|1020210178236|1020230057724|1020220091546|1020237009442|1020200121287|1020227020582|1020230031750|1020247032491|1020210175822|1020230057423|1020180171195|1020190009396|1020240129359|1020187004480|1020200122310|1020217004891|1020237018587|1020217014686|1020207036232|1020220024869|1020230102612|1020190137732|1020220133445|1020170152714|1020237017134|1020210154200|1020220130373|1020220189245|1020217036298|1020247030781|1020210170766|1020110083430|1020240020599|1020100123080|1020190090789|1020210130276|1020210127593|1020200010044|1020220095845|1020157020489|1020220110713|1020230056997|1020207030131|1020230057523|1020240058300|1020090097053|1020150018774|1020220115539|1020120141010|1020240009965|1020180003439|1020220105904|1020230058112|1020150181536|1020240148843|1020230054807|1020190024275|1020247032545|1020227031678|1020240058686|1020237020577|1020237017020|1020230045213|1020150169416|1020230057690|1020180157133|1020180114073|1020247020504|1020220075784|1020190071624|1020220145733|1020210074045|1020190153797|1020220173338|1020220150872|1020210020210|1020227015818|1020220126196|1020230012567|1020237029142|1020227044278|1020190094023|1020207018636|1020170134200|1020247036037|1020190020281|1019980033983|1020230057508|1020220017770|1020220163684|1020227015679|1020230027546|1020217001244|1020220040153|1020210181713|1020190108003|1020220168787|1020220030572|1020230058523|1020240150927|1020090134982|1020230025357|1020220187445|1020160157634|1020220138885|1020220026836|1020230172439|1020220029552|1020220156592|1020240106056|1020200126373|1020200094985|1020190041649|2020090010097|1020200076697|1020160153268|1020210110170|2020160004401|1020230057254|1020217034773|1020247034239|1020247028403|1020217043053|1020180023371|1020230027384|1020247034687|1020180135136|1020220183557|1020207023908|1020220108876|1020210161229|1020220049654|1020247035514|1020230014961|1020217026283|1020220076824|1020120032244|2019940003111|1020230012597|1020240044504|1020230018300|1020220148444|1020220189708|2019910024427|1020237007857|1020240147760|1020210173976|1020190179800|1020150185135|1020247034636|1020220115600|1020230056949|1020230099238|1020247032646|1020000070396|1020207013660|1020230194013|1020180170449|1020247034638|2019960026275|1020247030856|1020227040082|1020247034760|1020230057025|1020230178708|1020170174258|1020140193105|1020100101179|1020200015770|1020120017527|1020140056216|1020230056792|1020200115598|1020240001326|1020227000182|1020227020279|1020220067865|1020190146923|1020247035800|1020220021510|1020240058514|1020190053995|1020230030013|1020210170404|1020200097327|1020220097987|1020200016537|1020230058685|1020227001169|1020190120116|1020200037435|1020210012483|1020210178710|1020200177685|1020140130108|1020220161864|1020200034274|1020217033036|1020200117747|1020130025897|1020190019571|1020247036056|1020200042266|1020220135675|1020220085532|1020190130121|1020220034115|1020230058354|1020090033141|1020237003775|1020227011279|1020220086282|1020220002643|1020190128238|1020200004102|1020200154883|1020170019769|1020180116095|1020230057352|1020200016096|1020150185148|1020140012875|1020170021434|2019930011131|1020200075973|1020160006760|1020200079260|1020220162993|1020110005252|1020240114190|2020220002283|1020200106266|1020190022272|1020197036968|1020210017927|1020210141197|1020207018967|1020170104955|1020247033198|1020220182279|1020130002263|1020220095234|1020180062830|1020220189652|1020240029623|1020207012972|1020220002254|1020220100470|1020217019507|1020210178855|1020200037696|1020200133211|1020187018512|1020200097575|1020190136696|1020130152032|1020247031652|1020210138322|1020190178653|1020200038619|1020220162909|1020220016712|1020230057402|1020210131497|1020200015460|1020237009109|1020220187219|1020220119120|1020190008900|1020220109791|1020220166838|1020170059880|1020230058267|1020230012806|1020200017777|1020220115736|1020217038517|1020237043339|1020220062894|1020230024406|1020210004368|1020210117272|1020240047755|1020190096433|1020247034861|1020227019023|1020230057539|1020190127497|1020210084072|1020190082226|1020230058670|1020240086476|1020230057373|1020207033415|1020220128149|1020230058249|1020120155410|1020217001093|1020150084489|1020220107300|1020247032026|1020200189963|1020230174263|1020210029775|1020200018955|1020230149691|1020240001539|1020207021273|1020230054377|1020227042756|1020240146413|1020247030211|1020247029209|1020230018878|1020197022720|1020230057622|1020210122762|1020247035467|1020210061962|1020160102976|1020220175524|1020160023699|1020237044463|1020210136553|1020110080120|1020230059130|1020230057143|1020200056446|1020150108227|1020220169678|1020160015445|1020207010838|1020237022037|1020220167086|1020220089449|1020190094321|1020240129357|1020227013870|1020240154153|2019950035506|1020220131139|1020237035531|1020190166088|1020180131232|1020220135738|1020220052248|1020190119588|1020230057646|1020237027457|1020217023070|1020240055925|1020190017973|1020220132909"
# data_list = data.split("|")

# datas = [{'2020040031672': '119950034357'}, {'1020190062722': '120180136950'}, {'2020210000007': '120200533829'}, {'1020220021103': '220020242934'}, {'1020220175029': '120010134557'}, {'1020230022997':'220050129079'}, {'1020220163314':'220050257697'}, {'1020140035677':'220040333089'}]
# print(len(datas))

start = time()

mysql = Mysql()

company_no_id = mysql.get_all_company_no_id()
company_dict = {item[0]: item[1] for item in company_no_id}
university_no_id = mysql.get_all_university_no_seq()
university_dict = {item[0]: item[1] for item in university_no_id}

print("DB에서 값 가지고오기 " , time() - start )

start = time()

comp_patent_list = []
univ_patent_list = []

for data in tqdm(datas):
    key, value = list(data.items())[0]
    temp_dict = {}
    if value in university_dict:
        # print(201)
        temp_dict[key] = university_dict[value]
        univ_patent_list.append(temp_dict)
        continue
    if value in company_dict:
        # print(200)
        temp_dict[key] = company_dict[value]
        comp_patent_list.append(temp_dict)

print("기업 특허_리스트")
print(len(comp_patent_list))
print(comp_patent_list[:20])
print("대학 특허_리스트")
print(len(univ_patent_list))
print(univ_patent_list[:20])

print("우리 고객 리스트만 확인" , time() - start )