import sys,os


# app = input('装包拖过来：')

# install_app = 'adb install -r ' + app
# os.popen(install_app)

# # print('安装成功')

# obb = input('obb拖过来：')

# path_obb = 'cd '+ '/sdcard/Android/obb'

# mkdir_cmcm = 'mkdir -p com.jellyblast.cmcm'
# os.popen(path_obb)
# os.popen(mkdir_cmcm)

# push_obb = 'adb push ' + obb + '/sdcard/Android/obb/com.jellyblast.cmcm' 
# os.popen(push_obb)



os.system('adb shell')