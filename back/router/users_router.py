from flask import Flask, request, jsonify, make_response
from bd.usersRepository import *
from bd.filmRepository import *
from bd.commentsRepository import * 
from entities.user import *
from entities.comment import *
from entities.film import *
from flask import copy_current_request_context
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY']="thisisthesecretkey"

connectionUser= UserRepository()
connectionFilm= FilmRepository()
connectionComment= CommentsRepository()
    




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")