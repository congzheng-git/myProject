from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *
import os, sys
sys.path.append('G:\\Airtest\\testSDK_auto\\test_SDK\\lib')
from loadSetting import *
import HTMLTestRunner
import unittest
import logging
import airtest.utils.logger as logger

# cur_device = device() 

# 测试步骤执行函数 —— 将步骤函数及其参数传入此函数
def testStep(func, basenum, MaxtryNum, channelName, *args, **kwargs):
    try:
        # 判断此步骤是否执行顺利, 如果报错——
        func(*args, **kwargs)
    except Exception as e:
        print('错误信息: ', e)
        # 容错处理 —— 跳过授权/引导/重启游戏等
        tryPass(channelName)
        # 若执行中途报错
        basenum += 1
        # 步骤最多尝试N次
        if basenum == MaxtryNum:
            return False
        # 再试一次
        testStep(func, basenum, MaxtryNum, channelName, *args, **kwargs)
    # 无报错
    else:
        return True
    
# 判断游戏是否处于可点击测试的初始状态 —— 无引导覆盖于屏幕上
def is_test_state():
    logger.get_logger("airtest").info('开始检测是否处于测试状态')
    if exists(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920))):
        touch(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920)))
        if not exists(Template(r"tpl1569486525811.png", record_pos=(0.106, -0.011), resolution=(1080, 1920))):
            return False
        else:
            touch(Template(r"tpl1569487068913.png", record_pos=(0.392, -0.472), resolution=(1080, 1920)))
            return True
    else:
        return False
    return True


# def test_check():
#     test_state = is_test_state()
#     while not test_state:
#         print('不可进行测试，等待10s')
#         sleep(10)
#         tryPass(channelName)
#         print('尝试跳过障碍，等待10s')
#         sleep(10)
#         test_state =is_test_state() 
#     return True

# 报错时的处理方法
def tryPass(channelName):
    # 根据是否有设置这个图标判断是否进入了游戏界面
    while not exists(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920))):
        # 手机权限
        if exists(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920))):
            sleep(1)
            touch(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920)))
            sleep(1)
            if exists(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920))):
                sleep(1)
                touch(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920)))
                sleep(1)
                if exists(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920))):
                    sleep(1)
                    touch(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920)))
                    sleep(1)
        elif exists(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920))):
            touch(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920)))
            sleep(5)
        # 不同渠道的登入
        if channelName == 'huawei':
            # 华为权限
            if exists(Template(r"tpl1569484937369.png", record_pos=(0.219, 0.675), resolution=(1080, 1920))):
                sleep(1)
                touch(Template(r"tpl1569484937369.png", record_pos=(0.219, 0.675), resolution=(1080, 1920)))
                sleep(2)
            # 华为自带的更新
            elif exists(Template(r"tpl1569555755005.png", record_pos=(-0.209, 0.696), resolution=(1080, 1920))):
                sleep(1)

                touch(Template(r"tpl1569555755005.png", record_pos=(-0.209, 0.696), resolution=(1080, 1920)))
                sleep(2)

            # 华为广告
            elif exists(Template(r"tpl1569834980051.png", record_pos=(0.444, -0.536), resolution=(1080, 1920))):
                sleep(1)
                touch(Template(r"tpl1569834980051.png", record_pos=(0.444, -0.536), resolution=(1080, 1920)))
                sleep(2)
        elif channelName == 'vivo':
            if exists(Template(r"tpl1569485346473.png", record_pos=(-0.309, 0.723), resolution=(1080, 1920))):
                touch(Template(r"tpl1569485346473.png", record_pos=(-0.309, 0.723), resolution=(1080, 1920)))
                sleep(15)
    else:
        if exists(Template(r"tpl1569486271107.png", record_pos=(0.333, 0.087), resolution=(1080, 1920))):
            sleep(1)
            touch(Template(r"tpl1569486271107.png", record_pos=(0.333, 0.087), resolution=(1080, 1920)))
            sleep(2)
            touch(Template(r"tpl1569486187173.png", record_pos=(0.393, 0.598), resolution=(1080, 1920)))
            sleep(2)
            if exists(Template(r"tpl1569486271107.png", record_pos=(0.333, 0.087), resolution=(1080, 1920))):
                sleep(1)
                touch(Template(r"tpl1569486271107.png", record_pos=(0.333, 0.087), resolution=(1080, 1920)))
                sleep(2)
        if exists(Template(r"tpl1569487276763.png", record_pos=(0.392, -0.644), resolution=(1080, 1920))):
            touch(Template(r"tpl1569487276763.png", record_pos=(0.392, -0.644), resolution=(1080, 1920)))
            sleep(1)
        

    # 杀进程重进
#     else:
#         for i in cur_device.list_app():
#             if 'jelly' in i:
#                 stop_app(i)
# # vivo登录
# exists(Template(r"tpl1569485346473.png", record_pos=(-0.309, 0.723), resolution=(1080, 1920)))



# exists(Template(r"tpl1569485573521.png", record_pos=(0.297, 0.814), resolution=(1080, 1920)))
# touch(Template(r"tpl1569485573521.png", record_pos=(0.297, 0.814), resolution=(1080, 1920)))
# touch(Template(r"tpl1569486225873.png", record_pos=(0.368, 0.486), resolution=(1080, 1920)))

# # 连闯活动
# exists(Template(r"tpl1569486294093.png", record_pos=(-0.356, -0.668), resolution=(1080, 1920)))


# # 关卡开始界面
# exists(Template(r"tpl1569487276763.png", record_pos=(0.392, -0.644), resolution=(1080, 1920)))

# # 马戏团
# exists(Template(r"tpl1569487068913.png", record_pos=(0.392, -0.472), resolution=(1080, 1920)))

# # 马拉松
# exists(Template(r"tpl1569487137533.png", record_pos=(0.001, 0.4), resolution=(1080, 1920)))
# exists(Template(r"tpl1569487180115.png", record_pos=(0.005, 0.527), resolution=(1080, 1920)))
# exists(Template(r"tpl1569487239591.png", record_pos=(-0.03, -0.617), resolution=(1080, 1920)))
# exists(Template(r"tpl1569487276763.png", record_pos=(0.41, -0.552), resolution=(1080, 1920)))

# # 礼包

# exists(Template(r"tpl1569487362305.png", record_pos=(0.398, -0.371), resolution=(1080, 1920)))


# # 玩具之家
# exists(Template(r"tpl1569487680344.png", record_pos=(0.385, -0.638), resolution=(1080, 1920)))


# 装包授权
def install_authorize():
    if wait(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920)), intervalfunc=my_interval):
        touch(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920)))
    # elif:  —— 其它各种样式的‘继续’

# 各式引导跳过
def guide_task():
    # 进入游戏的首个引导 —— 有集市任务可以完成的引导, 点击后为游戏初始状态(集市内)
    if wait(Template(r"tpl1568971751735.png", record_pos=(-0.407, 0.548), resolution=(1080.0, 1920.0)), timeout=60, intervalfunc=my_interval):
        touch(Template(r"tpl1568971751735.png", record_pos=(-0.407, 0.548), resolution=(1080.0, 1920.0)))
        
# 建个文件夹存储各个渠道报告
def mkdir_pic_path(channelName):
    rootPath = r'G:\Airtest\testSDK_auto\test_result'
    picPath = os.path.join(rootPath, channelName)
    if not os.path.exists(picPath):
        os.mkdir(picPath)
    return picPath 
    
# 截图查看渠道/版本
def screenshot_for_version_channel(path, apkName):
    # 点击'设置'，等待，截图
        touch(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920)))
        sleep(5.0)
        picPath = os.path.join(path, apkName) + '.jpg'
        pic = snapshot(picPath, msg="版本渠道+版本号查看.")
        return True

# 自动化安装老包 —— 覆盖新包 —— 执行用例
def SDK_test(oldPath, newPath, get_suite, test_cases_old, test_cases_new):
    
    # 是否自定义所需覆盖安装的渠道         
    if custom_install_option == 'yes':
        oldApk_list = install_list(oldPath, custom_channel_list).install_list_custom()
        newApk_list = install_list(newPath, custom_channel_list).install_list_custom()
    else:
        # 非自定义即遍历整个安装列表进行安装
        oldApk_list = install_list(oldPath, None).install_list_all()
        newApk_list = install_list(newPath, None).install_list_all()

    # 连接手机(本地接口+手机ip), 得到当前的手机对象
    connect_device("Android://127.0.0.1:5037/172.16.2.93:7777")
    cur_device = device()

    # 测试报告写入
    # with open('SDK_test.txt', 'w+', encoding='utf8') as test_report:
    #     test_report.write('开始覆盖、执行用例...' + '\n')

    for oldApk in oldApk_list:
        for newApk in newApk_list:
            # apk文件名中渠道名称是XXX —— 如果分割出的第三串字符是日期:
            if oldApk.split('_')[2].isdigit():
                if oldApk.split('_')[1] == newApk.split('_')[1]:
                    # 得到渠道名称
                    channelName = oldApk.split('_')[1]
                    # 根据渠道名称创建一个文件夹
                    picPath_dir = mkdir_pic_path(channelName)

                    # 报告中标识开始测试此渠道
                    # with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                    #     test_report.write('\n' + '-'*25 + channelName + '-'*25 + '\n')
                     
                    # 安装低版本包
                    # with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                    #     test_report.write('[%s]---低版本%s开始安装---\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                    #     cur_device.install_app(oldApk, replace=True)
                    #     test_report.write('[%s]---低版本%s安装成功---\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                    # cur_device.install_app(oldApk, replace=True)
                    print('---低版本%s安装成功---'%(channelName))
                    sleep(10)

                    # 启动游戏, 开始执行用例
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            # 启动旧版本
                            start_app(i)
                            sleep(10)
                            # Web测试报告
                            report_name = os.path.join(picPath_dir, 'Report_old.html')

                            with open(report_name,'wb') as test_report:
                                # 创建unittest运行对象并指明Web测试报告信息, verbosity的值决定执行结果信息的详细程度
                                runner = HTMLTestRunner.HTMLTestRunner(stream=test_report,
                                title=channelName + ' Test Report',
                                description=u'用例执行情况',
                                verbosity=2)

                                # 创建测试运行器（TestRunner），将测试报告输出到文件中
                                # runner = unittest.TextTestRunner(stream=test_report)
                                
                                # 开始执行集合成了suite的case(旧版本的包需要确认些什么)
                                runner.run(get_suite(test_cases_old))
                            
                            # 覆盖
                            # with open('SDK_test.txt', 'a+', encoding='utf8') as test_report:
                            #     test_report.write('[%s]---新版本%s开始安装---\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                            #     cur_device.install_app(newApk, replace=True)
                            #     test_report.write('[%s]---新版本%s安装成功---\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), channelName))
                            cur_device.install_app(newApk, replace=True)
                            print('---当前版本%s安装成功---'%(channelName))
                            
                            # 启动新版本
                            start_app(i)
                            sleep(10)  
                            report_name = os.path.join(picPath_dir, 'Report_new.html')

                            with open(report_name,'wb') as test_report:
                                runner = HTMLTestRunner.HTMLTestRunner(stream=test_report,
                                title=channelName + 'Test Report',
                                description=u'用例执行情况',
                                verbosity=2)

                                # 创建测试运行器（TestRunner），将测试报告输出到文件中
                                # runner = unittest.TextTestRunner(stream=test_report)
                                
                                # 开始执行集合成了suite的case(新版本的包需要确认些什么)
                                runner.run(get_suite(test_cases_new))

                            sleep(20)
                            # 删除这个包
                            uninstall(i)

            # apk文件名中渠道相关名称是XXX_XXX —— 需要同时相同:
            elif oldApk.split('_')[1] == newApk.split('_')[1] and oldApk.split('_')[2] == newApk.split('_')[2]:
                    sleep(10)
                    channelName = oldApk.split('_')[1] + '_' + oldApk.split('_')[2]
                    picPath_dir = mkdir_pic_path(channelName)
                    cur_device.install_app(oldApk, replace=True)
                    print('---低版本%s_%s安装成功---'%(oldApk.split('_')[1], oldApk.split('_')[2]))
                    for i in cur_device.list_app():
                        if 'jelly' in i:
                            start_app(i)
                            sleep(10)
                            
                            report_name = os.path.join(picPath_dir, 'Report_old.html')
                            with open(report_name,'wb') as test_report:
                                runner = HTMLTestRunner.HTMLTestRunner(stream=test_report,
                                title=channelName + ' Test Report',
                                description=u'用例执行情况',
                                verbosity=2)

                            cur_device.install_app(newApk, replace=True)
                            print('---当前版本%s_%s安装成功---'%(oldApk.split('_')[1], oldApk.split('_')[2]))
                            start_app(i)
                            sleep(30)
                             
                            report_name = os.path.join(picPath_dir, 'Report_new.html')

                            with open(report_name,'wb') as test_report:
                                runner = HTMLTestRunner.HTMLTestRunner(stream=test_report,
                                title=channelName + 'Test Report',
                                description=u'用例执行情况',
                                verbosity=2)
                            uninstall(i)                    











