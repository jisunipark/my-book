# 유나님 / 지선
#상품 등록 페이지 연결
#상품 데이터를 보낸 사용자가 인증된 사용자인지 검증
#상품 정보 저장

from flask import Blueprint, send_from_directory, make_response,jsonify,request
import sqlite3

from appmain import app
from appmain.utils import verifyJWT, getJWTContent, savePic

article = Blueprint('article',__name__)

@article.route('/create_article')
def createArticlePage():
    return send_from_directory(app.root_path, 'templates/create_article.html')

@article.route('/api/article/create',methods=['POST'])
def createArticle():
            
    headerData = request.headers
    data = request.form #HTTP 요청의 본문 데이터를 가져온다
    files = request.files #업로드 파일 객체
    
    authToken = headerData.get("authtoken") #사용자 인증
    
    payload = {"success":False}
    
    if authToken:
        isValid = getJWTContent(authToken)
        
        if isValid:
            token = getJWTContent(authToken)
            username = token["username"]
        
            category = data.get("category")
            title = data.get("title")
            desc = data.get("desc")
            price = data.get("price")
            
            #"picture" 키이름의 첨부 파일
            if files:
                #print('createArticle.files', files)
                picFileName = savePic(files["picture"],username)
            
                #업로드 데이터 파일 디버깅 코드
                #print('createArticle.username',username)
                #print('createArticle.category',category)
                #print('createArticle.title',title)
                #print('createArticle.desc',desc)
                
                conn = sqlite3.connect('myBook.db')
                cursor = conn.cursor()
                
                if cursor:
                    if files:
                        SQL = 'INSERT INTO articles (author, title, category,description, price, picture) \
                            VALUES (?,?,?,?,?,?)'
                        cursor.execute(SQL, (username,title,category,desc,price,picFileName))
                    else:
                        SQL = 'INSERT INTO articles (author, title, category, description, price) \
                            VALUES (?,?,?,?,?)'
                        cursor.execute(SQL,(username, title, category, desc, price))
                    rowID = cursor.lastrowid
                    conn.commit()
                
                    #동작 확인용 디버깅 코드
                    #SQL = 'SELECT * FROM articles'
                    #cursor.execute(SQL)
                    #rows = cursor.fetchall()
                    #for row in rows:
                    #    print(row)
                
                    cursor.close()
                conn.close()
            
                payload = {"success": True, "articleNo":rowID}
            else:
                pass
        else:
            pass
    
    return make_response(jsonify(payload),200)

#페이지 서비스의 첫페이지를 이용
#요청받고 데이터를 전송하는 API 엔드포인트 처리 함수 작성
@article.route('/api/article/recent', methods=['GET'])
def getRecentArticles():
    payload = {"success":False}
    
    conn = sqlite3.connect('myBook.db')
    cursor = conn.cursor()
    
    if cursor:
        SQL = 'SELECT articleNo, author, title, category, description, price, picture FROM articles ORDER BY articleNo DESC LIMIT 6'
        cursor.execute(SQL)
        result = cursor.fetchall()
        cursor.close()
    conn.close()
    
    recentArticleDics=[]
    
    if len(result) > 0:
        for article in result:
            recentArticleDics.append({"articleNo":article[0], "title":article[2],"desc":article[4]})
            
            payload = {"success":True, "article":recentArticleDics}
        
        return make_response(jsonify(payload), 200)