# -*- coding: utf-8 -*- 
import sys, os

# from lib.loadSetting import 
from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
__author__ = "zheng.cong"

# 自动化安装老包 —— 覆盖新包
def autoInstall_replace(oldPath, newPath):
    # 是否自定义所需覆盖安装的渠道或全部覆盖安装         
    if custom_install_option == 'yes':
        oldApk_list = install_list(oldPath, custom_channel_list).install_list_custom()
        newApk_list = install_list(newPath, custom_channel_list).install_list_custom()
    else:
        oldApk_list = install_list(oldPath, None).install_list_all()
        newApk_list = install_list(newPath, None).install_list_all()

    cur_device = device()
    
    for oldApk in oldApk_list:
        for newApk in newApk_list:
            # 对于文件名中渠道名是XXX_XXX或仅是XXX的处理判断 —— 如果分割出的第三串字符就是日期:
            if oldApk.split('_')[2].isdigit():
                if oldApk.split('_')[1] == newApk.split('_')[1]:
                    # 得到渠道名称
                    channelName = oldApk.split('_')[1]
                    # 根据渠道名称创建文件夹
                    picPath_dir = mkdir_pic_path(channelName)
                    # 安装低版本包
                    a = cur_device.install_app(oldApk, replace=True)
                    print('---低版本%s安装成功---'%(oldApk.split('_')[1]))
                    sleep(10)
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            # 启动旧版本
                            start_app(i)
#                             sleep(30)
                            # 启动游戏后要做的事情：
                                
                            tryNum = 0
                            
                            testStep(screenshot_for_version_channel, tryNum, picPath_dir, os.path.basename(oldApk))
                            
                            
                            # 覆盖
                            cur_device.install_app(newApk, replace=True)
                            print('---当前版本%s安装成功---'%(oldApk.split('_')[1]))
                            # 启动新的
                            start_app(i)
                            sleep(30)
                            # 启动游戏后要做的事情：
                            try:
                                screenshot_for_version_channel(picPath_dir, os.path.basename(oldApk))
                            except TargetNotFoundError:
                                tryPass()
                            sleep(60)
                            # 删除这个包
                            uninstall(i)
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
                            try:
                                screenshot_for_version_channel(picPath_dir, os.path.basename(oldApk))
                            except TargetNotFoundError:
                                tryPass()
                            except FileNotExistError:
                                tryPass()
                            # 覆盖
                            cur_device.install_app(newApk, replace=True)
                            print('---当前版本%s_%s安装成功---'%(oldApk.split('_')[1], oldApk.split('_')[2]))
                            # 启动新的
                            start_app(i)
                            sleep(30)
                            # 启动游戏后要做的事情：
                            try:
                                screenshot_for_version_channel(picPath_dir, os.path.basename(oldApk))
                            except TargetNotFoundError:
                                tryPass()
                            except FileNotExistError:
                                tryPass()
                            except Exception as e:
                                print('错误: ', e)
                            # 删除这个包
                            uninstall(i)					


sys.path.append('g:\\Airtest\\newtest\\newtest.air')
from lib.loadSetting import install_list
from lib.loadSetting import SDKtest_setting
from lib.SDKtest_func import *
# if __name__=='__main__':
#     读取关于脚本运行的设置啊
settingFile_path = r'G:\Airtest\newtest\newtest.air\Setting.xlsx'

oldVersion_apk_path = SDKtest_setting(settingFile_path).oldVersion_apk_path()
newVersion_apk_path = SDKtest_setting(settingFile_path).newVersion_apk_path()
custom_channel_list = SDKtest_setting(settingFile_path).custom_channel_list()
custom_install_option = SDKtest_setting(settingFile_path).custom_install_option()

# 执行     
# connect_device("Android://127.0.0.1:5037/172.16.1.187:7777")
autoInstall_replace(oldVersion_apk_path, newVersion_apk_path)










