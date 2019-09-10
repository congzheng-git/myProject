import pymongo
import time
from mongo import mongodb
from mongo import re_pos_int

db = mongodb()


def remove_all(*COLLECTION_olys):
	#清除活动所有用户数据
	for COLLECTION_oly in COLLECTION_olys:
		db_coll_oly = db[COLLECTION_oly]
		user_all = db_coll_oly.find()
		for user in user_all:
			re_target = user['_id']
			result = db_coll_oly.delete_one({'_id': re_target})
			print('所有用户限时活动相关mongo数据已被删除')


def award(COLLECTION_udata):
	# 模拟发奖
	db_coll_udata = db[COLLECTION_udata]
	_id = input('输入ID> ')
	int_id = {'_id': re_pos_int(_id)}
	user_find = db_coll_udata.find_one(int_id)
	if user_find:
		session = input('输入届数> ')
		user_find['x']['81'] = session
		user_find['x']['80'] = "1"

		result = db_coll_udata.update_one(int_id, {'$set': user_find})
		print('发奖第%s届第1名，login可见弹窗' %(session))
	else:
		print('未找到此ID，溜了溜了')
		exit(1)


def clear_medal(COLLECTION_udata):
	# 清除用户后端头像、奖章等信息
	db_coll_udata = db[COLLECTION_udata]
	_id = input('输入ID> ')
	int_id = {'_id': re_pos_int(_id)}
	user_find = db_coll_udata.find_one(int_id)
	if user_find:
		user_find['p1'] = []
		user_find['p2'] = []
		user_find['p3'] = []
		user_find['p4'] = []
		user_find['pp1'] = []
	else:
		print('未找到此ID，溜了溜了')
		exit(1)	

	result = db_coll_udata.update_one(int_id, {'$set': user_find})
	print('清除成功, 删包重装无头像、勋章')


	
# str_choice_oly = input('输入：1>删除活动相关所有用户的后台数据;\n      2>清除用户后台头像、勋章、套装信息;\n      3>模拟一次活动发奖弹窗> ')
choice_oly = re_pos_int(input('输入：1>删除活动相关所有用户的后台数据;\n      2>清除用户后台头像、勋章、套装信息;\n      3>模拟一次活动发奖弹窗> '))
if choice_oly == 1:
	remove_all("time_limit_user", "time_limit_rank_score", "time_limit_rank_backup", "time_limit_rank", "time_limit_garden_war")
elif choice_oly == 2:
	clear_medal('user_data')
elif choice_oly == 3:
	award('user_data')


