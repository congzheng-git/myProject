import pymongo

# mongodb服务的地址和端口号
mongo_url = "172.16.0.111:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)
#连接到数据库myDatabase
DATABASE = "jelly_new_dev2"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "zzzz"
db_coll = db[COLLECTION]

student = {
    '_id': '10101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

result = db_coll.insert_one(student)
print(result)