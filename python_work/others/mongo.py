import pymongo

def mongodb():
	# mongodb服务的地址和端口号
	mongo_url = "172.16.0.111:27017"
	# 连接到mongodb，如果参数不填，默认为“localhost:27017”
	client = pymongo.MongoClient(mongo_url)
	# 连接到数据库myDatabase
	db = client[database_num()]
	return(db)

def database_num():
	# DATABASE_NUM = int(input("选择服务器--1国内安卓，2国内IOS，3海外> "))
	inp = input("选择服务器--1国内安卓，2国内IOS，3海外> ")
	DATABASE_NUM = re_pos_int(inp)
	if DATABASE_NUM == 1:
		DATABASE = "jelly_new_dev"
	elif DATABASE_NUM == 2:
		DATABASE = "jelly_new_dev2"
	elif DATABASE_NUM == 3: 
		DATABASE = "jelly_new_dev3"
	else:
		print('错了')
		DATABASE = database_num()

	return DATABASE
	

def re_pos_int(inp):
	# 判断输入是否为正整数
	pos_int = inp.isdigit()
	if pos_int:
		int_inp = int(inp)
	else:
		inp = input('输入错误，重新输入> ')
		int_inp = re_pos_int(inp)
	return int_inp

# database_num()

def db_default():
	mongo_url = "172.16.0.111:27017"
	client = pymongo.MongoClient(mongo_url)
	db = client["jelly_new_dev2"]
	return(db)