from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import unittest


class test_status(unittest.TestCase):
	def setUp(self):
		pass


	def test_status(self):
		test_cmd = 'python -m airtest run G:\\Airtest\\test_screenshot_status.air --device Android://127.0.0.1:5037/172.16.2.77:7777'
		assert_equal(0, os.system(test_cmd))
		

	def tearDown(self):
		pass