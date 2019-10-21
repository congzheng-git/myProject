from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb
import lib.userInfo

"""限时活动功能集合"""


class combineOlympic(lib.userInfo.getUserInfo):

	def __init__(self, userid):
		super(combineOlympic, self).__init__(userid)
		self.option_Olympic = request.values.get('combineOlympic')

	def combineOlympic(self):
		if self.option_Olympic == '1':
			outcome = self.remove_all_olympic("time_limit_user", "time_limit_rank_score", "time_limit_rank_backup", "time_limit_rank", "time_limit_garden_war")
		elif self.option_Olympic == '2':
			outcome = self.clear_medal_olympic(self.target)
		elif self.option_Olympic == '3':
			sessionsNum = request.values.get('sessionsNum')
			outcome = self.award_olympic(self.target, sessionsNum)
		else:
			outcome = 'Error: 提交项未选择'
		return outcome

	# 清除参与了活动的所有用户数据
	def remove_all_olympic(self, *COLLECTION_olys):
		for COLLECTION_oly in COLLECTION_olys:
			db_coll_oly = self.serverDb[COLLECTION_oly]
			users_all = db_coll_oly.find()
			for user in users_all:
				de_target = user['_id']
				result = db_coll_oly.delete_one({'_id': de_target})
			outcome = '清除了所有活动数据'
		return outcome 

	# 清除用户后端头像、奖章等信息
	def clear_medal_olympic(self, target):
		# 找到目标udata
		if self.udata:
			self.udata['p1'] = []
			self.udata['p2'] = []
			self.udata['p3'] = []
			self.udata['p4'] = []
			self.udata['p5'] = {}
			self.udata['pp1'] = {}
			result = self.db_data.update_one(self.target, {'$set': self.udata})
			outcome = '清除成功, 删包重装无头像、勋章等'
		else:
			outcome = '未找到此ID'
		return outcome

		# 模拟发奖弹窗
	def award_olympic(self, target, sessionsNum):
		if self.udata:
			# 届数可设置
			self.udata['x']['81'] = sessionsNum
			self.udata['x']['80'] = "1"
			result = self.db_data.update_one(self.target, {'$set': self.udata})
			outcome = 'login可见第一名发奖弹窗'
		else:
			outcome = '未找到此ID'
		return outcome
















