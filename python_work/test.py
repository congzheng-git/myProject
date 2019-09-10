# -*- coding: utf-8 -*- 
# from selenium import webdriver


# url_test = "http://172.16.1.240:5001/test"
# browser = webdriver.Firefox() 
# browser.get(url_test)

# browser.find_element_by_id('userid').send_keys('拿钱去喝酒')
# 
# 
# class GetTarget(target):
# 	"""get what you need"""
# 	def __init__(self, server):
# 		# super(GetTarget, self).__init__()
# 		self.target = target
# 		self.udata = self.GetServer()['user_data'].find_one(target)

# 	def GetServer():
# 		server = request.values.get('server')
# 		db = mongodb(server)
# 		return db
# 		
# 		
# 		
# -*- coding: utf-8 -*-  
import sys, os
from airtest.core.api import *
from airtest.core.android.android import * 
# import airtest.core.android.android as android
# import airtest.core.api as core

# print(android)
# print(core.device())


# head_channel = {
#     'oppo':'jelly.oppo',
#     'tecent':'jelly.yingyongbao',
# #     'qq_guanjia',
# #     'qq_browser',
#     'vivo': 'jelly.vivo',
#     'huawei':'jelly.huawei',
# #     'qq_huawei
#     'xiaomi':'jelly.xiaomi',
#     'qihoo':'jelly.qihoo',
#     'meizu':'jelly.meizu',    
# }


# def auto_install()
# 定位低金额文件夹，尝试自动化安装
# testPay_files_local = []
# testPay_apkname = []
# testPay_files_dir = r'Z:\JellyBlast\APKs\6.3.0线上低金额'
# # testPay_files_dir = r'\\172.16.0.150\release\JellyBlast\publish\android\国内安卓\6.2.0国内安卓'
# def testPay_files(testPay_files_dir, testPay_files_local):
#     for root, dirs, files in os.walk(testPay_files_dir):
#     	# testPay_files_local.append(root)
#     	for file in files:
#     		apk_path = os.path.join(root, file)
#     		testPay_files_local.append(apk_path)

# testPay_files(testPay_files_dir, testPay_files_local)
# print(testPay_files_local)


# for key in head_channel.keys():
# 	for file_local in testPay_files_local:
# 		if key in file_local:
# 			file_local_dir = os.path.join(testPay_files_local[0], file_local)
# 			# print(file_local_dir)
# 			testPay_apkname.append(file_local_dir)

# print(testPay_apkname)
			# print(key + '>>' + file_local)



# -*- encoding=utf8 -*-
__author__ = "zheng.cong"

from airtest.core.api import *
from airtest.core.android.android import *

import sys, os
import xlrd
auto_setup(__file__)

# autoInstall_oldDir = r'Z:\JellyBlast\publish\android\国内安卓\6.2.0国内安卓\内测包V3【线上用】'

# autoInstall_newDir = r'\\172.16.0.150\release\JellyBlast\publish\android\国内安卓\6.3.0国内安卓\内测包V2'
# 

# with open(r'C:\Users\zheng.cong\Desktop\python_work\rua!\newtest\newtest.air\Path.txt') as p:
# 	path_list = p.readlines()
# 	for i in range(0, len(path_list)):
# 		path_list[i] = path_list[i].rstrip('\n')
# autoInstall_oldDir = path_list[1]
# autoInstall_newDir = path_list[3]


path_excel = xlrd.open_workbook(r'C:\Users\zheng.cong\Desktop\python_work\rua!\newtest\newtest.air\Path.xlsx')

path_sheets = path_excel.sheets()[0]

autoInstall_oldDir = path_sheets.cell(0,1).value

autoInstall_newDir = path_sheets.cell(2,1).value

deviceUsing_info = path_sheets.cell

def autoInstall_replace(autoInstall_oldDir, autoInstall_newDir):
    filter_apk = ['.apk']
    oldApk_list = []
    newApk_list = []  
    oldApk_list = getInstall_list(autoInstall_oldDir, filter_apk, oldApk_list)
    newApk_list = getInstall_list(autoInstall_newDir, filter_apk, newApk_list)
    cur_device = device()
    for oldApk in oldApk_list:
        for newApk in newApk_list:
            if oldApk.split('_')[2].isdigit():
                if oldApk.split('_')[1] == newApk.split('_')[1]:
                    cur_device.install_app(oldApk, replace=True)
                    sleep(10)
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            # 启动，未解决手机安装权限、游戏弹窗、渠道登录等问题
                            start_app(i)
                            # 覆盖
                            cur_device.install_app(newApk, replace=True)
                            # 启动新的
                            start_app(i)
                            sleep(30)
                            # 删除这个包
                            uninstall(i)
            elif oldApk.split('_')[1] == newApk.split('_')[1] and oldApk.split('_')[2] == newApk.split('_')[2]:
                    cur_device.install_app(oldApk, replace=True)
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            # 启动，未解决手机安装权限、游戏弹窗、渠道登录等问题
                            start_app(i)
                            # 覆盖
                            cur_device.install_app(newApk, replace=True)
                            # 启动新的
                            start_app(i)
                            sleep(30)
                            # 删除这个包
                            uninstall(i)					

def getInstall_list(dir, filter_apk, Apk_list):
	for root, dirs, files in os.walk(dir):
		for file in files:
			apk_Path = os.path.join(root, file)
			apkType = os.path.splitext(apk_Path[1])
			for apkType in filter_apk:
				Apk_list.append(apk_Path)
	return Apk_list

# autoInstall_replace(autoInstall_oldDir, autoInstall_newDir)




# cur_device = device()

# print(cur_device.install_app('Z:\\JellyBlast\\publish\\android\\国内安卓\\6.2.0国内安卓\\内测包V2【楼梯问题】\\jelly_mfp_0126_v6.2.0_vc149_Release_0921_6.2.0.apk'))
    	



# school="河河"
# address="河南"
# age=60
# print("%-10s%-10s%-5d"%(school,address,age))

# #format的用法
# print("{:10s}{:10s}{:5d}".format(school,address,age))
# # 

# a = {'a':'1','b':'2'}
# print(a.values())
# c = '1'
# if c in a.values():
#     print('a')
#     
#     
a = ['a']
print(len(a))
if len(a) != 0:
    print('q')