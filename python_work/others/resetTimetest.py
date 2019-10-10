import paramiko

# ssh = paramiko.SSHClient()
# key = paramiko.AutoAddPolicy()
# ssh.set_missing_host_key_policy(key)
# pkey = paramiko.RSAKey.from_private_key_file('D:/Documents/ssh_host_rsa_key')

# ssh.connect('172.16.0.220', 22, 'root', pkey=pkey, timeout=5)
# stdin, stdout, stderr = ssh.exec_command('ls')
# print(stdout.read().decode())
# print(stderr.read())
# # 关闭连接
# ssh.close()

pkey='D:/sshtest/Identity'  #本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
key=paramiko.RSAKey.from_private_key_file(pkey) #有解密密码时,
paramiko.util.log_to_file('paramiko.log')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #通过公共方式进行认证 (不需要在known_hosts 文件中存在)

#ssh.load_system_host_keys() #如通过known_hosts 方式进行认证可以用这个,如果known_hosts 文件未定义还需要定义 known_hosts
ssh.connect('172.16.0.221', username = 'root', pkey=key) #这里要 pkey passwordkey 密钥文件
stdin,stdout,stderr=ssh.exec_command('hostname')
print(stdout.read())
stdin,stdout,stderr=ssh.exec_command('ls')
print(stdout.read())
# 关闭连接
ssh.close()


# HostIP = '172.16.0.33'
# username = 'mfp'
# passwd = 'mfp33'


# def run():
# 	try:
# 		ssh = paramiko.SSHClient()
# 		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 		ssh.connect(HostIP,22,username,passwd)
# 		ssh.exec_command("pwd")
# 		ssh.exec_command("mkdir jcc")
# 		ssh.exec_command("cd jcc")
# 		stdin,stdout,stderr = ssh.exec_command("pwd")
# 		print(stdout.read())
# 		print("check status %s OK\n" %HostIP)
# 		ssh.close()
# 	except Exception as ex:
# 		print("\tError %s\n"% ex)


# if __name__ == '__main__':
# 	print("begin")
# 	run()
