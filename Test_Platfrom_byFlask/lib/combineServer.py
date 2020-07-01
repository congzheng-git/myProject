from flask import Flask
from flask import render_template
from flask import request
from lib.mongoweb import mongodb
import os
import time 
import lib.userInfo
import paramiko

"""服务器功能集合"""


class combineServer(lib.userInfo.getUserInfo):

	def __init__(self, userid):
		super(combineServer, self).__init__(userid)
		self.server = request.values.get('server')
		self.option_Server = request.values.get('combineServer')
		self.time_Setting = request.values.get('timeSetting')
		self.timeSetting_date = request.values.get('timeSetting_date')
		self.timeSetting_clock = request.values.get('timeSetting_clock')
		self.act_list = [
			'inspire_bank_user', 
			'toy_user_job', 
			'toy_user_reward', 
			'toy_rank_cache', 
			'toy_history', 
			'camp_war_not_full_team',
			'camp_war_slot_team',
			'camp_war_team',
			'camp_war_user',
			'circus_not_full_team',
			'circus_season_info',
			'circus_season_rank',
			'circus_slot_team',
			'circus_team',
			'circus_user',
			'five_check_in',
			'gold_button_user',
			'inspire_user_job',
			'marathon_not_full_team',
			'marathon_slot_team',
			'marathon_user',
			'marathon_team',
			'new_mission_user',
			'team_not_full',
			'team_slot',
			'old_player'
		]

	def clearInvalidData(self, coll_invalid):
		# 需要删除被时间限制的活动数据
		db_coll_invalid = self.serverDb[coll_invalid]
		db_coll_invalid.remove()

	def combineServer(self):

		if self.option_Server == '1':
			if self.server.split('_')[1] == 'new':
				self.HostIP = '172.16.0.33'
				self.username = 'mfp'
				self.passwd = 'mfp33'
				outcome = self.resetTime_Old(self.HostIP, self.username, self.passwd)
			else:
				self.HostIP = '172.16.0.' + self.server.split('_')[2]
				self.username = 'root'
				outcome = self.resetTime_New(self.HostIP, self.username)
		elif self.time_Setting == 'setting':
			if self.server.split('_')[1] == 'new':
				self.HostIP = '172.16.0.33'
				self.username = 'mfp'
				self.passwd = 'mfp33'
				outcome = self.settingTime_Old(self.HostIP, self.username, self.passwd, self.timeSetting_date, self.timeSetting_clock)
			else:
				self.HostIP = '172.16.0.' + self.server.split('_')[2]
				self.username = 'root'
				outcome = self.settingTime_New(self.HostIP, self.username, self.timeSetting_date, self.timeSetting_clock)
		elif self.time_Setting == 'current':
			if self.server.split('_')[1] == 'new':
				self.HostIP = '172.16.0.33'
				self.username = 'mfp'
				self.passwd = 'mfp33'
				outcome = self.currentTime_Old(self.HostIP, self.username, self.passwd)
			else:
				self.HostIP = '172.16.0.' + self.server.split('_')[2]
				self.username = 'root'
				outcome = self.currentTime_New(self.HostIP, self.username)
		else:
			outcome = 'Error: 提交项未选择'
		return outcome

	def resetTime_Old(self, HostIP, username, passwd):
		try:
			# 通过用户名/密码连接到33服务器
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(HostIP, 22, username, passwd)
			# 恢复服务器时间
			# 创建shell伪终端用于发送命令
			ssh_shell = ssh.invoke_shell()
			time.sleep(0.2)

			buff = ''
			while not buff.endswith('$ '):
				resp = ssh_shell.recv(9999)
				buff += resp.decode('utf8')
				time.sleep(0.1)

			# 切换到root
			ssh_shell.send('su' + '\n')
			strrecv = ssh_shell.recv(4096).decode()
			while not 'Password' in strrecv:
				time.sleep(0.1)
				strrecv = ssh_shell.recv(4096).decode()
				# print(strrecv)

			ssh_shell.send('Microfun.001')
			ssh_shell.send('\n')
			while not '#' in strrecv:
				time.sleep(0.1)
				strrecv = ssh_shell.recv(4096).decode()
				# print(strrecv)
			# 服务器时间设置为系统时间
			# time.sleep()
			ssh_shell.send('hwclock --hctosys' + '\n')
			time.sleep(1)
			# 查看当前时间
			cmd = 'date'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			strout = bytes.decode(stdout.read())
			outcome = 'Current Time: %s'%(strout)
			ssh.close()
			for coll in self.act_list:
				self.clearInvalidData(coll)

		except Exception as ex:
			outcome = "\tError %s\n"% ex
		return outcome

	def resetTime_New(self, HostIP, username):
		try:
			pkey='D:/sshtest/Identity'  #本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
			key = paramiko.RSAKey.from_private_key_file(pkey)
			paramiko.util.log_to_file('paramiko.log')
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #通过公共方式进行认证 (不需要在known_hosts 文件中存在)
			#ssh.load_system_host_keys() #如通过known_hosts 方式进行认证可以用这个,如果known_hosts 文件未定义还需要定义 known_hosts
			ssh.connect(HostIP, username = username, pkey=key) #这里要 pkey passwordkey 密钥文件
			ssh_shell = ssh.invoke_shell()
			time.sleep(0.2)
			# 服务器时间设置为系统时间
			ssh_shell.send('hwclock --hctosys' + '\n')
			time.sleep(1)
			# 查看当前时间
			cmd = 'date'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			strout = bytes.decode(stdout.read())
			outcome = 'Current Time: %s'%(strout)
			# 关闭连接
			ssh.close()
			for coll in self.act_list:
				self.clearInvalidData(coll)
		except Exception as ex:
			outcome = "\tError %s\n"% ex
		return outcome

	def settingTime_Old(self, HostIP, username, passwd, date, clock):
		try:
			# 通过用户名/密码连接到33服务器
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(HostIP, 22, username, passwd)
			# 恢复服务器时间
			# 创建shell伪终端用于发送命令
			ssh_shell = ssh.invoke_shell()
			time.sleep(0.2)

			buff = ''
			while not buff.endswith('$ '):
				resp = ssh_shell.recv(9999)
				buff += resp.decode('utf8')
				time.sleep(0.1)

			# 切换到root
			ssh_shell.send('su' + '\n')
			strrecv = ssh_shell.recv(4096).decode()
			while not 'Password' in strrecv:
				time.sleep(0.1)
				strrecv = ssh_shell.recv(4096).decode()
				print(strrecv)

			ssh_shell.send('Microfun.001')
			ssh_shell.send('\n')
			while not '#' in strrecv:
				time.sleep(0.1)
				strrecv = ssh_shell.recv(4096).decode()
				print(strrecv)
			time.sleep(0.2)
			# 设置时间
			date_setting = 'date -s ' + '\'' + date + ' ' + clock + '\''
			ssh_shell.send(date_setting + '\n')
			stdin,stdout,stderr = ssh.exec_command(date_setting)
			if 'invalid' in stderr.read().decode():
				outcome = '时间格式错误'
				return outcome
			cmd = 'date'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			strout = bytes.decode(stdout.read())
			outcome = 'Current Time: %s'%(strout)
			ssh.close()
		except Exception as ex:
			outcome = "\tError %s\n"% ex
		return outcome

	def settingTime_New(self, HostIP, username, date, clock):
		try:
			pkey='D:/sshtest/Identity'  #本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
			key = paramiko.RSAKey.from_private_key_file(pkey)
			paramiko.util.log_to_file('paramiko.log')
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #通过公共方式进行认证 (不需要在known_hosts 文件中存在)
			#ssh.load_system_host_keys() #如通过known_hosts 方式进行认证可以用这个,如果known_hosts 文件未定义还需要定义 known_hosts
			ssh.connect(HostIP, username = username, pkey=key) #这里要 pkey passwordkey 密钥文件
			ssh_shell = ssh.invoke_shell()
			time.sleep(0.2)
			# 设置时间
			date_setting = 'date -s ' + '\'' + date + ' ' + clock + '\''
			stdin,stdout,stderr = ssh.exec_command(date_setting)
			if 'invalid' in stderr.read().decode():
				outcome = '时间格式错误'
				return outcome
			# 查看当前时间
			cmd = 'date'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			strout = bytes.decode(stdout.read())
			outcome = 'Current Time: %s'%(strout)

			# 关闭连接
			ssh.close()
		except Exception as ex:
			outcome = "\tError %s\n"% ex
		return outcome

	def currentTime_Old(self, HostIP, username, passwd):
		try:
			# 通过用户名/密码连接到33服务器
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(HostIP, 22, username, passwd)
			# 恢复服务器时间
			# 创建shell伪终端用于发送命令
			ssh_shell = ssh.invoke_shell()
			time.sleep(0.2)

			buff = ''
			while not buff.endswith('$ '):
				resp = ssh_shell.recv(9999)
				buff += resp.decode('utf8')
				time.sleep(0.1)
			# 查看当前时间
			cmd = 'date'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			strout = bytes.decode(stdout.read())
			outcome = 'Current Time: %s'%(strout)
		except Exception as ex:
			outcome = "\tError %s\n"% ex
		return outcome
	def currentTime_New(self, HostIP, username):
		try:
			pkey='D:/sshtest/Identity'  #本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
			key = paramiko.RSAKey.from_private_key_file(pkey)
			paramiko.util.log_to_file('paramiko.log')
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #通过公共方式进行认证 (不需要在known_hosts 文件中存在)
			#ssh.load_system_host_keys() #如通过known_hosts 方式进行认证可以用这个,如果known_hosts 文件未定义还需要定义 known_hosts
			ssh.connect(HostIP, username = username, pkey=key) #这里要 pkey passwordkey 密钥文件
			# 查看当前时间
			cmd = 'date'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			strout = bytes.decode(stdout.read())
			outcome = 'Current Time: %s'%(strout)
			# 关闭连接
			ssh.close()
			for coll in self.act_list:
				self.clearInvalidData(coll)
		except Exception as ex:
			outcome = "\tError %s\n"% ex
		return outcome

