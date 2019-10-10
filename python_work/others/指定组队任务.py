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
COLLECTION = "new_mission_user"
db_coll = db[COLLECTION]

def change_mission(target):
	_mission = input("指定任务：1.过2关、2.2个星星、3.1000红糖果、4.买礼包、5.买金砖、6.40个特效\n、7.3个关卡内道具、8.关卡前道具、9.花100金砖、10.消耗50彩虹\n11.1500蓝糖果、12.1100黄糖果、13.1200绿糖果、14.1300橙糖果、15.消60硬糖\n21.玩具之家、22.限时活动、23.娃娃机：")

	# 检索目标并修改任务内容
	user = db_coll.find_one(target)

	# 修改d字段下字符串a的首位,并清除任务信息
	_missionTime = str(user['d']['e'])
	_newMisson = str(_mission) + '_' + _missionTime
	user['d']['a'] = str(_newMisson)
	user['d']['b'] = None
	user['d']['f'], user['d']['g'], user['d']['i'] = 0, 0, 0
	user['d']['h'], user['d']['k'] = 1, 1
	user['d']['j'] = 2

	result = db_coll.update_one(target, {'$set': user})
	print("修改成功")
	time.sleep(1)

_id = input("哪个ID：")
target = {'_id': int(_id)}
result_find = db_coll.find_one(target)
if result_find:
	change_mission(target)
else:
	print("不存在此ID,重新输")
	_id = input("哪个ID：")
	target = {'_id': int(_id)}
	change_mission(target)

