import os
import xlrd
from gevent import monkey
from copy import deepcopy
import gevent
import urllib.request
import time
import shutil


def report(publishPath):
	# 获取版本号用于生成报告
	current_version = publishPath.split('/')[-1]
	# report_name = r'Z:\01-QA-Jelly\4-Testing_report\check_report_' + current_version + '.txt'
	report_name = r'/mnt/webDevice/JellyBlast/01-QA-Jelly/4-Testing_report/check_report_' + current_version + '.txt'
	return report_name

def cutDirs(path, new_path):
	for dir in os.listdir(path):
		cur_path = os.path.join(path, dir)
		new_file_path = os.path.join(new_path, dir)
		if not os.path.exists(new_file_path):
			shutil.move(cur_path, new_file_path)
			print('\'' + new_file_path + '\'' + 'has cut')
		else:
			os.remove(new_file_path)
			shutil.move(cur_path, new_file_path)
			print('\'' + new_file_path + '\'' + 'has cut')

# def getMD5(apk):
# 	# 获取APK包的MD5的命令
# 	command = 'certutil -hashfile '
# 	apkname = apk
# 	MD5 = os.popen(command + apkname + ' MD5').readlines()
# 	return MD5[1]

def getMD5(apk):
	# Linux下获取文件MD5
	command = 'md5sum '
	apkname = apk
	MD5 = os.popen(command + apkname).readlines()[0].split(' ')[0]
	return MD5

def publishMD5(path):
	# 创建报告,先获取待提交包的MD5值并写入
	MD5TXT = report(publishPath)
	with open (MD5TXT, 'w+') as checkMD5:
		for root, dirs, files in os.walk(path):
			for filename in files:
				if filename.endswith('apk'):
					checkMD5.write(filename + ': ')
					checkMD5.write(getMD5(os.path.join(root, filename)))
					print(getMD5(os.path.join(root, filename)))
					checkMD5.write('\n')
					checkMD5.write('\n')
					print(filename + ' gets MD5 done')
	print('-'*150)
	print('publish--apk--MD5--finished')
	print('-'*150)

def mactchMD5(path, matches_links):
	MD5TXT = report(publishPath)
	# 打开报告,获取由链接下载下来的APK的包的MD5并同已写入的待提交包的MD5进行匹配
	for root, dirs, files in os.walk(path):
		for filename in files:
			if filename.endswith('apk'):
				with open (MD5TXT, 'r') as checkMD5:
					downloadMD5 = getMD5(os.path.join(root, filename))
					linesMD5 = checkMD5.read()
					# 若找到此MD5则在相应位置写入success
					pos = linesMD5.find(downloadMD5.rstrip())
					if pos != -1:
						print(filename + ' checks MD5 done')
						linesMD5 = linesMD5[:pos] + '-----------success-----------' + linesMD5[pos:]
						with open (MD5TXT, 'w') as checkMD5:
							checkMD5.write(linesMD5)
					# 匹配失败时, 在报告中写入失败的APK文件名及其来源链接
					else:
						print(filename + ' checks MD5 failed')
						print(downloadMD5.rstrip())
						with open (MD5TXT, 'a+') as checkMD5:
							if filename in matches_links.values():
								failedApk_link = list(matches_links.keys())[list(matches_links.values()).index(filename)]
								checkMD5.write('\n\n' + filename + ' mactches failed, ' + 'from the link: ' + failedApk_link)
	with open (MD5TXT, 'a+') as checkMD5:
		checkMD5.write('\n')
		checkMD5.write('\n')
	print('-'*150)
	print('MD5-check finished, get result at MD5.TXT')
	print('-'*150)
	checkChannels(channelsDict, MD5TXT)

def checkChannels(channelsDict, MD5TXT):
	for i in range(118, updateSheet.nrows):
		if str(testlink_col[i]).strip() and str(testlink_col[i]) not in ['\n', '\r\n']:
			testlink = str(testlink_col[i]).split(':', 1)[1].strip('\'')
			if testlink.startswith('http'):
				for i in str(testlink_col_channels[i]).split(':', 1)[1].split(';'):
					channelNum = i.strip('\'')
					with open (MD5TXT, 'a+') as checkMD5:
						if channelsDict.setdefault(channelNum, None):
							if channelsDict.setdefault(channelNum, None) in testlink:
								print('channel--%-5s--checked success, %-10s in the update link'%(str(channelNum), channelsDict[channelNum])) 
							else:
								print('channel--%-5s--checked failed, the keywords %-10s is not found, recorded in the MD5.TXT'%(str(channelNum), channelsDict[channelNum]))
								checkMD5.write('\n')
								checkMD5.write('\n' + 'channel ' + str(channelNum) + ' failed, the wrong link is: ' + testlink)
						else:
							print('channel--%-5s--is new, need to record')
							checkMD5.write('\n')
							checkMD5.write('\n' + 'channel ' + str(channelNum) + ' failed--links for the new channels, the link is: ' + testlink)
	# check over
	print('-'*150)
	print('links-check finished, all is finished')

def my_downLoad(url, file_name, links_Apks, links_failed):
	try:
		# 跳过已下载过的文件
		# 获取网盘中文件地址
		links_Apks[url] = file_name.split('/')[-1]
		apkName = os.path.basename(file_name)
		Net_path_file = os.path.join(Net_downloadPath, apkName)
		if not os.path.exists(Net_path_file):
			# 网盘中不存在,查看本地知否存在
			# 若本地不存在,则下载
			if not os.path.exists(file_name):
				# 根据url访问网络资源完成数据读取
				resp = urllib.request.urlopen(url)
				print(url + ' 开始下载...')
				with open(file_name, "wb") as apk:
					while True:
						# 读取数据
						file_data= resp.read(4096)
						if file_data:
							# 读取到的数据写入文件
							apk.write(file_data)
						else:
							break
			# 若本地存在,则查看文件大小
			else:
				if os.path.getsize(file_name) > 358745040:
					print('%s 已存在,跳过' %(file_name))
				else:
					os.remove(file_name)
					resp = urllib.request.urlopen(url)
					print('%s 不完整,删除重新下载' %(file_name))
					with open(file_name, "wb") as apk:
						while True:
							# 读取数据
							file_data= resp.read(4096)
							if file_data:
								# 读取到的数据写入文件
								apk.write(file_data)
							else:
								break
		# 网盘中存在
		else:
			# 根据网盘的文件大小是否下载完成——没什么必要
			if os.path.getsize(Net_path_file) > 358745040:
				print('%s 已存在,跳过' %(file_name))
			else:
				os.remove(Net_path_file)
				resp = urllib.request.urlopen(url)
				print('%s 不完整,删除重新下载' %(file_name))
				with open(file_name, "wb") as apk:
					while True:
						# 读取数据
						file_data= resp.read(4096)
						if file_data:
							# 读取到的数据写入文件
							apk.write(file_data)
						else:
							break
	except Exception as e:
		print("下载异常: %s" % file_name, 'Error: ', e)
	else:
		print("下载成功: %s" % file_name)


def separate_download(g_list, o_list, start, stop):
	with gevent.Timeout(1200, False) as timeout:
		for i in range(start, stop):
			if str(testlink_col[i]).strip() and str(testlink_col[i]) not in ['\n', '\r\n']:
				# get links
				testlink = str(testlink_col[i]).split(':', 1)[1].strip('\'')
				if testlink.startswith('http'):
					# 创建携程指派任务
					apkName = os.path.basename(testlink).replace('?','_').replace('&', '_')
					if not apkName.endswith('.apk'):
						apkName += '.apk'
					time.sleep(5)
					downloadPath_dirs = os.path.join(downloadPath, apkName)
					g_list.append(gevent.spawn(my_downLoad, testlink, downloadPath_dirs, links_Apks, links_failed))
		# 主线程等待所有的协程执行完，程序再退出
		o_list = gevent.joinall(g_list)
		g_list = []
	cutDirs(downloadPath, Net_downloadPath)


def get_failed_list(links_Apks, downloadPath):
	for value in list(links_Apks.values()):
		for dirname in os.listdir(downloadPath):
			if dirname == value:
				del links_Apks[list(links_Apks.keys())[list(links_Apks.values()).index(value)]]
	failed_list = list(links_Apks.keys())
	return failed_list


# 程序入口
if __name__ == '__main__':

	# 打开excel中更新链接页
	file_updatelink = 'sys_config.xlsx'
	updateExcel = xlrd.open_workbook(filename=file_updatelink)
	updateSheet = updateExcel.sheet_by_index(0)
	# 链接位于第二列，渠道号位于第四列
	testlink_col = updateSheet.col(2)
	testlink_col_channels = updateSheet.col(4)
	downloadPath = r"/code/update"
	# 每个版本需要改的是这个地址——可以通过最后修改时间来自动获取
	publishPath = r'/mnt/webDevice/JellyBlast/publish/android/China/6.9.1'
	# 后续把这里改一下——自动生成
	Net_downloadPath = r'/mnt/webDevice/JellyBlast/01-QA-Jelly/4-Testing_report/update_prompt_downloaded_6.9.1'
	channelsDict = {
	'162' : 'taptap',
	'109' : 'gamedl.gionee',
	'104' : 'qq_browser',
	'139' : 'app.2345',
	'24' : 'baidu_dk',
	'138' : 'zhongxing',
	'169' : 'nokia',
	'34' : 'sogou_sousuo',
	'44' : 'yingyongbao',
	'914' : 'anzhibdpz',
	'41' : 'lenovo',
	'125' : 'yunos',
	'158' : 'yixin',
	'28' : 'huawei',
	'135' : 'smartisan',
	'39' : 'coolyun',
	'142' : 'qq_huawei',
	'161' : 'toutiao',
	'31' : 'sogoucdn',
	'32' : 'sogoucdn',
	'33' : 'sogoucdn',
	'23' : 'wandoujia',
	'100' : 'mfp',
	'910' : 'anzhi91',
	'916' : 'anzhi91',
	'12' : 'mmarket',
	'124' : 'iqiyi',
	'21' : '360',
	'11' : 'dianxin_inside',
	'123' : 'microfun',
	'13' : 'microfun',
	'134' : 'microfun',
	'14' : 'microfun',
	'140' : 'microfun',
	'145' : 'microfun',
	'146' : 'microfun',
	'150' : 'microfun',
	'152' : 'microfun',
	'153' : 'microfun',
	'155' : 'microfun',
	'157' : 'microfun',
	'164' : 'microfun',
	'911' : 'microfun',
	'913' : 'microfun',
	'917' : 'microfun',
	'170' : 'jelly_2345',
	'148' : 'meituyun',
	'29' : 'vivo',
	'128' : 'samsung',
	'129' : 'letv',
	'122' : 'tmgp',
	'122 * 10000145' : 'tmgp',
	'122 * 10000144' : 'tmgp',
	'144' : 'koobee',
	'30' : 'uc',
	'27' : 'anzhi',
	'126' : 'aorayyh',
	'112' : 'binguoxiaoxiaoxiao',
	'22' : 'binguoxiaoxiaoxiao',
	'127' : 'zhuoyi',
	'137' : 'qq_guanjia',
	'120' : 'nubia',
	'165' : 'game233',
	'154' : 'sugar',
	'149' : 'appchina',
	'26' : 'xiaomi',
	'172' : 'game233_test',
	'922' : 'langang',
	'923' : 'lang11'
	}

	# 设置识别耗时操作
	monkey.patch_all()

	g_list = []
	o_list = []
	links_failed = []
	links_Apks = {}
	downloadRange = list(range(118, updateSheet.nrows, 10))
	downloadRange.append(updateSheet.nrows)
	for i in range(0, len(downloadRange)-1):
		separate_download(g_list, o_list, downloadRange[i], downloadRange[i+1])
	matches_links = deepcopy(links_Apks)
	# print(links_Apks)
	failed_list = get_failed_list(links_Apks, Net_downloadPath)
	print('下载失败总数: ', str(len(failed_list)), '失败列表: ', failed_list)
	print('下载到的APK总数: ', str(len([filename for root, dirs, files, in os.walk(Net_downloadPath) for filename in files if filename.endswith('apk')])))
	publishMD5(publishPath)
	mactchMD5(Net_downloadPath, matches_links)