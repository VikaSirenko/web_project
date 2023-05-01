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
            return ("No such user exists"), 404
    except: 
        return "Unable to get token", 400


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =request.headers.get('authorization')

        if not token:
            return "Token is missing", 403
        try:
            data=jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            result = f(*args, **kwargs)
            return result[0], 200
        except:
            return "Token is invalid", 403
        
        
    return decorated



@app.route('/createComment', methods=['POST'])
@token_required
def createComment():
    try:
        content = request.form  
        comment= Comment(0, content['userId'], content['filmId'], content['text'])
        newId= connectionComment.createComment(comment, connectionFilm, connectionUser)
        if(newId==None):
            return  "Unable to create comment ", 404
        else:
            return "Comment created", 200
    except:
        return "It is not possible to create a comment", 404





@app.route('/createFilm', methods=['POST'])
@token_required
def createFilm():
    try:
        content = request.form 
        film= Film(0, content['name'], content['year'], content['genre'], content['directors'], content['actors'], content['duration'], content['description'])
        newId= connectionFilm.createFilm(film)
        if(newId==None):
            return  "A film with that name exists", 404
        else:
            return "Film created", 200
    except:
        return "It is not possible to create a film", 404



@app.route('/getFilms', methods=['GET'])
def getListOfFilms():
    try:
        all_films= connectionFilm.getListOfFilms()
        if(len(all_films)!=0):
            string_list = ""
            for film in all_films:
                string_list += film.name+": "+film.year+", "+film.genre+"\n"
            return string_list, 200
        else:
            return ("There is no films in the database"), 404
    except:
        return "It is impossible to get the list of films", 400



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


