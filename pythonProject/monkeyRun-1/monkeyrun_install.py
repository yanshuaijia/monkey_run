import subprocess
import time
# import datetime
import requests
import json
import os

# 发送HTTP请求获取数据
url = "http://49.7.32.194:8080/aiyou/code/aiyou.php?act=new_get_job_info&job=knowledgeApp_trunk&bizID=14&os=2"
response = requests.get(url)

# 解析API返回的数据
try:
    data = json.loads(response.text)
    artifacts = next(item["artifacts"] for item in data["data"] if item.get("artifacts"))
    apk_url = next(item["relativePath"] for item in artifacts if item["fileName"].endswith(".apk"))
except (json.JSONDecodeError, KeyError, StopIteration):
    print("API请求失败或返回的数据格式错误")
    exit()

# 下载APK文件到本地
apk_data = requests.get(apk_url)
download_path = "./"
apk_file = apk_url.split("/")[-1]
apk_path = os.path.join(download_path, apk_file)
with open(apk_path, "wb") as f:
    f.write(apk_data.content)

# 判断本地是否有该apk，如果有则进行卸载
package_name = "com.iqiyi.knowledge"
uninstall_cmd = 'adb uninstall {}'.format(package_name)
check_cmd = ["adb", "shell", "pm", "list", "packages", "|", "grep", package_name]
check_result = subprocess.run(check_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if package_name in check_result.stdout:
    uninstall_result = subprocess.run(uninstall_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if uninstall_result.returncode == 0:
        print('已卸载本地apk')
    else:
        print('卸载命令执行失败：{}'.format(uninstall_result.stderr.strip()))
else:
    print('本地未找到指定应用，开始安装apk')
commands = []
intervals = []
device_id = subprocess.check_output(['adb', 'devices']).decode().split('\n')[1].split('\t')[0]
# 安装APK文件到手机
subprocess.Popen(['adb', 'install', apk_path], stdout=subprocess.DEVNULL)
time.sleep(30)
# 判断指定设备的'继续安装'点击
if device_id == 'ad3dec98':
    subprocess.Popen(['adb', 'shell', 'input', 'tap', '300', '2092'], stdout=subprocess.PIPE)
    time.sleep(20)
if device_id == '19111FDF6004QC':
    time.sleep(1)
if device_id == '8DY94DGUY9V8GMJJ':
    subprocess.Popen(['adb', 'shell', 'input', 'tap', '309', '2041'], stdout=subprocess.PIPE)
    time.sleep(20)
# 检查apk是否安装成功
package_name = b"com.iqiyi.knowledge"
check_cmd = ["adb", "shell", "pm", "list", "packages", "|", "grep", package_name]
result = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
print("安装成功" if result.returncode == 0 else "安装失败")

# 跳过协议弹窗和进行登录
device_id = subprocess.check_output(['adb', 'devices']).decode().split('\n')[1].split('\t')[0]

# pixel6  [devicesId:19111FDF6004QC]
if device_id == '19111FDF6004QC':
    commands = [
        ['adb', 'shell', 'am', 'start', '-n', 'com.iqiyi.knowledge/.splash.SplashActivity'],
        ['adb', 'shell', 'input', 'tap', '721', '1534'],
        ['adb', 'shell', 'input', 'tap', '201', '2265'],
        ['adb', 'shell', 'input', 'tap', '212', '1583'],
        ['adb', 'shell', 'input', 'text', '11100001110'],
        ['adb', 'shell', 'input', 'tap', '149', '1028'],
        ['adb', 'shell', 'input', 'text', 'test1110'],
        ['adb', 'shell', 'input', 'tap', '215', '1130'],
        ['adb', 'shell', 'input', 'tap', '540', '1273']
    ]
    intervals = [3, 5, 1, 2, 2, 2, 3, 1, 0]

# oneplus9 [devicesId:ad3dec98]
if device_id == 'ad3dec98':
    commands = [
        ['adb', 'shell', 'am', 'start', '-n', 'com.iqiyi.knowledge/.splash.SplashActivity'],
        ['adb', 'shell', 'input', 'tap', '718', '1531'],
        ['adb', 'shell', 'input', 'tap', '185', '2304'],
        ['adb', 'shell', 'input', 'tap', '257', '1571'],
        ['adb', 'shell', 'input', 'text', '11100001110'],
        ['adb', 'shell', 'input', 'tap', '180', '860'],
        ['adb', 'shell', 'input', 'text', 'test1110'],
        ['adb', 'shell', 'input', 'tap', '537', '1279'],
        ['adb', 'shell', 'input', 'tap', '725', '1377']
    ]
    intervals = [3, 5, 2, 2, 2, 2, 3, 3, 0]
# OPPO K9 Pro [devicesId:8DY94DGUY9V8GMJJ]
if device_id == '8DY94DGUY9V8GMJJ':
    commands = [
        ['adb', 'shell', 'am', 'start', '-n', 'com.iqiyi.knowledge/.splash.SplashActivity'],
        ['adb', 'shell', 'input', 'tap', '718', '1524'],
        ['adb', 'shell', 'input', 'tap', '236', '2252'],
        ['adb', 'shell', 'input', 'tap', '244', '1538'],
        ['adb', 'shell', 'input', 'text', '11100001110'],
        ['adb', 'shell', 'input', 'tap', '214', '1075'],
        ['adb', 'shell', 'input', 'text', 'test1110'],
        ['adb', 'shell', 'input', 'tap', '555', '1280'],
        ['adb', 'shell', 'input', 'tap', '731', '1362']
    ]
    intervals = [3, 5, 2, 2, 2, 2, 3, 3, 0]
for i in range(len(commands)):
    subprocess.run(commands[i])
    time.sleep(intervals[i])

