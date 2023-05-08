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


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =request.headers.get('authorization')

        if not token:
            return "Token is missing", 403
        try:
            data=jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if (data['email']=='vika_sirenko@gmail.com' and hashlib.sha256(data['password'].encode()).hexdigest()=='03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'):
                result = f(*args, **kwargs)
                return result[0], 200
            else:
                return "You do not have administrator rights to perform this action", 403
        except:
            return "Token is invalid", 403
        
    return decorated


@app.route('/createComment', methods=['POST'])
@token_required
def createComment():
    try:
        user_data=request.headers.get('authorization')
        data=jwt.decode(user_data, app.config['SECRET_KEY'], algorithms=['HS256'])
        user=connectionUser.getUserByEmail(data['email'])
        content = request.form  
        comment= Comment(0, user['_id'], content['filmId'], content['text'])
        newId= connectionComment.createComment(comment, connectionFilm, connectionUser)
        if(newId==None):
            return  "Unable to create comment ", 404
        else:
            return "Comment created", 200
    except:
        return "It is not possible to create a comment", 404




@app.route('/createFilm', methods=['POST'])
@admin_token_required
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



@app.route('/getComments', methods=['GET'])
def getListOfComments():
    try:
        content = request.form 
        all_comments= connectionComment.getListOfFilmComments(content["filmId"])
        if(len(all_comments)!=0):
            string_list = ""
            for comment in all_comments:
                user=connectionUser.getUserById(comment.userId)
                userName=user['firstName']+" "+user["lastName"]
                string_list += userName+": "+comment.text+"\n"
            return string_list, 200
        else:
            return ("There are no comments for this movie"), 404
    except:
        return "It is impossible to get the list of comments", 400
    



@app.route('/deleteFilm', methods=['DELETE'])
@admin_token_required
def deleteFilm():
    try:
        content = request.form 
        result=connectionFilm.deleteFilm(content['_id'])
        if (result):
                connectionComment.deleteAllFilmComments(content["_id"])
                return "Deleted", 200
        else:
                return ("Cannot find film to delete"), 404
    except:
        return "Can not delete", 400
    



@app.route('/deleteComment', methods=['DELETE'])
@admin_token_required
def deleteComment():
    try:
        content = request.form 
        result=connectionComment.deleteComment(content['_id'])
        if (result):
                return "Deleted", 200
        else:
                return ("Cannot find comment to delete"), 404
    except:
        return "Can not delete", 400



@app.route('/editFilm', methods=['PUT'])
@admin_token_required
def editFilm():
    try:
        content = request.form 
        old_name=content['oldName']
        film= Film(0, content['name'], content['year'], content['genre'], content['directors'], content['actors'], content['duration'], content['description'])
        result= connectionFilm.editFilm(old_name, film)
        if(result=='updated'):
            return  "Film data has been updated", 200
        else:
            return "Film data has not been updated", 404
    except:
        return "Unable to update movie data", 404




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


