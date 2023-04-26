import pymongo 

client = pymongo.MongoClient("mongodb+srv://VikaSirenko:16842778@cluster0.8kq1ltu.mongodb.net/?retryWrites=true&w=majority")
db = client.project