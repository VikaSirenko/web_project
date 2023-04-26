import hashlib

class User(object):
    _id=""
    firstName=""
    lastName=""
    email=""
    password=""


    def __init__(self, _id, firstName, lastName, email, password):
        self._id=_id
        self.firstName=firstName
        self.lastName=lastName
        self.email=email
        self.password=self._passwordHashing(password)

    
    def _passwordHashing(self,  password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password