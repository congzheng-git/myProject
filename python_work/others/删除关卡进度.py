import pymongo
import time
from mongo import mongodb

db = mongodb()

# 连接到集合(表):myDatabase.myCollection
COLLECTION_1 = "user_data"
COLLECTION_2 = "user_level"
db_coll_1 = db[COLLECTION_1]
db_coll_2 = db[COLLECTION_2]

_id = input("删哪个ID：")
_level = input("删到多少关：")

# 检索目标并修改关卡数据
target = {'_id': int(_id)}

user_1 = db_coll_1.find_one(target)
user_1['r'] = int(_level)

user_2 = db_coll_2.find_one(target)
if int(_level) == 0:
	user_2['a'] = {}	
else:
	user_2['a'] = {}
	user_2['a'][_level] = "400000_3"



result = db_coll_1.update_one(target, {'$set': user_1})
result = db_coll_2.update_one(target, {'$set': user_2})
print("删除成功")
time.sleep(1)