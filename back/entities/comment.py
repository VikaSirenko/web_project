class Comment(object):
    _id=""
    userId=""
    filmId=""
    text=""


    def __init__(self, _id, userId, filmId, text):
        self._id=_id
        self.userId=userId
        self.filmId=filmId
        self.text=text

 