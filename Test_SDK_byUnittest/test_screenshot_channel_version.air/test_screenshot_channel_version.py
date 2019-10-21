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

if test_check():
    testStep(screenshot_for_version_channel, 0, case_step_tryNum, channelName, screenshot_path, channelName)

