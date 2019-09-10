from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import userInfo

"""添加马戏团奖励雕像"""


class addStatue(userInfo.getUserInfo):

	def __init__(self, userid):
		super(addStatue, self).__init__(userid)

		self.db_house = self.serverDb['user_house']
		self.uhouse = self.db_house.find_one(self.target)


	def addStatue(self):
		dictStatue = {
            "a" : 300,
            "b" : {
                "300" : 0
            }
        }
		if self.uhouse:
			self.uhouse['f']['433'] = dictStatue
			result = self.db_house.update_one(self.target, {'$set': self.uhouse})
			outcome = '添加雕像成功'
		return outcome
