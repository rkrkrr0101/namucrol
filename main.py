import pymysql
import os
from dotenv import load_dotenv
import crol
import util
load_dotenv(verbose=True)

# 크롤링
res = crol.namuCrol()  # None반환하면 에러,정상반환은 Str
if res is None:
    print("에러")
    quit()

# 결과값자르기
res = crol.toReplace(res)


# 디비연결
db = pymysql.connect(
    user=os.environ.get('db_user'),
    passwd=os.environ.get('db_pw'),
    host=os.environ.get('db_host', '127.0.0.1'),
    db=os.environ.get('db_db'),
    charset='utf8'
)
# 커서생성
cursor = db.cursor(pymysql.cursors.DictCursor)

# 검색결과삽입
util.insertLog(db, cursor, res)

# 한달치 데이터 긁어오기
logres = util.selectLog(db, cursor)

# 현재 캐시데이터 삭제후 재삽입
util.rerollNamuData(db, cursor, logres)
