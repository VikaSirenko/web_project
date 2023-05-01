class Film(object):
    _id=""
    name=""
    year=""
    genre=""
    directors=""
    actors=""
    duration=""
    description=""


    def __init__(self, _id, name, year, genre, directors, actors, duration, description):
        self._id=_id
        self.name= name
        self.year=year
        self.genre=genre
        self.directors=directors
        self.actors=actors
        self.duration=duration
        self.description=description
