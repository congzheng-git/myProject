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

    # 杀进程重进
#     else:
#         for i in cur_device.list_app():
#             if 'jelly' in i:
#                 stop_app(i)
# # vivo登录
# exists(Template(r"tpl1569485346473.png", record_pos=(-0.309, 0.723), resolution=(1080, 1920)))


# touch(Template(r"tpl1569486187173.png", record_pos=(0.393, 0.598), resolution=(1080, 1920)))

# exists(Template(r"tpl1569485573521.png", record_pos=(0.297, 0.814), resolution=(1080, 1920)))
# touch(Template(r"tpl1569485573521.png", record_pos=(0.297, 0.814), resolution=(1080, 1920)))
# touch(Template(r"tpl1569486225873.png", record_pos=(0.368, 0.486), resolution=(1080, 1920)))

# # 连闯活动
# exists(Template(r"tpl1569486294093.png", record_pos=(-0.356, -0.668), resolution=(1080, 1920)))
# exists(Template(r"tpl1569486271107.png", record_pos=(0.333, 0.087), resolution=(1080, 1920)))


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
        
def my_interval():
    print('pass')

    
    
    
    


















