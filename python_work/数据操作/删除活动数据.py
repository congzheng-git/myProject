import pymongo
import time
from mongo import mongodb
from mongo import re_pos_int

db = mongodb()

def delete_target(COLLECTION, *depends):

	db_coll = db[COLLECTION]
	_id = input("删哪个ID> ")
	target = {'_id': re_pos_int(_id)}
	result_find = db_coll.find_one(target)
	# print(db_coll.find()[0])

	if result_find:
		result = db_coll.delete_one(target)
		print("删除成功")
		time.sleep(1)
	else:
		print("未找到此ID,重新输入> ")
		delete_target(COLLECTION)

	for depend in depends:
		
		db_coll = db[depend]
		depend_find = db_coll.find_one(target)

		# 删除排行榜等表单中此UserID的相关数据(找到了就删，找不到进娃娃机逻辑)
		# 不够严谨，限时活动有的表单没找到东西也会走elif
		if depend_find:
			result = db_coll.delete_one(target)

		# 娃娃机活动，teamID=日期+UserID，删除team中个人信息
		# 'b'字段是每个id的队伍id
		elif result_find['b'] != 0:


			# 队伍相关信息
			target_team = {'_id': result_find['b']}
			find_team = db_coll.find_one(target_team)
			# 能找到队伍就是娃娃机活动，找不到就是其它不用动的活动数据(比如限时活动其它depends)
			if find_team:
				# 一个人一队就删队，否则只删自己
				if isinstance(find_team['a'], dict):
					if len(find_team['a']) != 1:
						del find_team['a'][_id]
						result = db_coll.update_one(target_team, {'$set': find_team})
					else:
						result = db_coll.delete_one(find_team) 
				# 单人则同时再删掉not_full队伍
				elif find_team['a'] == 1:
					result = db_coll.delete_one(find_team)


def Del_data(_activity):	

	if _activity == 1:
		delete_target("inspire_bank_user")

	elif _activity == 2:
		delete_target("inspire_user_job")

	elif _activity == 3:
		delete_target("prize_claw_user", "prize_claw_team", "prize_claw_not_full_team")

	elif _activity == 4:
		delete_target("time_limit_user", "time_limit_rank_score", "time_limit_rank_backup", "time_limit_rank", "time_limit_garden_war")

	elif _activity == 5:
		delete_target("toy_user_job")

	elif _activity == 6:
		delete_target("new_mission_user")

	elif _activity == 7:
		delete_target("new_task_user")

	elif _activity == 8:
		delete_target("camp_war_user")

	else:
		_activity = int(input("输错了，重新输入> "))
		Del_data(_activity)

_activity = int(input("删什么活动：1.星星银行，2.宝箱激励，3.娃娃机，4.限时活动，5.玩具之家，6组队任务，7.迎新会, 8.阵营战> "))
Del_data(_activity)
