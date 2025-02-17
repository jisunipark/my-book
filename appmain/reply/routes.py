from flask import Blueprint, request, make_response, jsonify
import sqlite3
from appmain import app
from appmain.utils import veryfyJWT, getJWTContent
reply = Blueprint('reply', __name__)

#댓글을 저장
