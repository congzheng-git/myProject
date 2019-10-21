# -*- encoding=utf8 -*-
__author__ = "zheng.cong"

from airtest.core.api import *
import time
import pytest
import os, sys
from airtest.core.api import *

import logging
import airtest.utils.logger as logger
logger.get_logger("airtest").setLevel(logging.ERROR)

class Get_config(object):
	def __init__(self):
		self.path = 'Z:\\publish\\android\\China\\6.9.1\\pilot_run'
	
	def get_apks_name(self):
		return ([os.path.join(root, filename) for root, dirs, files, in os.walk(self.path) for filename in files if filename.endswith('apk')])

	def get_devices():
		os.system('adb kill-server')
		os.system('adb start-server')
		connect_device("Android://127.0.0.1:5037/172.16.2.144:7777")
		print('设备已连接:', device())

	def get_channel_name(apkName):
		whole_channelName = os.path.basename(apkName)
		if whole_channelName.split('_')[2].isdigit():
			channelName = whole_channelName.split('_')[1]
		else:
			channelName = whole_channelName.split('_')[1] + '_' + whole_channelName.split('_')[2]
		return channelName

class channelLogin():
	def __init__(self, channelName):
		self.channelName = channelName
	def channelLogin(self):
		if self.channelName == 'vivo':
			if exists(Template(r"tpl1570873650954.png", record_pos=(-0.261, 0.714), resolution=(1080, 1920))):
				sleep(1)
				touch(Template(r"tpl1570873650954.png", record_pos=(-0.261, 0.714), resolution=(1080, 1920)))
				sleep(1)

		elif self.channelName == 'oppo':
			if exists(Template(r"tpl1570873720097.png", record_pos=(0.355, -0.363), resolution=(1080, 1920))):
				sleep(1)

				touch(Template(r"tpl1570873720097.png", record_pos=(0.355, -0.363), resolution=(1080, 1920)))
				sleep(1)

			elif exists(Template(r"tpl1570874787685.png", record_pos=(-0.27, 0.716), resolution=(1080, 1920))):
				sleep(1)

				touch(Template(r"tpl1570874787685.png", record_pos=(-0.27, 0.716), resolution=(1080, 1920)))
				sleep(1)

		elif self.channelName == 'huawei' or self.channelName == 'qq_huawei':
			print(self.channelName)
			if exists(Template(r"tpl1570873588104.png", record_pos=(-0.207, 0.696), resolution=(1080, 1920))):
				touch(Template(r"tpl1570873588104.png", record_pos=(-0.207, 0.696), resolution=(1080, 1920)))
				sleep(1)

			elif exists(Template(r"tpl1571387538084.png", record_pos=(0.445, -0.54), resolution=(1080, 1920))):
				touch(Template(r"tpl1571387538084.png", record_pos=(0.445, -0.54), resolution=(1080, 1920)))
				sleep(1)			  
				
		elif self.channelName == 'tencent' or self.channelName ==  'qq_browser' or self.channelName == 'qq_guanjia':
			if exists(Template(r"tpl1570873686930.png", record_pos=(0.001, 0.682), resolution=(1080, 1920))):
				sleep(1)
				touch(Template(r"tpl1570873686930.png", record_pos=(0.001, 0.682), resolution=(1080, 1920)))
				sleep(1)

class Test_updateCheck(object):
	
	def teardown_class(self):
		for apkName in device().list_app():
			if 'jelly' in apkName:
				uninstall(apkName)
	
	@pytest.fixture
	def log(self):
		log_for_test = logging.getLogger('test_check')
		log_for_test.setLevel(logging.INFO)
		return log_for_test

	@pytest.fixture
	def channelName(self, apkName):
		whole_channelName = os.path.basename(apkName)
		if whole_channelName.split('_')[2].isdigit():
			channelName = whole_channelName.split('_')[1]
		else:
			channelName = whole_channelName.split('_')[1] + '_' + whole_channelName.split('_')[2]
		return channelName
	# @pytest.mark.usefixtures('device_connect')
	# 使用usefixtures的方法会报错——无法识别出fixture的返回(识别成了function)
	# fixture配置成auto且下方不将device_connect配置为参数也会报错,信息同上
	# @pytest.mark.parametrize("apkName", Get_config().get_apks_name())
	def test_install_apks(self, apkName, channelName, log):
		print('start install %s'%(channelName))
		is_installed = False
		device().install_app(apkName, replace=True)
		sleep(10)
		for apkName in device().list_app():
			if 'jelly' in apkName:
				is_installed = True
				break
		assert is_installed, '低版本安装失败'
		log.info('低版本%s安装成功'%(channelName))
	
	@pytest.mark.incremental
	def test_start_apk(self, log):
		start_game = False
		for i in device().list_app():
			if 'jelly' in i:
				start_app(i)
				sleep(10)
				if exists(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920))):
					start_game = True
					break
		# 这里应该判断一下当前运行的app, 但由于有权限弹窗干扰了判断
		# air_adb = r'C:\Users\zheng.cong\AppData\Local\Programs\Python\Python37\lib\site-packages\airtest\core\android\static\adb\windows\adb'
		# cur_app = os.popen(air_adb + ' shell dumpsys window | findstr mCurrentFocus').readlines()
		# for i in cur_app:
		# 	if 'jelly' in cur_app:
		# 		start_game = True
		assert start_game, '启动失败'
		log.info('启动游戏')

	def is_in_game(self):
		if exists(Template(r"tpl1570782212384.png", record_pos=(0.427, -0.824), resolution=(1080, 1920))):
			touch(Template(r"tpl1570782212384.png", record_pos=(0.427, -0.824), resolution=(1080, 1920)))
			if exists(Template(r"tpl1571210117925.png", record_pos=(0.101, -0.027), resolution=(1080, 1920))):
				touch(Template(r"tpl1571210148111.png", record_pos=(0.431, -0.647), resolution=(1080, 1920)))
				return True
		else:
			return False
	
	def phone_authorized(self):
		if exists(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920))):
			sleep(1)

			touch(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920)))
			sleep(1)
			if exists(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920))):
				sleep(1)

				touch(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920)))
				sleep(1)
				if exists(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920))):
					sleep(1)

					touch(Template(r"tpl1570782102183.png", record_pos=(0.244, 0.806), resolution=(1080, 1920)))
					sleep(1)

	@pytest.mark.incremental
	def test_get_in_game(self, channelName, log):
		tryNum = 1
		while not self.is_in_game():
			is_in_game = False
			self.phone_authorized()
			sleep(10)
			try_login = channelLogin(channelName).channelLogin()
			sleep(5)
			if exists(Template(r"tpl1570862752616.png", record_pos=(-0.062, -0.042), resolution=(1080, 1920))):
				touch(Template(r"tpl1570862752616.png", record_pos=(-0.062, -0.042), resolution=(1080, 1920)))
			if tryNum == 4:
				snapshot('G:\\Airtest\\test_upadte.air\\' + channelName + '_登录失败.png')
				break
			tryNum += 1
		else:
			is_in_game = True
			# print('执行点击')
			if exists(Template(r"tpl1570862752616.png", record_pos=(-0.062, -0.042), resolution=(1080, 1920))):
				touch(Template(r"tpl1570862752616.png", record_pos=(-0.062, -0.042), resolution=(1080, 1920)))
		assert is_in_game, '进入游戏失败,需要处理前置渠道登录等'
		log.info('进入游戏主界面')

	@pytest.mark.incremental
	def test_update_opened(self, log):
		try:
			if exists(Template(r"tpl1570779032974.png", record_pos=(-0.426, -0.654), resolution=(1080, 1920))):
				touch(Template(r"tpl1570779032974.png", record_pos=(-0.426, -0.654), resolution=(1080, 1920)))
				sleep(1)
				touch(Template(r"tpl1570779065225.png", record_pos=(0.009, 0.315), resolution=(1080.0, 1920.0)))
				sleep(1)
				is_update_opened = True
			else:
				is_update_opened = False
				snapshot('G:\\Airtest\\test_upadte.air\\' + channelName + '_无更新提醒主界面截图.png')
		except:
			snapshot('G:\\Airtest\\test_upadte.air\\' + channelName + '_无更新提醒主界面截图.png')
			is_update_opened = False
		assert is_update_opened, '此渠道更新提醒未开启'
		log.info('开启了更新提醒')

	@pytest.mark.incremental
	def test_is_downloading(self, log):
		try:
			# 有时候点击开始下载出现进度条后会立即失败,多试几次
			sleep(3)
			tryNum = 1
			while not exists(Template(r"tpl1570793068491.png", record_pos=(-0.151, 0.225), resolution=(1080, 1920))):
				touch(Template(r"tpl1570779032974.png", record_pos=(-0.426, -0.654), resolution=(1080, 1920)))
				sleep(1)
				touch(Template(r"tpl1570779065225.png", record_pos=(0.009, 0.315), resolution=(1080.0, 1920.0)))
				sleep(1)
				# start_update_download(channelName, log)
				tryNum += 1
				if tryNum == 3:
					is_downloading = False
					break
			else:
				is_downloading = True
		except:
			is_downloading = False
		assert is_downloading, '未能正常开始下载'
		log.info('更新提醒开始下载')

	
	@pytest.mark.incremental
	def test_is_downloaded_finished(self, log):
		try:
			if wait(Template(r"tpl1570780317693.png", record_pos=(0.246, 0.8), resolution=(1080, 1920)), timeout=300, interval=10):
				is_downloaded_finished = True
		except:
			snapshot('G:\\Airtest\\test_upadte.air\\' + channelName + '_下载失败.png')
			is_downloaded_finished = False
		assert is_downloaded_finished, '下载失败或超时'
		log.info('新版本下载成功')


if __name__ == '__main__':
	Get_config.get_devices()
	my_cmd = '--apkName'
	for apkName in Get_config().get_apks_name():
		cmd_content = apkName
		channelName = Get_config.get_channel_name(apkName)
		cmd_report = '--html=./report/' + channelName + '_report.html' 
		pytest.main(['-p', 'no:warnings', '-s', '-v', my_cmd, cmd_content, 'test_updateCheck_pytest.py', cmd_report])



