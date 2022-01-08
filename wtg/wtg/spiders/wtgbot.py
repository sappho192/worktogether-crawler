import scrapy
import re
import os.path

class WtgbotSpider(scrapy.Spider):
    name = 'wtgbot'
    allowed_domains = ['https://www.worktogether.or.kr']
    start_urls = [
    'https://www.worktogether.or.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?pageIndex=1&pageUnit=10&relYn=N&totalEmpCount=0&jobsCount=0&len=0&tot=0&mainSubYn=N&softMatchingPossibleYn=N&preferentialGbn=D&disableEmpHopeGbn=D&pageSize=10&firstIndex=1&lastIndex=1&recordCountPerPage=10&rowNo=0&benefitSrchAndOr=O&serialversionuid=3990642507954558837&onlyContentSrchYn=N&softMatchingMinRate=+66&softMatchingMaxRate=100&empTpGbcd=1&charSet=EUC-KR&startPos=0&collectionName=tb_workinfo&certifiYn=N&preferentialYn=Y&preferential=D&siteClcd=WORK&majorYn=N&onlyTitleSrchYn=N&keywordSecd=N|N|N|N&resultCnt=10&sortOrderBy=DESC&sortField=DATE#none'
    ]
    for i in range(2,35):
        start_urls.append(f'https://www.worktogether.or.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?pageIndex={i}&pageUnit=10&relYn=N&totalEmpCount=0&jobsCount=0&len=0&tot=0&mainSubYn=N&softMatchingPossibleYn=N&preferentialGbn=D&disableEmpHopeGbn=D&pageSize=10&firstIndex=1&lastIndex=1&recordCountPerPage=10&rowNo=0&benefitSrchAndOr=O&serialversionuid=3990642507954558837&onlyContentSrchYn=N&softMatchingMinRate=+66&softMatchingMaxRate=100&empTpGbcd=1&charSet=EUC-KR&startPos=0&collectionName=tb_workinfo&certifiYn=N&preferentialYn=Y&preferential=D&siteClcd=WORK&majorYn=N&onlyTitleSrchYn=N&keywordSecd=N|N|N|N&resultCnt=10&sortOrderBy=DESC&sortField=DATE#none')
    print(start_urls)

    def parse(self, response):
        regex = r"<a href=\"(\/empInfo/empInfoSrch/detail/empDetailAuthView\.do\?callPage.+)\">"
        matches = re.finditer(regex, response.text, re.MULTILINE)

        result = set()
        for matchNum, match in enumerate(matches, start=1):
            # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                # print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
                urltail = match.group(groupNum)
                # result.append(filename)
                url = 'https://www.worktogether.or.kr' + urltail
                url = url.replace('&amp;', '&')
                print(url)
                result.add(url)

        resultFile = 'result.txt'
        if(os.path.isfile(resultFile)): # file exists
            file = open(resultFile, 'a')
            for item in result:
                file.write('%s\n' % item)
        else: # if file is not exist
            file = open(resultFile, 'w+')
            for item in result:
                file.write('%s\n' % item)
        pass
