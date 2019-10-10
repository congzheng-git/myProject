from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb
import random
import lib.userInfo


"""给马戏团活动添加10个假人"""


class circusDummys(lib.userInfo.getUserInfo):

	def __init__(self, userid):
		super(circusDummys, self).__init__(userid)

		self.db_circus = self.serverDb['circus_user']
		self.db_circusTeam = self.serverDb['circus_team']
		self.ucircus = self.db_circus.find_one(self.target)


	def circusDummys(self):
		if self.ucircus:
			tcircus = self.ucircus['b']
			tcircus_target = {'_id': tcircus}
			tcircus_find = self.db_circusTeam.find_one(tcircus_target)
			if tcircus_find:
				for i in range(0, 10):
					uid = str(random.randint(0, 100000)) 
					ucon = { "a" : "","b" : "","c" : 1,"d" : -1}
					ucon['a'] = '假人' + uid
					ucon['b'] = str(random.randint(1, 5))
					ucon['c'] = random.randint(1, 3000)
					tcircus_find['a'][uid] = ucon 
				result = self.db_circusTeam.update_one(tcircus_target,  {'$set': tcircus_find})
				outcome = '加了10个假人.'
			else:
				outcome = '尚未组队'
		else:
			outcome = 'ID not found'
		return outcome















# # 执行函数
# def increaseDummy(circus_ID, db):
#     target = {'_id': int(circus_ID)}
#     db_coll_circusUser = db['circus_user']
#     db_coll_circusTeam = db ['circus_team']
#     ucircus_find = db_coll_circusUser.find_one(target)
#     if ucircus_find:
#         tcircus = ucircus_find['b']
#         tcircus_target = {'_id': tcircus}
#         tcircus_find = db_coll_circusTeam.find_one(tcircus_target)
#         if tcircus_find:
#             for i in range(0, 10):
#                 uid = str(random.randint(0, 100000)) 
#                 ucon = { "a" : "","b" : "","c" : 1,"d" : -1}
#                 ucon['a'] = '假人' + uid
#                 ucon['b'] = str(random.randint(1, 5))
#                 ucon['c'] = random.randint(1, 3000)
#                 tcircus_find['a'][uid] = ucon 
#             result = db_coll_circusTeam.update_one(tcircus_target,  {'$set': tcircus_find})
#             outcome = '加了10个假人.'
#         else:
#         	outcome = '尚未组队'
#     else:
#         outcome = '未找到此ID'
#     return outcome
