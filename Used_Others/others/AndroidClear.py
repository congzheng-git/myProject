import os, sys
import time

def claer_cur_app():
	cmd_devices = 'adb devices'
	device_info = os.popen(cmd_devices).readlines()
	if 'kill' not in ''.join(device_info):
		if device_info[-2].split()[1] == 'device':
			cmd = 'adb shell dumpsys window w|findstr \/|findstr name='
			cur_app = os.popen(cmd).readlines()
			for i in cur_app:
				if 'jelly' in i or 'mfp' in i:
					cur_appname = i.split('/')[0].split('=')[2]
					if cur_appname[0] != 'P':
						cmd_clear = 'adb shell pm clear ' + cur_appname
						clear_result = os.popen(cmd_clear).readlines()
						if 'Error' not in clear_result[0] and 'not' not in clear_result[0]:
							outcome = '清除成功'
							return outcome
						else:
							outcome = '失败、手机不支持'
							return outcome
					else:
						cmd_clear = 'adb shell pm clear ' + cur_appname[6:]
						clear_result = os.popen(cmd_clear).readlines()
						if 'Error' not in clear_result[0] and 'not' not in clear_result[0]:
							outcome = '清除成功'
							return outcome	
						else:
							outcome = '失败、手机不支持'
							return outcome
				else:
					outcome = '先打开Jelly再点击'
		else:
			outcome = '设备尚未连接成功'
	else:
		outcome = '设备尚未连接成功'
	return outcome

output = claer_cur_app()

print(output)

time.sleep(5)