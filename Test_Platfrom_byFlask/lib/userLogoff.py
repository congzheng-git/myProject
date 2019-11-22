from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import userInfo
import psycopg2

"""创建新用户"""


class userLogoff(userInfo.getUserInfo):
	def __init__(self, userid):
		super(userLogoff, self).__init__(userid)
		self.infodb = 'user_info'
		self.pridb = 'user_principals'

	def userLogoff(self):
		conn = psycopg2.connect(database="op_sso_test", user="postgres", host="172.16.0.214", port="21001")
		curs = conn.cursor()
		user_del_sql = ['delete from %s where userid=%s'%(self.infodb, self.uid), 'delete from %s where userid=%s'%(self.pridb, self.uid)]
	
		try:
			user_sel_sql = 'select * from user_info where userid=%s'%self.uid
			curs.execute(user_sel_sql)
			uid_in_infodb = curs.fetchall()
			if not len(uid_in_infodb) == 0:
				for del_sql in user_del_sql:
					curs.execute(del_sql)
				conn.commit()
				outcome = '删除成功'
			else:
				outcome = 'id not found'

		except Exception as e:
			outcome = e

		return outcome

