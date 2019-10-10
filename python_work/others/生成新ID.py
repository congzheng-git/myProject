import pymongo
import time
from mongo import mongodb

db = mongodb()

COLLECTION = "user_info"
db_coll = db[COLLECTION]


_id = input("哪个ID：")
target = {'_id': int(_id)}

user = db_coll.find_one(target)
# print('a' in user.keys())
# if user['a']:
if 'a' in user.keys():
	user['a'] += '_zxc'
	user['b'] += '_qwe'
else:
 	print('直接删包重装')

result = db_coll.update_one(target, {'$set': user})


def new_ID():

	newTarget = {'_id': int(_id) + 1}
	new_user = db_coll.find_one(newTarget)
	newID = int(_id) + 1

	# 检索新生成的ID 
	while new_user:
		newID += 1
		new_user = db_coll.find_one({'_id': newID})		
		
	return(newID)



print("旧ID已注销,删包重装将得到的ID是:", new_ID())


time.sleep(1)
