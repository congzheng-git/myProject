from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb
import lib.userInfo

"""设置关卡进度"""


class levelSetting(lib.userInfo.getUserInfo):

	def __init__(self, userid):
		super(levelSetting, self).__init__(userid)
		return

	def levelSetting(self):
		
		if not self.ulevel:
			outcome = '全新用户不能修改，先过1关'
			return outcome

		if self.udata:
			user_cur_level = request.values.get('maxLeveL')
			if not self.levelCheck(user_cur_level):
				outcome = 'Error: 关卡输入错误'
				return outcome
			self.udata['r'] = int(user_cur_level)
			self.ulevel['a'] = {}

			# 收到0即清除进度
			if int(user_cur_level) == 0:
				result = self.db_data.update_one(self.target, {'$set': self.udata})
				result = self.db_level.update_one(self.target, {'$set': self.ulevel})
				outcome = '清除关卡进度'
				return outcome

			# 判断是否为金卡座
			if request.values.get('alllevelStars') == '1':
				for  i  in range(1, int(user_cur_level) + 1):		
					self.ulevel['a'][str(i)] = "400000_3_1"
			else:
				self.ulevel['a']['1'] = "400000_3_1"
				for  i  in range(2, int(user_cur_level) + 1):		
					self.ulevel['a'][str(i)] = "400000_3"

			# 非满星功能
			# 
			# 
			# 
			# 

			result = self.db_data.update_one(self.target, {'$set': self.udata})
			result = self.db_level.update_one(self.target, {'$set': self.ulevel})

			outcome = '设置进度成功，删包重装可见'
		else:
			outcome = '未找到此ID'

		return outcome

	def levelCheck(self, level):
		return [False, True][level.isdigit()]


