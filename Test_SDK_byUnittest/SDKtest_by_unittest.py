# -*- coding: utf-8 -*- 
import sys, os
sys.path.append('./')
from lib.SDKtest_func import *
from lib.loadSetting import *
from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
from testCase.test_screenshot_channel_version import test_channel_version
from testCase.test_screenshot_energy import test_energy
from testCase.test_screenshot_status import test_status
import HTMLTestRunner
import unittest


__author__ = "zheng.cong"
test_cases_old = (test_channel_version, test_energy)

test_cases_new = (test_channel_version, test_energy)

if __name__ == '__main__':
    
    SDK_test(oldVersion_apk_path, newVersion_apk_path, get_suite)