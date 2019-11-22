from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import userInfo
import psycopg2

"""创建新用户"""


class userLogoff_mongo(userInfo.getUserInfo):
	def __init__(self, userid):
		super(userLogoff_mongo, self).__init__(userid)
		self.db_info = self.serverDb['user_info']
		self.uinfo = self.db_info.find_one(self.target)

	# 给user_info中id各非空string字段添加信息
	def userLogoff_mongo(self):
		if self.uinfo:
			if 'a' in self.uinfo and 'b' in self.uinfo:
				for key in self.uinfo:
					if self.uinfo[key] and not isinstance(self.uinfo[key], int):
						self.uinfo[key] += '_zxc'
			else:
				outcome = 'user data error'
				return outcome
			result = self.db_info.update_one(self.target, {'$set': self.uinfo})
			outcome = '旧ID已注销'
		else:
			outcome = 'ID not found'

		return outcome