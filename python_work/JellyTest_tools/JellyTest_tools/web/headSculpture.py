from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import userInfo

"""添加历史上的特殊头像"""


class headSculpture(userInfo.getUserInfo):

	def __init__(self, userid):
		super(headSculpture, self).__init__(userid)
		return


	def headSculpture(self):
		if self.udata:
			for i in range(0, 16):
				self.udata['p3'].append(i)
			self.udata['p3'].append(1001)
			self.udata['p3'] = list(set(self.udata['p3']))

			result = self.db_data.update_one(self.target, {'$set': self.udata})
			outcome = '头像增加成功'
		else:
			outcome = 'ID not found'
		return outcome



