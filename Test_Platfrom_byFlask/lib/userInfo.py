from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb


"""获取userid各基础信息"""


class getUserInfo(object):

	def __init__(self, userid):
	
		self.serverDb = self.getServer()
		self.db_data = self.serverDb['user_data']
		self.db_level = self.serverDb['user_level']

		self.uid = userid
		if userid:
			self.target = {'_id': int(userid)}
			self.udata = self.db_data.find_one(self.target)
			self.ulevel = self.db_level.find_one(self.target)
		

	def getServer(self):

		server = request.values.get('server')
		severDb = mongodb(server)
		return severDb












































# # 删除礼包购买记录，方便测礼包
# def delete_Gift():
# 	delete_Gift_ID = request.values.get('userid')
# 	db = server()
# 	outcome = buy_gift_clear(delete_Gift_ID, db=db)
# 	return outcome
# # 执行函数
# def buy_gift_clear(delete_Gift_ID, db):
# 	target = {'_id': int(delete_Gift_ID)}
# 	db_coll_gift = db['user_gift_data']
# 	ugift_find = db_coll_gift.find_one(target)
# 	if ugift_find:
# 		result = db_coll_gift.delete_one(target)
# 		outcome = '删除成功'
# 	else:
# 		outcome = '未找到此ID'
# 	return outcome






























