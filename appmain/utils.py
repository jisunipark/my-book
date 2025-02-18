# 예지님 
# 유나님 / 지선
import jwt
import sqlite3

from appmain import app

# 로그인 토큰을 보낸 사용자가 현재 로그인한 사용자가 맞는지 확인한다.
def verifyJWT(token):
  if token is None:
    return None
  else :
    try :
      decodedToken = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
      if decodedToken:
        conn = sqlite3.connect('myBook.db')
        cursor = conn.cursor()

        if cursor :
          SQL = 'SELECT authkey FROM users WHERE email=?'
          cursor.execute(SQL, (decodedToken["email"],))
          authkey = cursor.fetchone()[0]
          cursor.close()
        conn.close()

        if authkey == decodedToken["authkey"]:
          return True
        else :
          return None
      else :
        return None
    except :
      return None
    
# JWT 토큰을 해석하고 '키-값'의 쌍으로 이루어진 해석된 로그인 토큰을 반환한다.
def getJWTContent(token):
  isVerified = verifyJWT(token)

  if isVerified:
    return jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
  else:
    return None