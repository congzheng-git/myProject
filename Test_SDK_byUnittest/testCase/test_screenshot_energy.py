from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import unittest
sys.path.append('../lib')
from SDKtest_func import *
from loadSetting import *


class test_energy(unittest.TestCase):
	def setUp(self):
		# 连接手机并检测是否处于可测试状态
		connect_device("Android://127.0.0.1:5037/172.16.2.144:7777")
		is_test_state()
		pass

	def screenshot_for_energy(path, channelName):
        print('开始能量界面截图')
  		# 点击查看能量
        touch(Template(r"tpl1569749528977.png", record_pos=(-0.14, -0.824), resolution=(1080, 1920)))
        sleep(5.0)
        picPath_name = os.path.join(path, channelName) + '//初始能量.jpg'
        pic = snapshot(picPath_name, msg="能量查看.")
        touch(Template(r"tpl1569749459746.png", record_pos=(0.44, -0.473), resolution=(1080.0, 1920.0)))
        sleep(1.0)
        return True

	def test_energy(self):
		testStep(screenshot_for_energy, 0, case_step_tryNum, channelName, screenshot_path, channelName)

	def tearDown(self):
		# 使游戏回归可测试状态
		is_test_state()
		pass
