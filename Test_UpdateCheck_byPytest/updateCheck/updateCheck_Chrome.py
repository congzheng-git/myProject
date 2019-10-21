# -*- coding: gbk -*-
import xlrd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import os
import shutil
import requests

file_updatelink = 'sys_config.xlsx'
updateExcel = xlrd.open_workbook(filename=file_updatelink)
updateSheet = updateExcel.sheet_by_index(0)
testlink_col = updateSheet.col(2)
testlink_col_channels = updateSheet.col(4)

publishPath = r'Z:\publish\android\China\6.9.1'

def report(publishPath):
	# get current version for report
	current_version = publishPath.split('\\')[-1]
	report_name = r'Z:\01-QA-Jelly\4-Testing_report\check_report_' + current_version + '.txt'
	return report_name

def downloadAPKpath(publishPath):
	# get current version for downloadAPKs and create it
	current_version = publishPath.split('\\')[-1]
	download_dir_name = 'update_prompt_downloaded_' + current_version
	download_path_name = r'Z:\01-QA-Jelly\4-Testing_report'
	downloadPath = os.path.join(download_path_name, download_dir_name)
	if not os.path.exists(downloadPath):
		os.mkdir(downloadPath)
	else:
		for i in os.listdir(downloadPath):
			os.remove(os.path.join(downloadPath, i))
	return downloadPath

Net_downloadPath = downloadAPKpath(publishPath)
downloadPath = r'G:\updateCheck'
for i in os.listdir(downloadPath):
	os.remove(os.path.join(downloadPath, i))

def cutDirs(path, new_path):
	try:
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
	except FileNotFoundError:
		print('something downloaded over, try again')
		cutDirs(downloadPath, Net_downloadPath)

# function - get MD5(cmd command)
def getMD5(apk):
	command = 'certutil -hashfile '
	apkname = apk
	MD5 = os.popen(command + apkname + ' MD5').readlines()
	return MD5[1]

# get APK-MD5 in publish
def publishMD5(path):
	MD5TXT = report(publishPath)
	with open (MD5TXT, 'w+') as checkMD5:
		for root, dirs, files in os.walk(path):
			for filename in files:
				# write in TXT - MD5.TXT
				if filename.endswith('apk'):
					checkMD5.write(filename + ', MD5: ')
					checkMD5.write(getMD5(os.path.join(root, filename)) + '\n')
					print(filename + ' gets MD5 done')

	print('----------------------------------------------------------------------------------------------------------------------------------------')
	print('publish--apk--MD5--finished')
	print('----------------------------------------------------------------------------------------------------------------------------------------')

# mactchMD5 dowload-APKs to publish-APKs
def mactchMD5(path, links_Apks):
	MD5TXT = report(publishPath)
	for root, dirs, files in os.walk(path):
		for filename in files:
			if filename.endswith('apk'):
				with open (MD5TXT, 'r') as checkMD5:
					# downloadAPKs - MD5 
					downloadMD5 = getMD5(os.path.join(root, filename))
					linesMD5 = checkMD5.read()
					# find in MD5.TXT
					pos = linesMD5.find(downloadMD5.rstrip())
					if pos 	!= -1:
						print(filename + ' matches MD5 done')
						linesMD5 = linesMD5[:pos] + '-----------success-----------' + linesMD5[pos:]
						with open (MD5TXT, 'w') as checkMD5:
							checkMD5.write(linesMD5)
					# found failed--write filename and links
					else:
						with open (MD5TXT, 'a+') as checkMD5:
							fileDownload = filename + '.crdownload'
							if fileDownload in links_Apks.values():
								failedApk_link = list(links_Apks.keys())[list(links_Apks.values()).index(fileDownload)]
								checkMD5.write('\n\n' + filename + ' mactches failed, ' + 'from the link: ' + failedApk_link)
							else:
								failedApk_link = list(links_Apks.keys())[list(links_Apks.values()).index(filename)]
								checkMD5.write('\n\n' + filename + ' mactches failed, ' + 'from the link: ' + failedApk_link)

	print('----------------------------------------------------------------------------------------------------------------------------------------')
	print('MD5-check finished, get result at MD5.TXT')
	print('----------------------------------------------------------------------------------------------------------------------------------------')
	checkChannels(channelsDict, MD5TXT)

# check download status
def Checkfinished(path, linkNum, downloadFailedNum):
	finishedNum = downloadFinished(path)
	print('finished apks num: ' + str(finishedNum))
	print('out time apks num: ' + str(downloadFailedNum))
	if finishedNum + downloadFailedNum  >= linkNum:
		print('go on downloading')
		return True
	else:
		return False

# check the files by time
def sortFile(path):
	dirList = os.listdir(path)
	try:
		dirList.sort(key=lambda fn: os.path.getctime(path + '\\' + fn))
	except FileNotFoundError:
		print('not found, try again')
		sortFile(downloadPath)
	if len(dirList) != 0:
		return dirList[-1]
	else:
		return 'Failed - noResponse'

# read excel, download apks
def downloadApks(publishPath, downloadPath, Net_downloadPath):
	
	downloadFailedNum = 0
	linkNum = 0
	links_Apks = {}
	links_List = []

	for i in range(118, updateSheet.nrows):
		if str(testlink_col[i]).strip() and str(testlink_col[i]) not in ['\n', '\r\n']:
			# get links
			testlink = str(testlink_col[i]).split(':', 1)[1].strip('\'')
			if testlink.startswith('http'):
				linkNum += 1
				print('number of links visited: ' + str(linkNum))
				# get links in webbroswer
				links_List.append(testlink)
				try:
					driver.get(testlink)
				except TimeoutException:
					print('browser is time out: ' + testlink)
					continue
				waitingTime = 0
				time.sleep(5)
				# get the latest downloaded file and save it in the dictionary 
				if sortFile(downloadPath):
					latestFile = sortFile(downloadPath)
					if len(list(links_Apks.values())) >= 1:
						# if the connection is not responding, no file is downloaded
						if not latestFile == list(links_Apks.values())[-1]:
							links_Apks[testlink] = latestFile
						else:
							links_Apks[testlink] = 'Failed - get no Response(APK) from this link'
					else:
						links_Apks[testlink] = latestFile
				# check downloading status
				while not Checkfinished(downloadPath, linkNum, downloadFailedNum):
					print('downloading, wait for 10s...')
					waitingTime += 10
					time.sleep(10)
					# wait 30 seconds for each file
					if waitingTime == 50:
						waitingTime = 0
						print('APK downloaded timeout: ' + testlink)
						finishedNum = downloadFinished(downloadPath)
						downloadFailedNum = downloadFailed(linkNum, finishedNum, downloadFailedNum)
	# waiting for out-time
	overWaittime = 0
	while len([filename for root, dirs, files, in os.walk(downloadPath) for filename in files if not filename.endswith('apk')]) != 0:
		time.sleep(30)
		overWaittime += 30
		if overWaittime >= 900:
			print('too long to wait, please check the downloaded Apks')
			break
		print('waiting for out-time apks downloading...')
	# result
	# print('links-Apks:', links_Apks) 
	for i in links_Apks.keys():
		print("%-150s %-80s" % (i, links_Apks[i]))
	print('----------------------------------------------------------------------------------------------------------------------------------------')
	print('number of links visited: %-5s'%(linkNum))
	print('number of apks finished: %-5s'%(downloadFinished(downloadPath)))
	print('number of links  failed: %-5s'%(str(int(linkNum) - int(downloadFinished(downloadPath)))))
	print('----------------------------------------------------------------------------------------------------------------------------------------')

	for value in list(links_Apks.values()):
		valueDownload = str(value)
		if valueDownload.endswith('load'):
			if valueDownload.rstrip('.crdownload') in [filename for root, dirs, files, in os.walk(downloadPath) for filename in files]:
				if list(links_Apks.keys())[list(links_Apks.values()).index(value)] in links_List:
					links_List.remove(list(links_Apks.keys())[list(links_Apks.values()).index(value)])
					# print(links_List)
			else: 
				print('Not yet downloaded -', value, 'from the link: ', list(links_Apks.keys())[list(links_Apks.values()).index(value)])
		else:
			if valueDownload in [filename for root, dirs, files, in os.walk(downloadPath) for filename in files]:
				if list(links_Apks.keys())[list(links_Apks.values()).index(value)] in links_List:
					links_List.remove(list(links_Apks.keys())[list(links_Apks.values()).index(value)])
					# print(links_List)
			else: 
				print('Not yet downloaded -', value, 'from the link: ', list(links_Apks.keys())[list(links_Apks.values()).index(value)])

	if len(links_List) != 0:
		print('failed links list: ' ,set(links_List))
	else: 
		print('all links download success')

	print('download over')
	cutDirs(downloadPath, Net_downloadPath)
	print('----------------------------------------------------------------------------------------------------------------------------------------')
 
	publishMD5(publishPath)
	mactchMD5(Net_downloadPath, links_Apks)

# finined apks num
def downloadFinished(path):
	"""get num"""
	return  len([filename for root, dirs, files, in os.walk(path) for filename in files if filename.endswith('apk')])

# failed apks num
def downloadFailed(linkNum, finishedNum, downloadFailedNum):
	downloadFailedNum += 1

	# reduce when some apks finished
	getSum = finishedNum + downloadFailedNum 
	print('sum: ', getSum)
	print('linkNum: ', linkNum)

	if getSum - linkNum > 0:
		reduceNum = getSum - linkNum
		print('reduce: ', reduceNum)
		downloadFailedNum -= reduceNum
		print('failed num: ', downloadFailedNum)
	return downloadFailedNum

# links for channels
def checkChannels(channelsDict, MD5TXT):
	for i in range(118, updateSheet.nrows):
		if str(testlink_col[i]).strip() and str(testlink_col[i]) not in ['\n', '\r\n']:
			testlink = str(testlink_col[i]).split(':', 1)[1].strip('\'')
			if testlink.startswith('http'):
				for i in str(testlink_col_channels[i]).split(':', 1)[1].split(';'):
					channelNum = i.strip('\'')
					with open (MD5TXT, 'a+') as checkMD5:
						checkMD5.write('\n')
						checkMD5.write('\n')
					if channelsDict.setdefault(channelNum, None):
						if channelsDict.setdefault(channelNum, None) in testlink:
							print('channel--%-5s--checked success, %-10s in the update link'%(str(channelNum), channelsDict[channelNum])) 
						else:
							print('channel--%-5s--checked failed, the keywords--%-10s--is not found, recorded in the MD5.TXT'%(str(channelNum), channelsDict[channelNum]))
							with open (MD5TXT, 'a+') as checkMD5:
								checkMD5.write('\n')
								checkMD5.write('\n' + 'channel ' + str(channelNum) + ' failed, the wrong link is: ' + testlink)
					else:
						print('channel--%-5s--is new, need to record')
						with open (MD5TXT, 'a+') as checkMD5:
							checkMD5.write('\n')
							checkMD5.write('\n' + 'channel ' + str(channelNum) + ' failed--links for the new channels, the wrong link is: ' + testlink)
	# check over
	print('----------------------------------------------------------------------------------------------------------------------------------------')
	print('links-check finished, all is finished')

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


if __name__ == '__main__':

	options = webdriver.ChromeOptions()
	prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': downloadPath}
	options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome(chrome_options=options)
	downloadApks(publishPath, downloadPath, Net_downloadPath)

