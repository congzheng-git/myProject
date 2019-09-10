import pymongo
import time
import random
from dateutil import parser
import mongo


db = mongo.db_default()

# target = {'_id': 11110}
target = input('输入目标ID> ')
udata = get_udata()
ulevel = get_ulevel()
revised = []

# 确认目标存储，获得ID信息
def get_udata(target):
	udata = db['user_data'].find_one(target)
	if udata:
		return udata
	else:
		target = input('没找到，重新输入> ')
		get_udata(target)
def get_ulevel(target):
	ulevel = db['user_level'].find_one(target)
	if ulevel:
		return ulevel
	else:
		target = input('没找到，重新输入> ')
		get_ulevel(target)

# 变更数据内容
def revise(revised, *datas):
	# 修改目标内容
	for data in datas:
		revised.append(data)
	return revised

#删除关卡进度
def delete_level(udata, ulevel, revised):
	
	_level = mongo.re_pos_int(input('要删到多少关> '))
	udata['r'] = int(_level)
	if int(_level) == 0:
		ulevel['a'] = {}	
	else:
		ulevel['a'] = {}
		ulevel['a'][str(_level)] = "400000_3"
	revised = revise(revised, ulevel, udata)
	print('删除成功')
	time.sleep(1)
	return revised

# 全关卡三星
def All_stars(udata, ulevel, revised):
	_level = mongo.re_pos_int(input('最大关卡数> '))
	udata['r'] = int(_level)	
	# 金卡座？
	isGold = mongo.re_pos_int(input('1.关卡全金；2.非金卡座> '))
	if isGold == 1:
		for  i  in range(1, int(_level) + 1):		
			ulevel['a'][str(i)] = "400000_3_1"
	else:
		ulevel['a']['1'] = "400000_3_1"
		for  i  in range(2, int(_level) + 1):		
			ulevel['a'][str(i)] = "400000_3"
	revised = revise(revised, ulevel, udata)
	return revised
	print('修改成功')
	time.sleep(1)

# 删除活动数据	
def delete_activity():
	_activity = mongo.re_pos_int(input("删什么活动：1.星星银行，2.宝箱激励，3.娃娃机，4.限时活动，5.玩具之家，6组队任务，7.迎新会> "))
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

	else:
		_activity = mongo.re_pos_int(input("输错了，重新输入> "))
		Del_data(_activity)
	
	pass
def delete_target(COLLECTION, *depends):

	db_coll = db[COLLECTION]
	_id = input("删哪个ID> ")
	target = {'_id': mongo.re_pos_int(_id)}
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

# 增加背包道具
def increase_item(udata, revised):
	udata['q']['1_1'] = 5000
	udata['q']['4_101'] = 500
	udata['q']['4_102'] = 500
	udata['q']['4_103'] = 500
	udata['q']['4_104'] = 500
	udata['q']['11_1'] = 101
	udata['q']['11_2'] = 101
	udata['q']['11_3'] = 101
	revised = revise(revised, udata)
	return revised
	print('道具增加成功')
	time.sleep(1)

# 指定组队任务
def new_task():
	_mission = mongo.re_pos_int(input("指定任务：1.过2关、2.2个星星、3.1000红糖果、4.买礼包、5.买金砖、6.40个特效\n7.3个关卡内道具、8.关卡前道具、9.花100金砖、10.消耗50彩虹\n11.1500蓝糖果、12.1100黄糖果、13.1200绿糖果、14.1300橙糖果、15.消60硬糖\n21.玩具之家、22.限时活动、23.娃娃机："))
	utask = db['new_mission_user'].find_one(target)
	# 修改d字段下字符串a的首位,并清除任务信息
	_missionTime = str(utask['d']['e'])
	_newMisson = str(_mission) + '_' + _missionTime
	utask['d']['a'] = str(_newMisson)
	utask['d']['b'] = None
	utask['d']['f'], utask['d']['g'], utask['d']['i'] = 0, 0, 0
	utask['d']['h'], utask['d']['k'] = 1, 1
	utask['d']['j'] = 2

	result = db['new_mission_user'].update_one(target, {'$set': utask})
	print("修改成功")
	time.sleep(1)

# 模拟数据冲突
def data_confilict(udata, target):
	inp = mongo.re_pos_int(input('输入1>模拟一次冲突； 其它>退出： '))
	confilict(inp, udata, target)
def confilict(inp, udata, target):
	if inp == 1:
		# 字符串z1转数组后改第4位的年份
		Str_z1 = udata['z1']
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
		udata['w'] = myDatetime
		udata['z1'] = Str_z1
		result = db['user_data'].update_one(target, {'$set': udata})
		
		
		inp = mongo.re_pos_int(input('输入1>模拟一次冲突~ 其它>退出：'))
		confilict(inp, udata, target)
	else:
		exit(1)
	pass
# 创建新ID
def data_newID():
	
	pass
# 限时活动相关
def timelimit_Act():
	pass





# # revised = delete_level(udata, ulevel, revised)
# revised = All_stars(udata, ulevel, revised)
# delete_activity()
# increase_item(udata, revised)\
# new_task()
# data_confilict(udata, target)

if len(revised) == 2:
	re_ulevel = revised[0]
	re_udata = revised[1]
	result = db['user_level'].update_one(target, {'$set': re_ulevel})
	result = db['user_data'].update_one(target, {'$set': re_udata})
elif len(revised) == 1:
	re_udata = revised[0]
	result = db['user_data'].update_one(target, {'$set': re_udata})


