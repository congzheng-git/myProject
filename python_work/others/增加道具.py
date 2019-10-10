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
COLLECTION_1 = "circus_user"
db_coll_1 = db[COLLECTION_1]
COLLECTION_2 = 'circus_team'
db_coll_2 = db[COLLECTION_2]
_id = input("哪个ID：")
# 检索目标
target = {'_id': int(_id)}
user_1 = db_coll_1.find_one(target)
a = user_1['b']

target_team = {'_id': a}

print(db_coll_2.find_one(target_team))

# print(user_1['b'])

# user_1['q']['1_1'] = 5000
# user_1['q']['4_101'] = 500
# user_1['q']['4_102'] = 500
# user_1['q']['4_103'] = 500
# user_1['q']['4_104'] = 500
# user_1['q']['11_1'] = 101
# user_1['q']['11_2'] = 101
# user_1['q']['11_3'] = 101


# result = db_coll_1.update_one(target, {'$set': user_1})
# print("增加成功")
# time.sleep(1)
