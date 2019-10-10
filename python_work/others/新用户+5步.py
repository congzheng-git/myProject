import pymongo
import time

# mongodb服务的地址和端口号
mongo_url = "172.16.0.111:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)

# 连接到数据库myDatabase
DATABASE_NUM = int(input("选择服务器--1国内安卓，2国内IOS，3海外:"))
if DATABASE_NUM == 1:
	DATABASE = "jelly_new_dev"
elif DATABASE_NUM == 2:
	DATABASE = "jelly_new_dev2"
elif DATABASE_NUM == 3:
	DATABASE = "jelly_new_dev3"

db = client[DATABASE]

# 连接到集合(表):myDatabase.myCollection
COLLECTION_1 = "add_step_user"
db_coll_1 = db[COLLECTION_1]

_id = input("哪个ID：")
_type = input("改成哪个类型：1.免费，2.五折，3.正常：")
# 检索目标
target = {'_id': int(_id)}
user_1 = db_coll_1.find_one(target)

if int(_type) == 1:
	user_1['a'] = 1
	print(user_1['a'])
elif int(_type) == 2:
	user_1['a'] = 2
elif int(_type) == 3:
    user_1['a'] = 3


result = db_coll_1.update_one(target, {'$set': user_1})
print("修改成功")
time.sleep(1)
