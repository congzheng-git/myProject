import pymongo

def mongodb(server):
	# mongodb服务的地址和端口号
	mongo_url = "172.16.0.111:27017"
	# 连接到mongodb，如果参数不填，默认为“localhost:27017”
	client = pymongo.MongoClient(mongo_url)
	# 连接到数据库myDatabase
	db = client[server]
	return(db)
	



