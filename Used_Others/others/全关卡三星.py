import pymongo
import time
from mongo import mongodb
from mongo import re_pos_int


dbData = mongodb()

# 连接到集合(表):myDatabase.myCollection
COLLECTION_DATA = "user_data"
COLLECTION_LEVEL = "user_level"
db_coll_data = dbData[COLLECTION_DATA]
db_coll_level = dbData[COLLECTION_LEVEL]

_id = input("改哪个ID：")
_level = input("最大关卡数> ")

# 检索目标并修改关卡数据
target = {'_id': int(_id)}
udata = db_coll_data.find_one(target)
# 用户最大关卡数字段
udata['r'] = int(_level)


ulevel = db_coll_level.find_one(target)
ulevel['a'] = {}

isGold = input('1.关卡全金；2.非金卡座> ')
int_isGold = re_pos_int(isGold)
if int_isGold == 1:
	for  i  in range(1, int(_level) + 1):		
		ulevel['a'][str(i)] = "400000_3_1"
else:
	ulevel['a']['1'] = "400000_3_1"
	for  i  in range(2, int(_level) + 1):		
		ulevel['a'][str(i)] = "400000_3"


result = db_coll_data.update_one(target, {'$set': udata})
result = db_coll_level.update_one(target, {'$set': ulevel})

print("修改成功")
time.sleep(1)