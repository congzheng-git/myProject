from flask import Flask
from flask import render_template
from flask import request
from mongoweb import mongodb
import os
import userInfo
import paramiko

"""重置服务器时间"""


class resetTime(userInfo.getUserInfo):

	def __init__(self, userid):
		super(resetTime, self).__init__(userid)
		self.server = request.values.get('server')
		# if self.server.split('_')[1] == 'new':
		# 	self.HostIP = '172.16.0.33'
		# 	self.username = 'mfp'
		# 	self.passwd = 'mfp33'


	def resetTime(self):

		if self.server.split('_')[1] == 'new':
			HostIP = '172.16.0.33'
			username = 'mfp'
			passwd = 'mfp33'
			try:
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(HostIP,22,username,passwd)
				ssh.exec_command('hwclock --hctosys')
				stdin,stdout,stderr = ssh.exec_command("date")
				outcome = 'current time: %s'%(stdout.read())
				ssh.close()
			except Exception as ex:
				outcome = "\tError %s\n"% ex
		else:
			pass

			# pkey='D:/sshtest/Identity'  #本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
			# key=paramiko.RSAKey.from_private_key_file(pkey)
			# paramiko.util.log_to_file('paramiko.log')
			# ssh = paramiko.SSHClient()
			# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #通过公共方式进行认证 (不需要在known_hosts 文件中存在)

			# #ssh.load_system_host_keys() #如通过known_hosts 方式进行认证可以用这个,如果known_hosts 文件未定义还需要定义 known_hosts
			
			# ssh.connect('172.16.0.221', username = 'root', pkey=key) #这里要 pkey passwordkey 密钥文件
			# stdin,stdout,stderr=ssh.exec_command('hostname')
			# print(stdout.read())
			# stdin,stdout,stderr=ssh.exec_command('ls')
			# print(stdout.read())
			# # 关闭连接
			# ssh.close()
		return outcome
