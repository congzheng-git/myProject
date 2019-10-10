import random
from dateutil import parser
from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb
import lib.userInfo

"""修改用户后台的同步时间戳"""


class dataConflict(lib.userInfo.getUserInfo):
	def __init__(self, userid):
		super(dataConflict, self).__init__(userid)
		return

	def dataConflict(self):
		
		if self.udata:
			Str_z1 = self.udata['z1']
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
			self.udata['w'] = myDatetime
			self.udata['z1'] = Str_z1
			result = self.db_data.update_one(self.target, {'$set': self.udata})
			outcome = '同步时间戳已修改，可在前端upload触发冲突'
		else:
			outcome = 'ID not found'

		return outcome




