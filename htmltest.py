#!/usr/bin/env python
# coding: utf-8

# In[9]:


#!pip install pymysql
#!pip install selenium

#!pip install webdriver-manager
#!python -m pip install --upgrade pip


# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pymysql
import os


# In[ ]:





# In[11]:


#크롤링설정
options=webdriver.ChromeOptions()
#options.add_argument('window-size=1920,1080')
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#유저에이전트로 크롤링인거속이기
options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#크롤링시작
driver.get("https://search.namu.wiki/api/ranking")
#선택클릭
#driver.find_element(by=By.XPATH,value='//*[@placeholder="Search"]').click()
#driver.find_element(by=By.XPATH,value='/html/body').send_keys(Keys.TAB)
#driver.send_keys(Keys.TAB)
#대기5초
driver.implicitly_wait(time_to_wait=5)
#값받아오기
#드라이버닫기


ht=driver.page_source
driver.close()
db = pymysql.connect(
    user=os.environ.get('db_user') , 
    passwd=os.environ.get('db_pw'), 
    host=os.environ.get('db_host','127.0.0.1'), 
    db=os.environ.get('db_db'), 
    charset='utf8'
)
#커서생성
cursor = db.cursor(pymysql.cursors.DictCursor)


# In[13]:





# In[14]:


#검색결과삽입
sql="""insert into  test 
(new_tablecol)
values(%s)
"""
cursor.execute(sql,ht)
db.commit()