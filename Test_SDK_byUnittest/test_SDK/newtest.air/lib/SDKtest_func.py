from airtest.core.api import *
from airtest.core.android.android import * 
from airtest.aircv.error import *

cur_device = device()

# 测试步骤执行函数 —— 将步骤函数及其参数传入此函数
def testStep(func, basenum, MaxtryNum, channelName, *args, **kwargs):
    # while basenum < MaxtryNum:
    try:
        # 判断步骤是否执行完毕
        isDone = False
        isDone = func(*args, **kwargs)
    except Exception as e:
        print('错误信息: ', e)
        # 容错处理 —— 跳过授权/引导/重启游戏等
        tryPass(channelName)
        # 若执行中途报错
        if not isDone:
            basenum += 1
            # 步骤最多尝试N次
            if basenum == MaxtryNum:
                return
            # 再试一次
            testStep(func, basenum, MaxtryNum, channelName, *args, **kwargs)
    # 无报错
    else:
        return

# 判断游戏是否处于可点击测试的初始状态 —— 无引导覆盖于屏幕上
def is_test_state():
    if exists(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920))):
        touch(Template(r"tpl1568969049545.png", record_pos=(0.435, -0.83), resolution=(1080, 1920)))
        if not exists(Template(r"tpl1569486525811.png", record_pos=(0.106, -0.011), resolution=(1080, 1920))):
            return False
        else:
            touch(Template(r"tpl1569487068913.png", record_pos=(0.392, -0.472), resolution=(1080, 1920)))
            return True
    else:
        return False

# 游戏状态检测
def test_check():
    test_state = is_test_state()
    while not test_state:
        print('不可进行测试，等待10s')
        sleep(10)
        tryPass(channelName)
        print('尝试跳过障碍，等待10s')
        sleep(10)
        test_state =is_test_state()
    return True

# 报错时的处理方法
def tryPass(channelName):
    # 手机权限
    if exists(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920))):
        touch(Template(r"tpl1569484863321.png", record_pos=(0.249, 0.818), resolution=(1080, 1920)))
        sleep(5)
    elif exists(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920))):
        touch(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920)))
        sleep(10)
    # 判断是否进入了游戏界面
    if not exists(Template(r"tpl1569749528977.png", record_pos=(-0.14, -0.824), resolution=(1080, 1920))):
        if channelName == 'huawei':
            # 华为权限
            # elif exists(Template(r"tpl1569484937369.png", record_pos=(0.219, 0.675), resolution=(1080, 1920))):
                # touch(Template(r"tpl1569484937369.png", record_pos=(0.219, 0.675), resolution=(1080, 1920)))
            # 华为更新
            if exists(Template(r"tpl1569555755005.png", record_pos=(-0.209, 0.696), resolution=(1080, 1920))):
                touch(Template(r"tpl1569555755005.png", record_pos=(-0.209, 0.696), resolution=(1080, 1920)))
            # 华为广告
            if exists(Template(r"tpl1569834980051.png", record_pos=(0.444, -0.536), resolution=(1080, 1920))):
                touch(Template(r"tpl1569834980051.png", record_pos=(0.444, -0.536), resolution=(1080, 1920)))
        elif channelName == 'vivo':
            if exists(Template(r"tpl1569485346473.png", record_pos=(-0.309, 0.723), resolution=(1080, 1920))):
                touch(Template(r"tpl1569485346473.png", record_pos=(-0.309, 0.723), resolution=(1080, 1920)))
        # # 进入游戏的首个引导 —— 有集市任务可以完成的引导, 点击后为游戏初始状态(集市内)
        # elif exists(Template(r"tpl1568971751735.png", record_pos=(-0.407, 0.548), resolution=(1080.0, 1920.0))):
        #     touch(Template(r"tpl1568971751735.png", record_pos=(-0.407, 0.548), resolution=(1080.0, 1920.0)))

# 装包授权
def install_authorize():
    if wait(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920)), intervalfunc=my_interval):
        touch(Template(r"tpl1568968956252.png", record_pos=(0.231, 0.805), resolution=(1080, 1920)))
    # elif:  —— 其它各种样式的‘继续’

# 建个文件夹存储各个渠道截图等内容
def mkdir_pic_path(channelName):
    rootPath = r'G:\Airtest\newtest\screenshot'
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

# 创建测试集
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



















