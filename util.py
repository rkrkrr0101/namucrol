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
    logRes = cursor.fetchall()
    return logRes


def deleteData(db, cursor):
    sql = """delete from namu_data"""
    cursor.execute(sql)

# todo:cc의존성 제거(주입시키자),for문 함수로 빼내기,테스트생성
# 그냥 리롤나무데이터 프록시씌운다음에 거기서 주입시키고,내부애들도 받는거넣으면될거같은데


def rerollNamuData(db, cursor, logRes):
    # 나무데이터 리셋
    deleteData(db, cursor)

    logDict = {}
    sql = """insert into  namu_data 
    (nd_one,nd_two,nd_three,nd_four,nd_five,nd_six,nd_seven,nd_eight,nd_nine,nd_ten,nd_kind)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    # 1시간 하루 이렇게 갯수세서 캐시에 넣기
    for logIndex, logData in enumerate(logRes):
        # 현재로우 값 딕셔너리에 추가
        logDict = dictMerge(logDict, sumRanking(logData))

        # 카운트에 해당하는 숫자일때(하루,한시간,일주일..) 정렬해서 인서트할 값 생성
        LogIncludeCount(cursor, sql, logIndex, logDict, cc.COUNT, cc.COUNTKIND)
    # 완료후 커밋
    db.commit()

# 이거 cc도 제거

# 여기서부턴 목업필요


def LogIncludeCount(cursor, sql, logIndex, logDict, count, countKind):
    # 현재 로그인덱스값이 count에 있으면
    if logIndex+1 in count:
        # 정렬해서 인서트할 값 생성
        logDataRes = namuDataCreate(logIndex, logDict, count, countKind)
        cursor.execute(sql, logDataRes)
        return True
    else:
        return False


def sumRanking(data):
    resDict = {}

    for countIndex, itemData in enumerate(data.items()):
        if (itemData[0] == 'na_time' or itemData[0] == 'id'):
            continue  # 실제 값이 아니면 패스
        # 해당 logDict에 값이 있으면 try,없으면 except
        try:
            resDict[itemData[1]] += 11-countIndex
        except:
            resDict[itemData[1]] = 11-countIndex
    return resDict

# 전체dic를 정렬후 10개고르고 현재kind추가


def namuDataCreate(countIndex, dic, count, countKind):
    # 정렬해서
    sortDict = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    resArray = []
    # 상위10개 insert
    for i in sortDict[:10]:
        resArray += [i[0]]
    # 카운트종류(hour,day...) 추가
    resArray += [countKind[count.index(countIndex+1)]]
    return resArray


def dictMerge(firstDict, secondDict):
    return dict(Counter(firstDict)+Counter(secondDict))
