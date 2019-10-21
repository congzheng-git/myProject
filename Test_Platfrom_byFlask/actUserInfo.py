from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import userInfo

"""删除活动内ID相关数据"""


class actUserInfo(userInfo.getUserInfo):
	# 继承自getUserInfo
	def __init__(self, userid):
		super(actUserInfo, self).__init__(userid)
		self.reqVal = request.values

	# 只删除单个表单内id相关数据的活动
	def getActivity_single(self, opAct):

		self.db_act_single = self.serverDb[opAct]
		self.uact_single = self.db_act_single.find_one(self.target)

		return self.uact_single

	def delete_Activity_single(self, opAct):

		uact_single = self.getActivity_single(opAct)
		if uact_single:
			result = self.db_act_single.delete_one(uact_single)
			outcome = '删除成功'
		else:
			outcome = 'ID not found'

		return outcome

	# 组队类活动——火箭、马戏团等
	def getActivity_team(self, opAct):

		activity_team_user = opAct + '_user'
		activity_team_team = opAct + '_team'
		activity_team_not_full = opAct + '_not_full_team'

		self.db_act_team_user = self.serverDb[activity_team_user]
		self.db_act_team_team = self.serverDb[activity_team_team]
		self.db_act_team_not_full = self.serverDb[activity_team_not_full]

		self.uact_team = self.db_act_team_user.find_one(self.target)
		return self.uact_team

	def delete_Activity_team(self, opAct):
		
		uact_team = self.getActivity_team(opAct)

		if uact_team:
			result = self.db_act_team_user.delete_one(uact_team)
			if uact_team['b'] != 0:
				uact_teamInfo = self.db_act_team_team.find_one({'_id': uact_team['b']})
				if uact_teamInfo:
					# 一个人一队就删队伍，否则只删自己
					if len(uact_teamInfo['a']) != 1:
						del uact_teamInfo['a'][self.uid]
						result = self.db_act_team_team.update_one({'_id': uact_team['b']}, {'$set': uact_teamInfo})
					else:
						result = self.db_act_team_team.delete_one(uact_teamInfo)
						# 删除未满的队伍
						if self.db_act_team_not_full:
							uact_team_not_full = self.db_act_team_not_full.find_one({'_id': uact_team['b']})
							if uact_team_not_full:
								result = self.db_act_team_not_full.delete_one(uact_team_not_full)
						# 复用型team_not_full
						else:
							uact_team_not_full = self.serverDb['team_not_full'].find_one({'_id': uact_team['b']})
							if uact_team_not_full:
								result = self.serverDb['team_not_full'].delete_one(uact_team_not_full)
				outcome = '组队删除成功'
			else:
				outcome = '个人删除成功'				
		else:
			outcome = 'ID not found'
		return outcome

 
	# 其他数据特殊格式的活动
	def getActivity_others(self, opAct):
		# 当前只有通关活动
		if 'pass' in opAct:
			self.db_act_others = self.serverDb[opAct]
			# 模糊匹配id
			self.uact_others = self.db_act_others.find({'_id': {'$regex': self.uid}})
			return self.uact_others


	def delete_Activity_others(self, opAct):
		# 通关活动可能有多版本数据
		if 'pass' in opAct:
			uact_others = self.getActivity_others(opAct)
			# 不清楚空的Cursor实例如何判断，但其不会执行'for'循环
			outcome = 'ID not found'	
			for i in uact_others:
				result = self.db_act_others.delete_one(i)
				outcome = '删除成功'
			return outcome	


	def actUserInfo(self):

		if self.reqVal.get('activity'):
			self.opAct = self.reqVal.get('activity')[2:]
		else:
			outcome = 'Error: 提交项未选择'
			return outcome

		if self.reqVal.get('activity')[0] == 's':
			outcome = self.delete_Activity_single(self.opAct)
		elif self.reqVal.get('activity')[0] == 't':
			outcome = self.delete_Activity_team(self.opAct)
		elif self.reqVal.get('activity')[0] == 'o':
			outcome = self.delete_Activity_others(self.opAct)
		else:
			outcome = 'Error: 提交项未选择'
		return outcome
