# 예지님
from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3
import bcrypt     # 비밀번호 암호화
import secrets
import jwt


from appmain import app
user = Blueprint('user', __name__)

@user.route('/signup')
def signUp():
  return send_from_directory(app.root_path, 'templates/signup.html')

@user.route('/api/user/signup', methods=['POST'])
def register():
  # request 객체는 클라이언트의 요청을 담고 있다.
  # request 객체의 요소인 form 객체에는 요청의 본문(body)이 들어있다.
  data = request.form

  username = data.get("username")
  email = data.get("email")
  passwd = data.get("passwd")

  # 암호화
  hashedPW = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

  conn = sqlite3.connect('myBook.db')
  cursor = conn.cursor()

  if cursor:
    SQL = 'INSERT INTO users (username, email, passwd) VALUES (?, ?, ?)'
    cursor.execute(SQL, (username, email, hashedPW))
    conn.commit()

    SQL = 'SELECT * FROM users'
    cursor.execute(SQL)
    rows = cursor.fetchall()
    for row in rows:
      print(row)

    cursor.close()
  conn.close()

  payload = {"success": True}
  return make_response(jsonify(payload), 200)

@user.route('/signin')
def signIn():
  return send_from_directory(app.root_path, 'templates/signin.html')

@user.route('/api/user/signin', methods=['POST'])
def getAuth():
  # 클라이언트가 전달한 데이터를 얻는다.
  data = request.form

  email = data.get("email")
  passwd = data.get("passwd")

  # 데이터베이스에 저장되어 있는 비밀번호와 일치하는지 확인한다.
  conn = sqlite3.connect('myBook.db')
  cursor = conn.cursor()

  payload = {"authenticated": False, "email": '', "username": '', "authtoken": ''}

  if cursor:
    SQL = 'SELECT id, username, passwd FROM users WHERE email=?'
    cursor.execute(SQL, (email,))
    result = cursor.fetchone()    # 먼저 출력되는 데이터를 가져온다.

    # result[0] : 사용자 고유 Id, result[1] : 사용자 이름, result[2] : 비밀번호

    if result:
      pwMatch = bcrypt.checkpw(passwd.encode('utf-8'), result[2])
      id = result[0]
      username = result[1]
    else :
      pwMatch = None
    
    # 로그인 토큰을 생성한다.
    if pwMatch:
      authkey = secrets.token_hex(16)

      SQL = 'UPDATE users SET authkey=? WHERE id=?'
      cursor.execute(SQL, (authkey, id))
      conn.commit()

      # jwt.encode(토큰에 포함할 정보, 서명, 암호화 방법)
      token = jwt.encode({"id": id, "email": email, "username": username, "authkey": authkey}, app.config["SECRET_KEY"], algorithm='HS256')
      payload = {"authenticated": True, "email": email, "username": username, "authtoken": token}

      # print('user.signin: %s' % email)
    else :
      pass

    cursor.close()
  conn.close()

  # 응답을 클라이언트에게 전달한다.
  return make_response(jsonify(payload), 200)