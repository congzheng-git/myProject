from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import unittest
sys.path.append('../lib')
from SDKtest_func import *
from loadSetting import *


class test_channel_version(unittest.TestCase):
	def setUp(self):
		# 连接手机并检测是否处于可测试状态
		connect_device("Android://127.0.0.1:5037/172.16.2.144:7777")
		is_test_state()
		pass

	def screenshot_for_version_channel(path, channelName):
		# 点击'设置'，等待，截图
		print('开始测试设置界面截图')
		touch(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920)))
		sleep(5.0)
		picPath = os.path.join(path, channelName)
		if len(os.listdir(picPath)) == 0:
			picPath_name = os.path.join(path, channelName) + '\\渠道+版本号(旧).jpg'
		else:
			picPath_name = os.path.join(path, channelName) + '\\渠道+版本号(新).jpg'
		pic = snapshot(picPath_name, msg="版本渠道+版本号查看.")
		return True

	def test_channel_version(self):
		testStep(screenshot_for_version_channel, 0, case_step_tryNum, channelName, screenshot_path, channelName)

	def tearDown(self):
		# 使游戏回归可测试状态
		is_test_state()
		pass





