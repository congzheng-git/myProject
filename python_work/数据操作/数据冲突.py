import pymongo
import random
from dateutil import parser
from mongo import mongodb
from mongo import re_pos_int
# from mongo import AntiEmpty



db = mongodb()
COLLECTION = 'user_data'
db_coll = db[COLLECTION]


def Main_input(_id):
	target = {'_id': int(_id)}
	User = db_coll.find_one(target)

	if User:
		Str_inp = input('输入1>模拟一次冲突； 其它>退出： ')
		if Str_inp:
			inp = int(Str_inp)
		conflict(inp, User, target)
	else:
		_id = input('未找到此ID，重新输入>')
		Main_input(_id)

def conflict(inp, User, target):
	if inp == 1:
		# 字符串z1转数组后改第4位的年份
		Str_z1 = User['z1']
		list_z1 = list(Str_z1)
		list_z1[3] = str(random.randint(0,9))
		Str_z1 = ''.join(list_z1)

		# 生成随机date，覆盖原有的'w'字段
		date_1 = '2018-01-11T'
		date_2 = str(random.randint(0,2)) + str(random.randint(0,3))
		date_3 = ':00:00.000Z'
		dateStr = date_1 + date_2 + date_3
		myDatetime = parser.parse(dateStr)

		# 更新
		User['w'] = myDatetime
		User['z1'] = Str_z1
		result = db_coll.update_one(target, {'$set': User})
		

		inp = re_pos_int(input('输入1>模拟一次冲突~ 其它>退出：'))
		conflict(inp, User, target)

	else:
		exit(1)


print('模拟一次冲突后，前端有所操作再login，触发数据冲突界面弹出')
_id = input("输入ID>")
Main_input(_id)