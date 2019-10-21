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

# 自动化安装老包 —— 覆盖新包 —— 执行用例
def SDK_test(oldPath, newPath, get_suite):
    
    # 是否自定义所需覆盖安装的渠道或全部覆盖安装         
    if custom_install_option == 'yes':
        oldApk_list = install_list(oldPath, custom_channel_list).install_list_custom()
        newApk_list = install_list(newPath, custom_channel_list).install_list_custom()
    else:
        oldApk_list = install_list(oldPath, None).install_list_all()
        newApk_list = install_list(newPath, None).install_list_all()

    connect_device("Android://127.0.0.1:5037/172.16.2.77:7777")
    cur_device = device()

    with open('SDK_test.txt', 'w+', encoding='utf8') as test_report:
        test_report.write('开始覆盖、执行用例...' + '\n')

    for oldApk in oldApk_list:
        for newApk in newApk_list:
            # apk文件名中渠道相关名称是XXX —— 如果分割出的第三串字符就是日期:
            if oldApk.split('_')[2].isdigit():
                if oldApk.split('_')[1] == newApk.split('_')[1]:
                    # 得到渠道名称
                    channelName = oldApk.split('_')[1]
                    # 根据渠道名称创建文件夹
                    picPath_dir = mkdir_pic_path(channelName)

                    with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                        test_report.write('\n' + '-'*25 + channelName + '-'*25 + '\n')
                    # 安装低版本包
                    with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                        test_report.write('[%s]---低版本%s开始安装---\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                        cur_device.install_app(oldApk, replace=True)
                        test_report.write('[%s]---低版本%s安装成功---\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))

                    sleep(10)

                    # 启动游戏并执行用例
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            # 启动旧版本
                            start_app(i)
                            sleep(10)

                            # 启动后要做的事情：
                            # with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                            
                            # 测试报告
                            report_name = os.path.join(picPath_dir, 'Report_old.html')

                            with open(report_name,'wb') as test_report:
                                runner = HTMLTestRunner.HTMLTestRunner(stream=test_report,
                                title=channelName + 'Test Report',
                                description=u'用例执行情况',
                                verbosity =2)
                                # 创建测试运行器（TestRunner），将测试报告输出到文件中
                                # runner = unittest.TextTestRunner(stream=test_report)
                                runner.run(get_suite(test_cases_old))
                            
                            # 覆盖
                            with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                                test_report.write('[%s]---新版本%s开始安装---\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                                cur_device.install_app(newApk, replace=True)
                                test_report.write('[%s]---新版本%s安装成功---\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                            
                            # 启动新版本
                            start_app(i)
                            sleep(30)  
                            # 启动后要做的事情：
                            
                            # 测试报告
                            report_name = os.path.join(picPath_dir, 'Report_new.html')

                            with open(report_name,'wb') as test_report:
                                runner = HTMLTestRunner.HTMLTestRunner(stream=test_report,
                                title=channelName + 'Test Report',
                                description=u'用例执行情况',
                                verbosity =2)
                                # 创建测试运行器（TestRunner），将测试报告输出到文件中
                                # runner = unittest.TextTestRunner(stream=test_report)
                                runner.run(get_suite(test_cases_new))

                            sleep(60)
                            # 删除这个包
                            uninstall(i)

            # apk文件名中渠道相关名称是XXX_XXX —— 需要同时相同:
            elif oldApk.split('_')[1] == newApk.split('_')[1] and oldApk.split('_')[2] == newApk.split('_')[2]:
                    cur_device.install_app(oldApk, replace=True)
                    print('---低版本%s_%s安装成功---'%(oldApk.split('_')[1], oldApk.split('_')[2]))
                    sleep(10)
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            # 启动，未解决手机安装权限、游戏弹窗、渠道登录等问题
                            start_app(i)
                            sleep(30)
                            # 启动游戏后要做的事情：

                            runner = unittest.TextTestRunner()
                            runner.run(get_suite(test_cases_old))

                            # 覆盖
                            cur_device.install_app(newApk, replace=True)
                            print('---当前版本%s_%s安装成功---'%(oldApk.split('_')[1], oldApk.split('_')[2]))
                            # 启动新的
                            start_app(i)
                            sleep(30)
                            # 启动游戏后要做的事情：

                            runner = unittest.TextTestRunner()
                            runner.run(get_suite(test_cases_new))

                            # 删除这个包
                            uninstall(i)                    


if __name__ == '__main__':
    
    SDK_test(oldVersion_apk_path, newVersion_apk_path, get_suite)