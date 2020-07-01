# -*- encoding=utf8 -*-
from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import unittest
import os, sys
sys.path.append('G:\\Airtest\\testSDK_auto\\test_SDK\\lib')
from SDKtest_func import *
from loadSetting import *

__author__ = "zheng.cong"
# connect_device("Android://127.0.0.1:5037/172.16.2.93:7777")
# cur_device = device()
auto_setup(__file__)

class test_channel_version(unittest.TestCase):
	def setUp(self):
#         cur_device = device()
		# 获取到当前所执行渠道的文件夹路径,如 G:\Airtest\testSDK_auto\test_result\huawei
		self.path = os.path.join(screenshot_path, channelName)
		print(channelName)
		print('确认游戏是否是测试状态')
		# 确认当前游戏状态, 如果不是则走一下登入游戏/跳引导之类的流程
		while not is_test_state():
			# 通过渠道判断登录逻辑
			tryPass(channelName)

		# 目的是最终达到可测试状态
		print('可以开始测试')

	def test_channel_version(self):

		# 点击'设置'，等待，截图
		touch(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920)))
		sleep(3.0)
		is_snapshot = False

		# 这里应该去assert当前游戏的渠道+版本号是不是符合预期, 暂未想到便捷的处理方式

		if exists(Template(r"tpl1573530127377.png", record_pos=(0.103, -0.024), resolution=(720, 1280))):
			# 这里通过根据文件夹下现有的文件数来进行判断——正在截图的是旧版本还是新版本, 应该有更好的方法
			if len(os.listdir(self.path)) == 0:
				picPath_name = self.path + '\\渠道+版本号(旧).jpg'
			else:
				picPath_name = self.path + '\\渠道+版本号(新).jpg'
			# 截图
			pic = snapshot(picPath_name, msg="版本渠道+版本号查看.")
			is_snapshot = True

		self.assertTrue(is_snapshot, msg='未能截图')

		# 命令行运行——性能及准确性不好, 不应使用这种方式
		# test_cmd = 'python -m airtest run G:\\Airtest\\test_screenshot_channel_version.air --device Android://127.0.0.1:5037/172.16.2.77:7777'
		# assert_equal(0, os.system(test_cmd))

	def tearDown(self):
		# 如果有关闭按键则点击, 尽量返回到游戏主界面
		if exists(Template(r"tpl1573530390953.png", record_pos=(0.432, -0.642), resolution=(720, 1280))):
			touch(Template(r"tpl1573530390953.png", record_pos=(0.432, -0.642), resolution=(720, 1280)))





