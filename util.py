import pymysql
import os
import constcount as cc
from collections import Counter


def insertLog(db, cursor, res):
    sql = """insert into  namu_log 
    (na_one,na_two,na_three,na_four,na_five,na_six,na_seven,na_eight,na_nine,na_ten)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, res)
    db.commit()


def selectLog(db, cursor):
    sql = """select * from namu_log
    order by na_time DESC LIMIT 1440
    """
    cursor.execute(sql)
    logres = cursor.fetchall()
    return logres


#todo:cc의존성 제거(주입시키자)
def rerollNamuData(db, cursor, logres):
    # 나무데이터 리셋
    sql = """delete from namu_data"""
    cursor.execute(sql)

    logdic = {}
    sql = """insert into  namu_data 
    (nd_one,nd_two,nd_three,nd_four,nd_five,nd_six,nd_seven,nd_eight,nd_nine,nd_ten,nd_kind)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    # 1시간 하루 이렇게 갯수세서 캐시에 넣기
    for logindex, logdata in enumerate(logres):        
        #현재로우 값 딕셔너리에 추가
        logdic=dictMerge(logdic,sumRanking(logdata))

        # 카운트에 해당하는 숫자일때(하루,한시간,일주일..)
        if logindex+1 in cc.count:
            # 정렬해서 인서트할 값 생성          
            logDataRes=namuDataCreate(logindex,logdic)
            cursor.execute(sql, logDataRes)
    db.commit()
    # rerollNamuData 분리,테스트코드작성,테스트코드 작성 편하게 분리하면될듯
    # 바깥쪽for문, 안쪽for문이랑 if문 이렇게 분리하면될거같다


def sumRanking(data):
    resDict = {}
    for countindex, itemdata in enumerate(data.items()):
        if (itemdata[0] == 'na_time' or itemdata[0] == 'id'):
            continue  # 실제 값이 아니면 패스
        # 해당 logdic에 값이 있으면 try,없으면 except
        try:
            resDict[itemdata[1]] += 11-countindex
        except:
            resDict[itemdata[1]] = 11-countindex
    return resDict

def namuDataCreate(countIndex,dic):
    # 정렬해서
    sortdic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    resArray = []
    # 상위10개 insert
    for i in sortdic[:10]:
        resArray += [i[0]]
    # 카운트종류(hour,day...) 추가
    resArray += [cc.countkind[cc.count.index(countIndex+1)]]
    return resArray
            

def dictMerge(firstDict,secondDict):
    return dict(Counter(firstDict)+Counter(secondDict))