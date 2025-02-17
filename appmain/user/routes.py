# 예지님
from flask import Blueprint, send_from_directory, make_response, jsonify, request
import sqlite3
import bcrypt     # 비밀번호 암호화

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