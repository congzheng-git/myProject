import xlrd
import sys, os

class SDKtest_setting(object):
	"""由excel读取关于SDK测试的设置"""
	def __init__(self, path):
		self.path = path
		self.setting_excel = xlrd.open_workbook(self.path)
		self.setting_sheets = self.setting_excel.sheets()[0]

	def oldVersion_apk_path(self):
		return self.setting_sheets.cell(0,1).value

	def newVersion_apk_path(self):
		return self.setting_sheets.cell(2,1).value

	def custom_channel_list(self):
		return self.setting_sheets.cell(4,1).value.split(',')

	def custom_install_option(self):
		return self.setting_sheets.cell(4,7).value


class install_list(object):
	"""根据excel中信息得到需要安装的apk的列表"""
	def __init__(self, path, custom_list):
		self.path = path
		self.custom_list = custom_list
		
	def install_list_all(self):
		return [os.path.join(root, filename) for root, dirs, files, in os.walk(self.path) for filename in files if filename.endswith('apk')]

	def install_list_custom(self):
		return [os.path.join(root, filename) for root, dirs, files, in os.walk(self.path) for filename in files if filename.endswith('apk') for customName in self.custom_list if customName in filename]

class sortFile(object):
	"""获取路径下最新创建的文件夹"""
	def __init__(self, path):
		self.path = path
	def sortFile(self):
		self.dirList = os.listdir(self.path)
		self.dirList.sort(key=lambda fn: os.path.getctime(self.path + '\\' + fn))
		if len(self.dirList) != 0:
			return self.dirList[-1]


screenshot_path = 'G:\\Airtest\\newtest\\screenshot'
# 重试次数、截图存储路径信息		
case_step_tryNum = 3
channelName = sortFile(screenshot_path).sortFile()

settingFile_path = r'G:\Airtest\newtest\newtest.air\Setting.xlsx'
# 读取关于脚本运行的设置
oldVersion_apk_path = SDKtest_setting(settingFile_path).oldVersion_apk_path()
newVersion_apk_path = SDKtest_setting(settingFile_path).newVersion_apk_path()
custom_channel_list = SDKtest_setting(settingFile_path).custom_channel_list()
custom_install_option = SDKtest_setting(settingFile_path).custom_install_option()
