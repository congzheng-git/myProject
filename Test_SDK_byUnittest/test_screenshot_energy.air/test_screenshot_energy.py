# -*- encoding=utf8 -*-
__author__ = "zheng.cong"

from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import os, sys
sys.path.append('G:\\Airtest\\newtest\\newtest.air\\lib')
from SDKtest_func import *
from loadSetting import *

auto_setup(__file__)

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



if test_check():
    testStep(screenshot_for_energy, 0, case_step_tryNum, channelName, screenshot_path, channelName)

