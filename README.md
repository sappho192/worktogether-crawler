**발로 짰습니다.**

# 사용법
## 환경 설치
* 윈도우+R -> powershell 엔터 -> 까만(혹은 남색) 터미널 불러오기
* pip install scrapy 엔터

* wtgbot, wtgdbot 모두 결과 파일에(txt,csv) 결과를 이어서 덧붙이기 때문에 새로 실행하려면 기존에 만들어진 result.txt와 result.csv는 지우고 실행해야 합니다.  
버스 노선의 경우 csv로 저장후 액셀에서 읽어들일때 30-11 같은 노선은 날짜로(1970-11-30) 읽어들이는 경우가 있기 때문에 이런건 모집 링크로 직접 들어가서 가져와야 할 것 같습니다.

## 실행 전 준비 사항
* 아래 링크로 들어가서 마지막 페이지가 몇 페이지인지 확인해주세요. 코드 작성 시점엔 35~38페이지 정도 됐습니다.  
https://www.worktogether.or.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?pageIndex=1&pageUnit=10&relYn=N&totalEmpCount=0&jobsCount=0&len=0&tot=0&mainSubYn=N&softMatchingPossibleYn=N&preferentialGbn=D&disableEmpHopeGbn=D&pageSize=10&firstIndex=1&lastIndex=1&recordCountPerPage=10&rowNo=0&benefitSrchAndOr=O&serialversionuid=3990642507954558837&onlyContentSrchYn=N&softMatchingMinRate=%2066&softMatchingMaxRate=100&empTpGbcd=1&charSet=EUC-KR&startPos=0&collectionName=tb_workinfo&certifiYn=N&preferentialYn=Y&preferential=D&siteClcd=WORK&majorYn=N&onlyTitleSrchYn=N&keywordSecd=N|N|N|N&resultCnt=10&sortOrderBy=DESC&sortField=DATE

* wtg/spiders/wtgbot.py 를 텍스트 편집기(메모장 등)으로 열어서 11번째 줄에 있는 아래 코드를 바꿔주세요.  
* `for i in range(2,35):` ← 35를 `실제 페이지+1`로 업데이트   
만약 마지막 페이지가 38페이지였다면 `for i in range(2,39):` 로 수정하고 저장하면 됩니다.

## 실행 방법
* 윈도우 탐색기에서 wtg/wtg 폴더까지 들어온 다음 적당히 빈 곳에서 쉬프트+마우스 오른쪽클릭 -> 여기에 PowerShell 창 열기 클릭
* PowerShell 창에서 아래 명령어 각각 한번씩 실행
* `scrapy crawl wtgbot`
* `scrapy crawl wtgdbot`

## 헤더 정보
* Url  
채용 페이지 주소

* Title,CeoName,EmployeeNumber,Money,Gross,Category,Detail,Address,Homepage,Blog,Sns,Source  
채용페이지제목,대표자명,근로자수,자본금,연매출액,업종,주요사업내용,회사주소,홈페이지,회사블로그,회사SNS

* RecruitCategory,RelativeCategory,WorkDetail,Due,JobType,RecruitNum,DisorderRecruitNum,WageCondition,CareerCondition,AcademicCareer,Keyword  
모집직종,관련직종,직무내용,접수마감일,고용형태,모집인원,장애인채용인원,임금조건,경력조건,학력,키워드

* ForeignLang,Major,Qualifi,ArmyEx,ComputerSkill,Advantage,EmployEx,Environment,AdvantageEx  
외국어능력,전공,자격면허,병력특례채용희망,컴퓨터활용능력,우대조건,고용허가제,작업환경,기타우대사항

* ApplyCategory,ApplyWay,ApplyMaterial,ApplyPaper  
전형방법,접수방법,제출서류준비물,제출서류양식첨부

* WorkLocation,NearSubway,Bus,WorkDays,Meal,WorkTime,Ensurance,RetireMoney,Welfare,DisabledComforts  
근무예정지,인근전철역,버스노선,근무형태,식사(비)제공,근무시간

