# suppress all warnings
import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import demjson
import requests
import json
import os
import re
from unicodedata import *
from bs4 import BeautifulSoup

class NTIC():

    _login_path = 'https://elearning.univ-constantine2.dz/elearning/login/index.php'
    _chrome_driver_path = 'C:/dev/Chrome Driver/chromedriver.exe'

    courses = {
        "POO": 1080,
        "TL": 1079,
        "ASD": 1076,
        "LM": 1077,
        "AO": 1075,
        "SI": 14,
        "LE": 1081
    }

    def __init__(self, usr = '181834034942', pwd = '22102000', no_cache = False):
        if(os.path.exists('cookie.json') and not no_cache):
            self.cookie = json.load(fp= open('cookie.json', 'r'))
        else:
            self.driver = self.get_driver()
            self.login(usr, pwd)
            self.cookie = self.get_cookie()

    def get_driver(self, run_headless = True):            
        options = webdriver.ChromeOptions()
        if(run_headless): options.add_argument("headless")

        return webdriver.Chrome(executable_path= self._chrome_driver_path, options=options)

    def login(self, username, password):
        
        self.driver.get(self._login_path)
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("loginbtn").click()
    
    def get_cookie(self):
        cookies = []
        for cookie in self.driver.get_cookies():
            cookies.append({cookie["name"]: cookie["value"]})
        
        return cookies[0]
    
    def course_link(self, id):
        return f'https://elearning.univ-constantine2.dz/elearning/course/view.php?id={id}'

    def make_session(self):
        session = requests.session()
        session.cookies.update(self.cookie)
        
        return session

    def get_course_html(self, course_name):
        return self.make_session().get(self.course_link(
            self.courses[course_name]
        )).text

    def find_destination(self, link):
        return self.make_session().get(link, allow_redirects=True).url
    
    def get_all_classes(self, course_name):
        soup = BeautifulSoup(self.get_course_html(course_name), 'html.parser')
        weeks = soup.find('div', {'class': 'course-content'})

        course_content = {}
        for li in weeks.find_all('li', {'id': re.compile('section-\d+')}):
            
            contentdiv = li.find_all('div', {'class': 'content'})[0]
            contentName = contentdiv.find('h3', {'class': 'sectionname'})
            
            if(contentName == None): continue
            contentName = contentName.get_text()
            course_content[contentName] = {}

            print(contentName)
            for activity in li.find_all('li', {'class': re.compile('activity .*')}):

                if(activity['class'][1] in ['folder', 'forum', 'label']): continue

                activity_instance = activity.find_all('div', {'class': 'activityinstance'})[0]

                link = activity_instance.find('a', {'onclick', re.compile('.*')})
                
                link_title = str(link.find('span', {'class': 'instancename'}).get_text())[0:-4]
                link = (
                    link.get('href') or
                    re.search(r"window\.open\((.*)", str(link.get('onclick'))).groups()[0].split(',')[0][1:-1]
                )

                course_content[contentName][link_title] = self.find_destination(link)
        
        print('==================================>')
        return course_content

if __name__ == '__main__':
    
    n = NTIC()
    
    course = 'SI'
    info = n.get_all_classes(course)
    with open(f'courses/{course}.json', 'w+', encoding= "UTF-8") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))