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
driver.get("https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8")
#선택클릭
driver.find_element(by=By.XPATH,value='//*[@placeholder="Search"]').click()
#대기5초
driver.implicitly_wait(time_to_wait=5)
#값받아오기
ta=driver.find_element(by=By.XPATH,value='/html/body/div/div/div[1]/nav/form/div/div/div')
#결과값자르기
res=ta.text.split('\n')
#드라이버닫기
driver.close()


# In[2]:


#디비연결
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
sql="""insert into  namu_log 
(na_one,na_two,na_three,na_four,na_five,na_six,na_seven,na_eight,na_nine,na_ten)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
cursor.execute(sql,res)
db.commit()


# In[15]:


#한달치 데이터 긁어오기
sql="""select * from namu_log
order by na_time DESC LIMIT 8640
"""
cursor.execute(sql)
logres=cursor.fetchall()


# In[21]:


#현재 캐시데이터 삭제
sql="""delete from namu_data"""
cursor.execute(sql)
db.commit()


# In[27]:


# i+1 12,288,2016,8640
#사전작업
logdic={}
sql="""insert into  namu_data 
(nd_one,nd_two,nd_three,nd_four,nd_five,nd_six,nd_seven,nd_eight,nd_nine,nd_ten,nd_kind)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
#count=[3,4,5,12]
#여기적힌거갯수일때 작동
count=[12,288,2016,8640]
countkind=['hour','day','week','month']

#1시간 하루 이렇게 갯수세서 캐시에 넣기
for logindex,logdata in enumerate (logres):
    
    for countindex,itemdata in enumerate(logdata.items()):
        if (itemdata[0]== 'na_time' or itemdata[0]=='id'):
            continue
#        print(countindex,itemdata[0])
        try:
            logdic[itemdata[1]]+=11-countindex
        except:
            logdic[itemdata[1]]=11-countindex
    if logindex+1 in count:
        sortdic=sorted(logdic.items(),key=lambda x:x[1],reverse=True)
        logdatares=[]
        for i in sortdic[:10]:           
            logdatares+=[i[0]]
        logdatares+=[countkind[count.index(logindex+1) ]]

        cursor.execute(sql,logdatares)
        db.commit()
     


# In[24]:





# In[ ]:




