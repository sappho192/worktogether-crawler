import scrapy
import scrapy.http
import re
import os.path
from pathlib import Path

def getLinks():
    filename = 'result.txt'
    result = []
    if(os.path.isfile(filename)): # file exists
        with open(filename, 'r') as file:
            result = file.readlines()
    else:
        file = Path(filename)
        file.touch(exist_ok=True)
    return result

def filterText(innerHtml, regex, trim=False):
    innerHtml = str(innerHtml)
    # regex = r"<td.?>(.+)</td>|<td.+>(.+)</td>|\\n(.+)\\t"
    matches = re.finditer(regex, innerHtml, re.MULTILINE)

    result = ''
    for matchNum, match in enumerate(matches, start=1):
        # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
            if not (match.group(groupNum) is None):
                result = match.group(groupNum)
    if(trim is True):
        result = result.replace('\\n','').replace('\\t','')
    return result

def filterCeoName(innerHtml):
    return filterText(innerHtml, r"<td.?>(.+)</td>")

def filterEmployeeNumber(innerHtml):
    return filterText(innerHtml, r"<td.?>(.+)</td>")

def filterMoney(innerHtml):
    return filterText(innerHtml, r"<td.?>(.+)</td>", True)

def filterGross(innerHtml):
    return filterText(innerHtml, r"<td.?>(.+)</td>", True)

def filterCategory(innerHtml):
    return filterText(innerHtml, r"<td.+>(.+)</td>")

def filterDetail(innerHtml):
    return filterText(innerHtml, r"<td.+>(.+)</td>", True)

def filterAddress(innerHtml):
    return filterText(innerHtml, r"\\n(.+)\\t", True)

def filterHomepage(innerHtml):
    return filterText(innerHtml, r"<td.+>.+<a href=\"(.+)\" target")

def filterBlog(innerHtml):
    return filterText(innerHtml, r"<td.+>.+<a href=\"(.+)\" target")

def filterSns(innerHtml):
    return filterText(innerHtml, r"<td.+>.+<a href=\"(.+)\" target")

def filterSource(innerHtml):    
    return filterText(innerHtml, r"<td.+>(.+)</td>")

def parseCompanyInfo(response: scrapy.http.Response):
    regex = r"<p class=\"tit\">(.+)"
    matches = re.finditer(regex, response.text, re.MULTILINE)

    title = ''
    for matchNum, match in enumerate(matches, start=1):
        # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
            title = match.group(groupNum)
            # print(title)

    ceoName_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[1]')
    employeeNumber_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[2]')
    money_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[1]')
    gross_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[2]')
    category_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[3]/td')
    detail_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[4]/td')
    address_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[5]/td/text()')
    homepage_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[6]/td')
    blog_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[7]/td')
    sns_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[8]/td')
    source_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[9]/td')

    # print(ceoName_org.extract())
    # print(employeeNumber_org.extract())
    # print(money_org.extract())
    # print(gross_org.extract())
    # print(category_org.extract())
    # print(detail_org.extract())
    # print(address_org.extract())
    # print(homepage_org.extract())
    # print(blog_org.extract())
    # print(sns_org.extract())
    # print(source_org.extract())

    ceoName         = filterCeoName(ceoName_org.extract())
    employeeNumber  = filterEmployeeNumber(employeeNumber_org.extract())
    money           = filterMoney(money_org.extract())
    gross           = filterGross(gross_org.extract())
    category        = filterCategory(category_org.extract())
    detail          = filterDetail(detail_org.extract())
    address         = filterAddress(address_org.extract())
    homepage        = filterHomepage(homepage_org.extract())
    blog            = filterBlog(blog_org.extract())
    sns             = filterSns(sns_org.extract())
    source          = filterSource(source_org.extract())

    return f'"{title}","{ceoName}","{employeeNumber}","{money}","{gross}","{category}","{detail}","{address}","{homepage}","{blog}","{sns}","{source}"'

def filterRecruitCat(innerHtml):
    return filterText(innerHtml, r"(.+)", True)

def filterRelativeCat(innerHtml):
    return filterText(innerHtml, r"(.+)", True)

def filterWorkDetail(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True)
    text = text.replace("\\xa0",' ').replace("\\r",'.').replace("<br>",'').replace("\"","\'").replace('&lt;', '<').replace('&gt;', '>')
    return text

def filterDue(innerHtml):
    return filterText(innerHtml, r"\\t([^a-zA-Z]+)\\n")

def filterJobType(innerHtml):
    return filterText(innerHtml, r"^([\w|\s]+)\\n")

def filterRecruitNum(innerHtml):
    return filterText(innerHtml, r"^([\w|\s]+)\\n")

def filterDisRecruitNum(innerHtml):
    return filterText(innerHtml, r"([^a-zA-Z|\s]+)\\n")

def filterWageCond(innerHtml):
    text = filterText(innerHtml, r"(.+)\\n.+\\t\s+", True).rstrip().replace("', '", ',')
    text = re.sub(r"\s{3,}", '', text)
    return text

def filterCareerCond(innerHtml):
    return filterText(innerHtml, r"(.+)", True)

def filterAcademicCareer(innerHtml):
    return filterText(innerHtml, r"\s\\t([^a-zA-z]+)", True)

def filterKeyword(innerHtml):
    # match가 여러개 있으니 반영할것
    text = filterText(innerHtml, r"(.+)", True)
    # text = re.sub(r"<a.+?>.+?</a>", '', text)
    text = text.replace("', '", ',').replace("'",'').replace("]",'').replace("[",'')
    return text

def parseJobDetail(response: scrapy.http.Response):
    # 모집직종
    recruit_cat_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[1]/td/text()')
    # 관련직종
    relative_cat_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[2]/td/text()')
    # 직무내용
    work_detail_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[3]/td')
    # 접수마감일
    due_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[4]/td')
    # 고용형태
    job_type_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[5]/td/text()')
    # 모집인원
    recruit_num_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[6]/td/text()')
    # 장애인 채용인원
    dis_recruit_num_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[7]/td/text()')
    # 임금조건
    wage_cond_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[8]/td/text()')
    # 경력조건
    career_cond_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[9]/td/text()')
    # 학력
    academic_career_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[10]/td/text()')
    # 키워드
    keyword_org = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[1]/tbody/tr[11]/td/text()')

    # print(str(recruit_cat_org.extract()).replace("['",'').replace("']",''))
    # print(str(relative_cat_org.extract()).replace("['",'').replace("']",''))
    # print(str(work_detail_org.extract()).replace("['",'').replace("']",''))
    # print(str(due_org.extract()).replace("['",'').replace("']",''))
    # print(str(job_type_org.extract()).replace("['",'').replace("']",''))
    # print(str(recruit_num_org.extract()).replace("['",'').replace("']",''))
    # print(str(dis_recruit_num_org.extract()).replace("['",'').replace("']",''))
    # print(str(wage_cond_org.extract()).replace("['",'').replace("']",''))
    # print(str(career_cond_org.extract()).replace("['",'').replace("']",''))
    # print(str(academic_career_org.extract()).replace("['",'').replace("']",''))
    # print(str(keyword_org.extract()))

    recruitCategory     = filterRecruitCat(str(recruit_cat_org.extract()).replace("['",'').replace("']",''))
    relativeCategory    = filterRelativeCat(str(relative_cat_org.extract()).replace("['",'').replace("']",''))
    workDetail          = filterWorkDetail(str(work_detail_org.extract()).replace("['",'').replace("']",''))
    due                 = filterDue(str(due_org.extract()).replace("['",'').replace("']",''))
    jobType             = filterJobType(str(job_type_org.extract()).replace("['",'').replace("']",''))
    recruitNum          = filterRecruitNum(str(recruit_num_org.extract()).replace("['",'').replace("']",''))
    disorderRecruitNum  = filterDisRecruitNum(str(dis_recruit_num_org.extract()).replace("['",'').replace("']",''))
    wageCondition       = filterWageCond(str(wage_cond_org.extract()).replace("['",'').replace("']",''))
    careerCondition     = filterCareerCond(str(career_cond_org.extract()).replace("['",'').replace("']",''))
    academicCareer      = filterAcademicCareer(str(academic_career_org.extract()).replace("['",'').replace("']",''))
    keyword             = filterKeyword(str(keyword_org.extract()))

    print(f'recruitCategory: {recruitCategory}, relativeCategory: {relativeCategory}, workDetail: {workDetail}, due: {due}, jobType: {jobType}, recruitNum: {recruitNum}, disorderRecruitNum: {disorderRecruitNum}, wageCondition: {wageCondition}, careerCondition: {careerCondition}, academicCareer: {academicCareer}, keyword: {keyword}')

    return f'"{recruitCategory}","{relativeCategory}","{workDetail}","{due}","{jobType}","{recruitNum}","{disorderRecruitNum}","{wageCondition}","{careerCondition}","{academicCareer}","{keyword}"'

def filterForeignLang(innerHtml):
    return filterText(innerHtml, r"<td>(.+)<!--.+</td>", True)

def filterMajor(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterQualifi(innerHtml):
    return filterText(innerHtml, r"<td>(.+)<!--.+</td>", True).replace("<br>", '')

def filterArmyEx(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterComputerSkill(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterAdvantage(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True).replace("\\xa0", ' ')

def filterEmployEx(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True).strip()

def filterEnvironment(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True)
    return text.replace("<p>",'').replace("</p>",', ')

def filterAdvantageEx(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True)
    text = text.replace('\\xa0', ' ').replace('<br>', ' ').replace('\\r', '')
    return 

def parsePreferential(response: scrapy.http.Response):
    foreign_lang_org    = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[1]/td')
    major_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[2]/td')
    qualifi_org         = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[3]/td')
    army_ex_org         = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[4]/td')
    computer_skill_org  = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[5]/td')
    advantage_org       = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[6]/td')
    employ_ex_org       = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[7]/td')
    environment_org     = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[8]/td')
    advantage_ex_org    = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[2]/tbody/tr[9]/td')

    # print(str(foreign_lang_org.extract()).replace("['",'').replace("']",''))
    # print(str(major_org.extract()).replace("['",'').replace("']",''))
    # print(str(qualifi_org.extract()).replace("['",'').replace("']",''))
    # print(str(army_ex_org.extract()).replace("['",'').replace("']",''))
    # print(str(computer_skill_org.extract()).replace("['",'').replace("']",''))
    # print(str(advantage_org.extract()).replace("['",'').replace("']",''))
    # print(str(employ_ex_org.extract()).replace("['",'').replace("']",''))
    # print(str(environment_org.extract()).replace("['",'').replace("']",''))
    # print(str(advantage_ex_org.extract()).replace("['",'').replace("']",''))

    foreignLang    = filterForeignLang(str(foreign_lang_org.extract()).replace("['",'').replace("']",''))
    major           = filterMajor(str(major_org.extract()).replace("['",'').replace("']",''))
    qualifi         = filterQualifi(str(qualifi_org.extract()).replace("['",'').replace("']",''))
    armyEx         = filterArmyEx(str(army_ex_org.extract()).replace("['",'').replace("']",''))
    computerSkill  = filterComputerSkill(str(computer_skill_org.extract()).replace("['",'').replace("']",''))
    advantage       = filterAdvantage(str(advantage_org.extract()).replace("['",'').replace("']",''))
    employEx       = filterEmployEx(str(employ_ex_org.extract()).replace("['",'').replace("']",''))
    environment     = filterEnvironment(str(environment_org.extract()).replace("['",'').replace("']",''))
    advantageEx    = filterAdvantageEx(str(advantage_ex_org.extract()).replace("['",'').replace("']",''))

    print(f'foreignLang: {foreignLang}, major: {major}, qualifi: {qualifi}, armyEx: {armyEx}, computerSkill: {computerSkill}, advantage: {advantage}, employEx: {employEx}, environment: {environment}, advEx: {advantageEx}')
    return f'"{foreignLang}","{major}","{qualifi}","{armyEx}","{computerSkill}","{advantage}","{employEx}","{environment}","{advantageEx}"'

def filterApplyCategory(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterApplyWay(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True)
    text = text.replace("\\xa0",' ').replace("\\r",'.').replace("<br>",'')
    return text

def filterApplyMaterial(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True).replace("<br>",'').replace("</a>",'').replace('<span>','').replace('</span>', '')
    text = re.sub(r'<a .+>', '', text)
    return text

def filterApplyPaper(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True)
    link = filterText(text, r"<a href=\"(.+)\" class").replace('&amp;','&')
    link = f'https://www.worktogether.or.kr/{link}'
    return link

def parseApplyDetail(response: scrapy.http.Response):
    apply_category_org  = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[3]/tbody/tr[1]/td')
    apply_way_org       = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[3]/tbody/tr[2]/td')
    apply_material_org  = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[3]/tbody/tr[3]/td')
    apply_paper_org     = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[3]/tbody/tr[4]/td')

    # print(str(apply_category_org.extract()).replace("['",'').replace("']",''))
    # print(str(apply_way_org.extract()).replace("['",'').replace("']",''))
    # print(str(apply_material_org.extract()).replace("['",'').replace("']",''))
    # print(str(apply_paper_org.extract()).replace("['",'').replace("']",''))

    applyCategory   = filterApplyCategory(str(apply_category_org.extract()).replace("['",'').replace("']",''))
    applyWay        = filterApplyWay(str(apply_way_org.extract()).replace("['",'').replace("']",''))
    applyMaterial   = filterApplyMaterial(str(apply_material_org.extract()).replace("['",'').replace("']",''))
    applyPaper      = filterApplyPaper(str(apply_paper_org.extract()).replace("['",'').replace("']",''))

    print(f'applyCategory: {applyCategory}, applyWay: {applyWay}, applyMaterial: {applyMaterial}, applyPaper: {applyPaper}')
    return f'"{applyCategory}","{applyWay}","{applyMaterial}","{applyPaper}"'

def filterWorkLocation(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True).replace('\\xao','')
    text = filterText(innerHtml, r"<span.+?>(.+)</span>", True)
    return text

def filterNearSubway(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True).strip()

def filterBus(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterWorkDays(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterMeal(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterWorkTime(innerHtml):
    text = filterText(innerHtml, r"<td>(.+)</td>", True)
    text = re.sub(r"\s{3,}", '', text)
    text = text.replace('<br>','').replace('<span>','').replace('</span>',' ').replace('<b>','').replace('</b>','').replace('\\xa0',' ')
    text = re.sub(r"<!--.+-->", '', text)
    return text

def filterEnsurance(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterRetireMoney(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterWalfare(innerHtml):
    return filterText(innerHtml, r"<td>(.+)</td>", True)

def filterDisabledComforts(innerHtml):
    return filterText(innerHtml, r"(.+)", True)

def parseWorkEnvironment(response: scrapy.http.Response):
    workLocation = ''
    nearSubway = ''
    bus = ''
    workDays = ''
    meal = ''
    workTime = ''
    ensurance = ''
    retireMoney = ''
    welfare = ''
    disabledComforts = ''

    fifth_info = str(response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[5]/th/text()').extract()).replace("['",'').replace("']",'')
    print(f'fifth_info: {fifth_info}')
    if(fifth_info == '식사(비) 제공'):
        work_location_org       = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[1]/td')
        near_subway_org         = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[2]/td')
        bus_org                 = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[3]/td')
        work_days_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[4]/td')
        meal_org                = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[5]/td')
        work_time_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[6]/td')
        ensurance_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[7]/td')
        retire_money_org        = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[8]/td')
        welfare_org             = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[9]/td')
        disabled_comforts_org   = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[10]/td/text()')

        workLocation        = filterWorkLocation(str(work_location_org.extract()).replace("['",'').replace("']",''))
        nearSubway          = filterNearSubway(str(near_subway_org.extract()).replace("['",'').replace("']",''))
        bus                 = filterBus(str(bus_org.extract()).replace("['",'').replace("']",''))
        workDays            = filterWorkDays(str(work_days_org.extract()).replace("['",'').replace("']",''))
        meal                = filterMeal(str(meal_org.extract()).replace("['",'').replace("']",''))
        workTime            = filterWorkTime(str(work_time_org.extract()).replace("['",'').replace("']",''))
        ensurance           = filterEnsurance(str(ensurance_org.extract()).replace("['",'').replace("']",''))
        retireMoney         = filterRetireMoney(str(retire_money_org.extract()).replace("['",'').replace("']",''))
        welfare             = filterWalfare(str(welfare_org.extract()).replace("['",'').replace("']",''))
        disabledComforts    = filterDisabledComforts(str(disabled_comforts_org.extract()).replace("['",'').replace("']",''))
    else: # 식사제공 칸 없고 바로 근무시간으로 넘어가짐
        work_location_org       = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[1]/td')
        near_subway_org         = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[2]/td')
        bus_org                 = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[3]/td')
        work_days_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[4]/td')
        work_time_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[5]/td')
        ensurance_org           = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[6]/td')
        retire_money_org        = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[7]/td')
        welfare_org             = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[8]/td')
        disabled_comforts_org   = response.selector.xpath('//*[@id="content"]/div[4]/div[1]/div[3]/table[4]/tbody/tr[9]/td/text()')

        workLocation        = filterWorkLocation(str(work_location_org.extract()).replace("['",'').replace("']",''))
        nearSubway          = filterNearSubway(str(near_subway_org.extract()).replace("['",'').replace("']",''))
        bus                 = filterBus(str(bus_org.extract()).replace("['",'').replace("']",''))
        workDays            = filterWorkDays(str(work_days_org.extract()).replace("['",'').replace("']",''))
        workTime            = filterWorkTime(str(work_time_org.extract()).replace("['",'').replace("']",''))
        ensurance           = filterEnsurance(str(ensurance_org.extract()).replace("['",'').replace("']",''))
        retireMoney         = filterRetireMoney(str(retire_money_org.extract()).replace("['",'').replace("']",''))
        welfare             = filterWalfare(str(welfare_org.extract()).replace("['",'').replace("']",''))
        disabledComforts    = filterDisabledComforts(str(disabled_comforts_org.extract()).replace("['",'').replace("']",''))

    # print(str(work_location_org.extract()).replace("['",'').replace("']",''))
    # print(str(near_subway_org.extract()).replace("['",'').replace("']",''))
    # print(str(bus_org.extract()).replace("['",'').replace("']",''))
    # print(str(work_days_org.extract()).replace("['",'').replace("']",''))
    # print(str(meal_org.extract()).replace("['",'').replace("']",''))
    # print(str(work_time_org.extract()).replace("['",'').replace("']",''))
    # print(str(ensurance_org.extract()).replace("['",'').replace("']",''))
    # print(str(retire_money_org.extract()).replace("['",'').replace("']",''))
    # print(str(welfare_org.extract()).replace("['",'').replace("']",''))
    # print(str(disabled_comforts_org.extract()).replace("['",'').replace("']",''))

    print(f'workLocation: {workLocation}, nearSubway: {nearSubway}, bus: {bus}, workDays: {workDays}, meal: {meal}, workTime: {workTime}, ensurance: {ensurance}, retireMoney: {retireMoney}, welfare: {welfare}, disabledComforts: {disabledComforts}')
    return f'"{workLocation}","{nearSubway}","{bus}","{workDays}","{meal}","{workTime}","{ensurance}","{retireMoney}","{welfare}","{disabledComforts}"'

class WtgdbotSpider(scrapy.Spider):
    name = 'wtgdbot'
    allowed_domains = ['www.worktogether.or.kr']
    start_urls = getLinks()
    # start_urls = ['https://www.worktogether.or.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?callPage=detail&wantedAuthNo=K151572201040054&rtnUrl=/empInfo/empInfoSrch/list/dtlEmpSrchList.do?relYn=N&totalEmpCount=0&jobsCount=0&len=0&tot=0&mainSubYn=N&softMatchingPossibleYn=N&preferentialGbn=D&disableEmpHopeGbn=D&pageSize=10&firstIndex=1&lastIndex=1&recordCountPerPage=10&rowNo=0&benefitSrchAndOr=O&preferentialGbn=D&serialversionuid=3990642507954558837&onlyContentSrchYn=N&softMatchingMinRate=%2066&softMatchingMaxRate=100&empTpGbcd=1&charSet=EUC-KR&startPos=0&collectionName=tb_workinfo&certifiYn=N&preferentialYn=Y&preferential=D&siteClcd=WORK&majorYn=N&onlyTitleSrchYn=N&keywordSecd=N|N|N|N&resultCnt=10&sortOrderBy=DESC&sortField=DATE&pageIndex=11&pageUnit=10']

    def parse(self, response: scrapy.http.Response):
        companyInfo = parseCompanyInfo(response)
        jobDetail = parseJobDetail(response)
        preferential = parsePreferential(response)
        applyDetail = parseApplyDetail(response)
        workEnvironment = parseWorkEnvironment(response)

        resultfile = 'result.csv'
        if(os.path.isfile(resultfile)): # file exists
            file = open(resultfile, 'a')
            file.write(f'"{response.url}",{companyInfo},{jobDetail},{preferential},{applyDetail},{workEnvironment}\n')
        else: # file not exist
            file = open('result.csv', 'w+')
            headerUrl = 'Url'
            headerCompanyInfo = 'Title,CeoName,EmployeeNumber,Money,Gross,Category,Detail,Address,Homepage,Blog,Sns,Source'
            headerJobDetail = 'RecruitCategory,RelativeCategory,WorkDetail,Due,JobType,RecruitNum,DisorderRecruitNum,WageCondition,CareerCondition,AcademicCareer,Keyword'
            headerPreferential = 'ForeignLang,Major,Qualifi,ArmyEx,ComputerSkill,Advantage,EmployEx,Environment,AdvantageEx'
            headerApplyDetail = 'ApplyCategory,ApplyWay,ApplyMaterial,ApplyPaper'
            headerWorkEnvironment = 'WorkLocation,NearSubway,Bus,WorkDays,Meal,WorkTime,Ensurance,RetireMoney,Welfare,DisabledComforts'
            file.write(f'{headerUrl},{headerCompanyInfo},{headerJobDetail},{headerPreferential},{headerApplyDetail},{headerWorkEnvironment}\n')
            file.write(f'"{response.url}",{companyInfo},{jobDetail},{preferential},{applyDetail},{workEnvironment}\n')

        pass
