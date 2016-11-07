from .models import lecture,kakao_user,major_list
import requests
from bs4 import BeautifulSoup
from datetime import date

import re

def function():
    new=kakao_user(user_key="000")
    new.save()
    


head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
timetable_url = "http://webs.hufs.ac.kr:8989/src08/jsp/lecture/LECTURE2020L.jsp"

class parsing_class():
    def __init__(self):

        ######-----시간표 url의 params 데이터를 실시간으로 반영하는 초기화 함수-----#####
        
        #-----today()로 해당연도, 해당학기 구하기-----#

        now = date.today()

        self.default_year = now.year

        if now.month >=8:
            self.default_session = '3'
        else:
            self.default_session = '1'

        #-----학부, 서울 캠퍼스-----#
        
        self.default_school = 'A' # 학부
        self.default_campus = 'H1' # 서울캠퍼스

        #-----default 옵션을 제외한 나머지 옵션 가져오기-----#

        self.gubun_list = ['1','2'] # 1=전공/부전공, 2=실용외국어/교양과목
        self.major_code_list = [] # 전공 코드 목록
        self.liberal_code_list = [] # 교양 코드 목록
        self.major_dict=dict()
        self.liberal_dict=dict()
        
        all_major=major_list.objects.filter(year=self.default_year,semester=self.default_session)
        liberals=all_major.filter(category=0)
        majors=all_major.filter(category=1)
        
        
        for major in majors:
            self.major_dict[major.major_name]=major.major_code
        
        for liberal in liberals:
            self.liberal_dict[liberal.major_name]=liberal.major_code
            
        self.major_code_list=list(self.major_dict.values())
        self.liberal_code_list=list(self.liberal_dict.values())
        
    def parsing_all(self):

        #-----조회할 데이터 옵션 선택-----#

        self.course_info_list = list()

        for i in range(len(self.gubun_list)):
            if  i == 0:
                for j in range(len(self.major_code_list)):
                    params ={
                        'tab_lang':'K',
                        'type':'',
                        'ag_ledg_year': self.default_year, # 년도
                        'ag_ledgr_sessn': self.default_session, # 1=1학기, 2=여름계절, 3=2학기, 4=겨울계절
                        'ag_org_sect':'A', # A=학부, B=대학원, D=통번역대학원, E=교육대학원, G=정치행정언론대학원, H=국제지역대학원, I=경영대학원(주간), J=경영대학원(야간), L=법학전문대학원, M=TESOL대학원, T=TESOL전문교육원
                        'campus_sect':'H1', # H1=서울, H2=글로벌
                        'gubun': self.gubun_list[i], # 1=전공/부전공, 2=실용외국어/교양과목
                        'ag_crs_strct_cd': self.major_code_list[j], # 전공 목록
                        'ag_compt_fld_cd':'' # 교양 목록
                        }

                    self.major_data = list(self.parsing(params))
            else:
                for k in range(len(self.liberal_code_list)):
                    params ={
                        'tab_lang':'K',
                        'type':'',
                        'ag_ledg_year': self.default_year, # 년도
                        'ag_ledgr_sessn': self.default_session, # 1=1학기, 2=여름계절, 3=2학기, 4=겨울계절
                        'ag_org_sect':'A', # A=학부, B=대학원, D=통번역대학원, E=교육대학원, G=정치행정언론대학원, H=국제지역대학원, I=경영대학원(주간), J=경영대학원(야간), L=법학전문대학원, M=TESOL대학원, T=TESOL전문교육원
                        'campus_sect':'H1', # H1=서울, H2=글로벌
                        'gubun': self.gubun_list[i], # 1=전공/부전공, 2=실용외국어/교양과목
                        'ag_crs_strct_cd': '', # 전공 목록
                        'ag_compt_fld_cd': self.liberal_code_list[k] # 교양 목록
                        }

                    self.liberal_data = list(self.parsing(params))

        self.all_data = self.major_data + self.liberal_data


    def parsing_major_name(self, major_name):

        #-----조회할 데이터 옵션 선택-----#

        self.course_info_list = list()

        if major_name in self.major_dict.keys() == True:
            params ={
                'tab_lang':'K',
                'type':'',
                'ag_ledg_year': self.default_year, # 년도
                'ag_ledgr_sessn':self.default_session, # 1=1학기, 2=여름계절, 3=2학기, 4=겨울계절
                'ag_org_sect':'A', # A=학부, B=대학원, D=통번역대학원, E=교육대학원, G=정치행정언론대학원, H=국제지역대학원, I=경영대학원(주간), J=경영대학원(야간), L=법학전문대학원, M=TESOL대학원, T=TESOL전문교육원
                'campus_sect':'H1', # H1=서울, H2=글로벌
                'gubun': '1', # 1=전공/부전공, 2=실용외국어/교양과목
                'ag_crs_strct_cd': self.major_dict[major_name], # 전공 목록
                'ag_compt_fld_cd': '' # 교양 목록
                }
        else:
            params ={
                'tab_lang':'K',
                'type':'',
                'ag_ledg_year':self.default_year, # 년도
                'ag_ledgr_sessn':self.default_session, # 1=1학기, 2=여름계절, 3=2학기, 4=겨울계절
                'ag_org_sect':'A', # A=학부, B=대학원, D=통번역대학원, E=교육대학원, G=정치행정언론대학원, H=국제지역대학원, I=경영대학원(주간), J=경영대학원(야간), L=법학전문대학원, M=TESOL대학원, T=TESOL전문교육원
                'campus_sect':'H1', # H1=서울, H2=글로벌
                'gubun': '2', # 1=전공/부전공, 2=실용외국어/교양과목
                'ag_crs_strct_cd': '', # 전공 목록
                'ag_compt_fld_cd': ''#self.liberal_dict[major_name] # 교양 목록
                }

        self.major_name_data = list(self.parsing(params))


    def parsing(self, params):

        #####-----params를 인자로 받아서 파싱하는 함수-----#####
        self.current_session=requests.session()
        self.current_session.post(timetable_url,data=params,headers=head)

        #-----파싱 시작-----#
        
        self.timetable = self.current_session.post(timetable_url,data=params,headers=head)

        html = BeautifulSoup(self.timetable.text, "lxml")
        tr_courses = html.find_all("tr", attrs={"height":"55"})
        
        for tr_course in tr_courses:
            course_area = tr_course.find_all("td")[1].string # 개설영역
            course_year = tr_course.find_all("td")[2].string # 학년
            course_number = tr_course.find_all("td")[3].string # 학수번호

            self.course_name = tr_course.find_all("td")[4].get_text() # 교과목명
            self.course_name = self.course_name.replace("\n","")
            cut_count = self.course_name.count("(")
            for i in range(cut_count):
                cut = self.course_name.rfind("(")
                self.course_name = self.course_name[:cut]
            
            self.course_professor = tr_course.find_all("td")[10].get_text() # 담당교수
            self.course_professor = self.course_professor.replace("\r","").replace("\t","").replace("\n","")
            cut = self.course_professor.rfind("(")
            if cut!=-1:
                self.course_professor = self.course_professor[:cut]

            self.course_time = tr_course.find_all("td")[13].get_text() # 강의시간
            cut = self.course_time.find("(")
            self.course_time = self.course_time[:cut-1]
            
            self.course_people = tr_course.find_all("td")[14].string # 현재인원
            self.course_people = self.course_people.replace("\xa0","")

            self.course_info_list.append([self.course_name, self.course_professor, self.course_time, self.course_people])

        self.parsing_data = self.course_info_list

        return self.parsing_data
    
    @staticmethod
    def major_list_parsing():
        now = date.today()

        default_year = now.year

        if now.month >=8:
            default_session = '3'
        else:
            default_session = '1'
            
        current_session = requests.session()
        
        current_session.get(timetable_url,headers=head)
        timetable = current_session.get(timetable_url,headers=head)
        html = BeautifulSoup(timetable.text, "lxml")
        liberals = html.find_all("select", attrs={"name":"ag_compt_fld_cd"})
        
        liberals = liberals[0].find_all("option")
        for liberal in liberals:
            
            major_name=liberal.get_text()
            major_name=major_name.replace('\xa0',"").replace('\r','').replace('\n','').replace('\t','')
            major_name=major_name[:-4]
            try:
                exist_one=major_list.objects.get(major_name=major_name,year=default_year,semester=default_session)
                exist_one.major_name=major_name
                exist_one.major_code=liberal['value']
                exist_one.year=default_year
                exist_one.semester=default_session
                exist_one.category=0
                exist_one.save()
            except:
                major_list(major_name=major_name,major_code=liberal['value'],year=default_year,semester=default_session,category=0).save()
   
        #-----전공 코드(params 데이터)와 전공명 딕셔너리 만들기-----#

        major_dict = dict()

        majors = html.find_all("select", attrs={"name":"ag_crs_strct_cd"})
        majors = majors[0].find_all("option")

        for major in majors:
            major_name = major.get_text()
            major_name = major_name.replace('\xa0',"").replace('\r','').replace('\n','').replace('\t','')
            cut = major_name.find("-")
            major_name = major_name[cut+1:]
            cut = major_name.find("(")
            major_name = major_name[:cut]
            
            try:
                exist_one=major_list.objects.get(major_name=major_name,year=default_year,semester=default_session)
                exist_one.major_name=major_name
                exist_one.major_code=major['value']
                exist_one.year=default_year
                exist_one.semester=default_session
                exist_one.category=1
                exist_one.save()
            except:
                major_list(major_name=major_name,major_code=major['value'],year=default_year,semester=default_session,category=1).save()
