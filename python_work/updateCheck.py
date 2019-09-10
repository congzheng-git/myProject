# -*- coding: gbk -*-
import xlrd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import os
import requests



file_updatelink = 'sys_config.xlsx'


updateExcel = xlrd.open_workbook(filename=file_updatelink)

updateSheet = updateExcel.sheet_by_index(0)

publishPath = r"Z:\android\China\6.9.1"
downloadPath = r"G:\updateCheck"
testlink_col = updateSheet.col(2)
testlink_col_channels = updateSheet.col(4)

# function - get MD5
def getMD5(apk):
	command = 'certutil -hashfile '
	apkname = apk
	MD5 = os.popen(command + apkname + ' MD5').readlines()
	return MD5[1]

# get APK-MD5 in publish
def publishMD5(path):
	MD5TXT = r'G:\MD5check\MD5.txt'
	with open (MD5TXT, 'w+') as checkMD5:
		for root, dirs, files in os.walk(path):
			for filename in files:
				# write in TXT - MD5.TXT
				if filename.endswith('apk'):
					print(filename + ' done')
					checkMD5.write(filename + ': ')
					checkMD5.write(getMD5(os.path.join(root, filename)) + '\n')
	print('----------------------------------------------------------------------------------------------------------------------------------------')
	print('publish--apk--MD5--finished')
	print('----------------------------------------------------------------------------------------------------------------------------------------')

# mactchMD5 between dowload-APKs and publish-APKs
def mactchMD5(path, links_Apks):
	MD5TXT = r'G:\MD5check\MD5.txt'
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
						print(filename + ' done')
						linesMD5 = linesMD5[:pos] + '-----------success-----------' + linesMD5[pos:]
						with open (MD5TXT, 'w') as checkMD5:
							checkMD5.write(linesMD5)
					else:
						with open (MD5TXT, 'a+') as checkMD5:
							# print(links_Apks)
							fileDownload = filename + '.crdownload'
							if fileDownload in links_Apks.values():
								failedApk_link = list(links_Apks.keys())[list(links_Apks.values()).index(fileDownload)]
								checkMD5.write('\n\n' + filename + ' mactches failed, ' + 'from the link: ' + failedApk_link)
							else:
								failedApk_link = list(links_Apks.keys())[list(links_Apks.values()).index(filename)]
								checkMD5.write('\n\n' + filename + ' mactches failed, ' + 'from the link: ' + failedApk_link)

	# print('\n')
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
		print('go on download')
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
		sortFile(path)
	return dirList[-1]

# read excel, download apks
def downloadApks():
	
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
				print('links num:' + str(linkNum))
				# get links in webbroswer
				links_List.append(testlink)
				try:
					driver.get(testlink)
				except TimeoutException:
					print('browser time out: ' + testlink)
					# links_List.append(testlink)
					# driver.get(testlink)
					continue
				waitingTime = 0
				time.sleep(5)
				if sortFile(downloadPath):
					if len(list(links_Apks.values())) > 1:
						if not sortFile(downloadPath) == list(links_Apks.values())[-1]:
							links_Apks[testlink] = sortFile(downloadPath)
						else:
							links_Apks[testlink] = 'Failed - noResponse'
					else:
						links_Apks[testlink] = sortFile(downloadPath)
				# check downloading status
				while not Checkfinished(downloadPath, linkNum, downloadFailedNum):
					print('downloading, wait for 10s...')
					waitingTime += 10
					time.sleep(10)
					# check out-time
					if waitingTime == 50:
						waitingTime = 0
						print('out-time: ' + testlink)
						finishedNum = downloadFinished(downloadPath)
						downloadFailedNum = downloadFailed(linkNum, finishedNum, downloadFailedNum)
	# waiting for out-time
	# print(links_List)
	
	overWaittime = 0
	while len([filename for root, dirs, files, in os.walk(downloadPath) for filename in files if not filename.endswith('apk')]) != 0:
		time.sleep(30)
		overWaittime += 30
		# if overWaittime > 500:
		# 	break
		print('waiting for out-time apks downloading')
	# result
	print('links-Apks:', links_Apks) 
	print('----------------------------------------------------------------------------------------------------------------------------------------')
	print('links num: %-5s'%(linkNum))
	print('apks finished num: %-5s'%(downloadFinished(downloadPath)))
	print('links failed num: %-5s'%(str(int(linkNum) - int(downloadFinished(downloadPath)))))
	print('----------------------------------------------------------------------------------------------------------------------------------------')


	for value in list(links_Apks.values()):
		valueDownload = str(value)
		if valueDownload.endswith('load'):
			if valueDownload.rstrip('.crdownload') in [filename for root, dirs, files, in os.walk(downloadPath) for filename in files]:
				if list(links_Apks.keys())[list(links_Apks.values()).index(value)] in links_List:
					links_List.remove(list(links_Apks.keys())[list(links_Apks.values()).index(value)])
					# print(links_List)
			else: 
				print('not found-', value)
		else:
			if valueDownload in [filename for root, dirs, files, in os.walk(downloadPath) for filename in files]:
				if list(links_Apks.keys())[list(links_Apks.values()).index(value)] in links_List:
					links_List.remove(list(links_Apks.keys())[list(links_Apks.values()).index(value)])
					# print(links_List)
			else: 
				print('not found -', list(links_Apks.keys())[list(links_Apks.values()).index(value)], value)
	if len(links_List) != 0:
		print('failed links: ' ,set(links_List))
	else: 
		print('all links success')
	print('download over')
	print('----------------------------------------------------------------------------------------------------------------------------------------')


	publishMD5(publishPath)
	mactchMD5(downloadPath, links_Apks)

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
					if channelsDict.setdefault(channelNum, None) and channelsDict.setdefault(channelNum, None) in testlink:
						print('channel--%-5s--checked success, %-10s in the update link'%(str(channelNum), channelsDict[channelNum])) 
					else:
						print('channel--%-5s--checked failed, write in the MD5.TXT'%(str(channelNum)))
						with open (MD5TXT, 'a+') as checkMD5:
							checkMD5.write('\n')
							checkMD5.write('\n' + 'channel ' + str(channelNum) + ' failed, the wrong link is: ' + testlink)
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
	'910' : 'langang',
	'916' : 'langang',
	'12' : 'mobilemarket',
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
	'172' : 'game233_test'}


if __name__ == '__main__':

	options = webdriver.ChromeOptions()
	prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'G:\updateCheck'}
	options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome(chrome_options=options)
	downloadApks()


