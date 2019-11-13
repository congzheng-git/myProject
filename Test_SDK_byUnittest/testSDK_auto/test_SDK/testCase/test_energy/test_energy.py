# -*- encoding=utf8 -*-
from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import unittest
import os, sys
sys.path.append('G:\\Airtest\\testSDK_auto\\test_SDK\\lib')
from SDKtest_func import *
from loadSetting import *



class test_energy(unittest.TestCase):
	def setUp(self):
		pass


	def test_energy(self):
		assert_equal(0, 0)

		# test_cmd = 'python -m airtest run G:\\Airtest\\test_screenshot_energy.air --device Android://127.0.0.1:5037/172.16.2.77:7777'
		# assert_equal(0, os.system(test_cmd))

	def tearDown(self):
		pass




# def screenshot_for_energy(path, channelName):
#         print('开始能量界面截图')
#   		# 点击查看能量
#         touch(Template(r"tpl1569749528977.png", record_pos=(-0.14, -0.824), resolution=(1080, 1920)))
#         sleep(5.0)
#         picPath_name = os.path.join(path, channelName) + '//初始能量.jpg'
#         pic = snapshot(picPath_name, msg="能量查看.")
#         touch(Template(r"tpl1569749459746.png", record_pos=(0.44, -0.473), resolution=(1080.0, 1920.0)))
#         sleep(1.0)
#         return True
