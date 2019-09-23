from flask import Flask
from flask import render_template
from flask import request
from bson import json_util as jsonb
import pymongo
import time
import progress
import sys, os
from importlib import import_module
from mongoweb import mongodb

app = Flask(__name__)
# flask用法，允许POST(我也不太明白)
@app.route('/test', methods=['POST', 'GET'])

# 服务器主函数
def scripts_All():
	if request.method == 'POST':
		# Web端提交(post)后执行——获取userid以及本次所提交请求的标识
		try:
			userid = request.values.get('userid')
			userserver = request.values.get('server')
			button_Option = request.values.get('button_Option')
			if useridCheck(userid):
				requestModule = import_module(button_Option)
				operationObject = getattr(requestModule, button_Option)(userid)
				outcome = getattr(operationObject, button_Option)()
			else:	
				outcome = 'Error: userid输入错误'
				return render_template('webtest.html', option_act = outcome)
		except ValueError:
			outcome = 'Error: 后台调用模块失效(null)'
			return render_template('webtest.html', option_act = outcome)
		except Exception as e:
			outcome = e
			return render_template('webtest.html', option_act = outcome)

		# Web前端提交后由后台反馈的信息再显示到Web端以示执行结果，后台所有函数均会返回outcome
		return render_template('webtest.html', option_act = outcome, id_req = userid, server_req = userserver)
	# 初始状态Web
	else:
		return render_template('webtest.html')

def useridCheck(userid):
	return [False, True][userid.isdigit()]



# flask用法，运行服务器
if __name__ =='__main__':
	# 上方发布到局域网，下方本地测试
	# app.run(host='0.0.0.0', port=5001)	
	app.run(debug=True)