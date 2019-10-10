from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb
import lib.userInfo


"""添加关卡内、关前道具"""


class increaseTools(lib.userInfo.getUserInfo):
	
	def __init__(self, userid):
		super(increaseTools, self).__init__(userid)
		self.increment = 200
		

	# 改变user_data中道具对应字段数值
	def increaseTools(self):
		if self.udata:
			# 关卡内道具
			self.udata['q']['4_101'] = self.increment
			self.udata['q']['4_102'] = self.increment
			self.udata['q']['4_103'] = self.increment
			self.udata['q']['4_104'] = self.increment
			#豆子
			self.udata['q']['2_1'] = 999999999
			#关卡前道具
			self.udata['q']['11_1'] = self.increment
			self.udata['q']['11_2'] = self.increment
			self.udata['q']['11_3'] = self.increment
		
			result = self.db_data.update_one(self.target, {'$set': self.udata})
			outcome = '道具增加成功'
		else:
			outcome = 'ID not found'
		return outcome



