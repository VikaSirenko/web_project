from comment import *
from bdConnection import *
import sys
sys.path.append('/.../web_project/entities')
import comment


coll=db.comments

class CommentsRepository:

    def getListOfFilmComments(self, filmId):
        field_name = 'fimlId'
        query = {field_name: {'$exists': True}}
        film_comments = coll.find(query)
        
        list_comments=[]
        for comment in film_comments:
            _id=comment["_id"]
            userId=comment["userId"]
            filmId= comment["filmId"]
            text=comment["text"]
            
            filmComment= Comment(_id,userId, filmId, text)
            list_comments.append(filmComment)
        
        return list_comments


    def createComment(self, comment,filmConnection, userConnection):
        if(userConnection.userExistsById(comment.userId)==True and  filmConnection.filmExistsById(comment.filmId)==True):
            new_comment={ "userId": comment.userId, "filmId":comment.filmId, "text": comment.text}
            result=coll.insert_one(new_comment)
            return result.inserted_id
        else: 
            return None 


    def deleteComment(self, commentId):
        result = coll.delete_one({'_id': commentId})
        if(result.deleted_count==1):
            return "deleted"
        else:
            return "not deleted"
    

