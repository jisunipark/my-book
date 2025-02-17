# 유나님 / 지선
#appmain 디렉터리의 웹 서버가 실행될 때마다 함께 실행
#상품 정보 관리 기능의 초깃값을 설정하는 역할

import sqlite3

conn=sqlite3.connect('myBook.db')
cursor=conn.cursor()

#SQL 'DROP TABLE article'
#cursor.execute(SQL)

#상품 정보를 저장하기 위한 데이터베이스 테이블 생성
SQL = '''
CREATE TABLE IF NOT EXISTS articles (
    articleNo INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    category INTEGER,
    description TEXT,
    price INTEGER,
    picture TEXT
)
'''

cursor.execute(SQL)

cursor.close()
conn.close()