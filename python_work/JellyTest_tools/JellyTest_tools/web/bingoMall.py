from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import progress
import userInfo

"""修改集市进度"""

class bingoMall(userInfo.getUserInfo):

	def __init__(self, userid):
		super(bingoMall, self).__init__(userid)

		self.db_house = self.serverDb['user_house']
		self.uhouse = self.db_house.find_one(self.target)

	def bingoMall(self):
		if self.uhouse:
			# 数据中有null而python中没有这东西，需先定义null，否则报错
			null = ''
			option_mall = request.values.get('bingoMallprogress')
			self.uhouse = getattr(progress, option_mall)
			result = self.db_house.update_one(self.target, {'$set': self.uhouse})
			outcome = '修改成功'
		else:
			# 没有创建过集市进度的用户不能直接改
			# 也可以通过insert_one来实现，没啥需求
			outcome = 'ID not found'
		return outcome