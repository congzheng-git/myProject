# -*- coding: utf-8 -*- 
import sys, os
sys.path.append('./')
sys.path.append('G:\\Airtest\\testSDK_auto\\test_SDK\\lib')
from lib.SDKtest_func import *
from lib.loadSetting import *
from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
from testCase.test_channel_version.test_channel_version import test_channel_version
from testCase.test_energy.test_energy import test_energy
import HTMLTestRunner
import unittest
  
__author__ = "zheng.cong"

# import logging
# import airtest.utils.logger as logger
# logger.get_logger("airtest").setLevel(logging.INFO)

# 根据引入的case组成集合(旧包/新包)
test_cases_old = (test_channel_version, test_energy)
test_cases_new = (test_channel_version, test_energy)
  
def get_suite(test_cases):
    # 创建测试加载器
    loader = unittest.TestLoader()
    # 创建测试包
    suite = unittest.TestSuite()
    # 遍历所有测试类
    for test_class in test_cases:
        # 从测试类中加载测试用例
        tests = loader.loadTestsFromTestCase(test_class)
        # 将测试用例添加到测试包中
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    # 通过主函数进行suite-case的依渠道循环执行
    SDK_test(oldVersion_apk_path, newVersion_apk_path, get_suite, test_cases_old, test_cases_new)