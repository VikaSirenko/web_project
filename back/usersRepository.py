from user import *
from bdConnection import *


coll=db.users

class UserRepository:

    def getListOfUsers(self):
        all_users= coll.find()
        
        list_users=[]
        for user in all_users:
            _id=user["_id"]
            firstName=user["firstName"]
            lastName=user["lastName"]
            email=user["email"]
            password=user["password"]
            web_user= User(_id,firstName, lastName, email, password)
            list_users.append(web_user)
        
        return list_users


    def userExist(self,userEmail):
        query = {"email": userEmail}
        user=coll.find_one(query)
        if(user!=None):
            return True
        else:
            return False
        
    def userExistsById(self, userId):
        query = {"_id": userId}
        user=coll.find_one(query)
        if(user!=None):
            return True
        else:
            return False


    def createUser(self, user):
        if(self.userExist(user.email)==False):
            new_user={ "firstName":user.firstName, "lastName":user.lastName, "email":user.email, "password": user.password}
            result=coll.insert_one(new_user)
            return result.inserted_id
        else: 
            return None 

    
