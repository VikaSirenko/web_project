from film import *
from bdConnection import *
from bson.objectid import ObjectId

coll=db.films

class FilmRepository:

    def getListOfFilms(self):
        all_films= coll.find()
        
        list_films=[]
        for film in all_films:
            _id=film["_id"]
            name=film["name"]
            year=film["year"]
            genre=film["genre"]
            directors=film["directors"]
            actors=film["actors"]
            duration=film["duration"]
            description=film["description"]
            web_film= Film(_id,name, year, genre, directors, actors, duration, description)
            list_films.append(web_film)
        
        
        return list_films


    def filmExist(self,filmName):
        query = {"name": filmName}
        film=coll.find_one(query)
        if(film!=None):
            return True
        else:
            return False
        

    def filmExistsById(self, filmId):
        query = {"_id": ObjectId(filmId)}
        film=coll.find_one(query)
        if(film!=None):
            return True
        else:
            return False


    def createFilm(self, film):
        if(self.filmExist(film.name)==False):
            new_film={ "name":film.name, "year":film.year, "genre":film.genre, "directors":film.directors, "actors":film.actors, "duration":film.duration, "description":film.description }
            result=coll.insert_one(new_film)
            return result.inserted_id
        else: 
            return None 


    def deleteFilm(self, filmId):
        result = coll.delete_one({'_id': ObjectId(filmId)})
        if(result.deleted_count==1):
            return True
        else:
            return False
    

    def editFilm(self, film):
        query = {'name': film.name}
        new_values = {'$set': {"name": film.name, "year": film.year, "genre":film.genre, "directors":film.directors, "actors":film.actors, "duration":film.duration, "description":film.description}}
        result = coll.update_one(query, new_values)
        if(result.modified_count==1):
            return "updated"
        else: 
            return "not updated"
