from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import unittest


class test_channel_version(unittest.TestCase):
	def setUp(self):
		# 检测是否处于可测试状态
		pass


	def test_channel_version(self):
		test_cmd = 'python -m airtest run G:\\Airtest\\test_screenshot_channel_version.air --device Android://127.0.0.1:5037/172.16.2.77:7777'
		assert_equal(0, os.system(test_cmd))
		

	def tearDown(self):
		# 使游戏回归可测试状态
		pass





