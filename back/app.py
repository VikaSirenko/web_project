from flask import Flask, request, jsonify, make_response
from usersRepository import *
from filmRepository import *
from commentsRepository import * 
from user import *
from comment import *
from film import *
from flask import copy_current_request_context
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY']="thisisthesecretkey"

connectionUser= UserRepository()
connectionFilm= FilmRepository()
connectionComment= CommentsRepository()
    


@app.route('/registration', methods=['POST'])
def registration():
    try:
        content = request.form
        student= User(0, content['firstName'], content['lastName'], content['email'], content['password'])
        newId= connectionUser.createUser(student)
        if(newId==None):
            return  "User with that email exists ", 404
        else:
            return "User created", 200
    except:
        return "It is not possible to create a new user", 404



@app.route('/signIn', methods=['GET'])
def signIn():
    try:
        content = request.form
        email = content['email']
        password=content['password']
        exist=connectionUser.userExistForSignIn(email, password)
        if(exist):
            token=jwt.encode({'email':email, 'password':password, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(hours=24)}, app.config["SECRET_KEY"])
            return token, 200
        else:
            return ("There is no student with this username"), 404
    except: 
        return "Unable to get token", 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")