import subprocess
import datetime
import time
import requests
import re
import json
import os
# 调用iu取包接口
url = "http://49.7.32.194:8080/aiyou/code/aiyou.php?act=new_get_job_info&job=knowledgeApp_trunk&bizID=14&os=2"
response = requests.get(url)
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
# 跳过协议弹窗和进行登录，根据不同设备编辑不同坐标
device_id = subprocess.check_output(['adb', 'devices']).decode().split('\n')[1].split('\t')[0]
# pixel6  [devicesId:19111FDF6004QC]
if device_id == '19111FDF6004QC':
    commands = [
        ['adb', 'shell', 'am', 'start', '-n', 'com.iqiyi.knowledge/.splash.SplashActivity'],
        ['adb', 'shell', 'input', 'tap', '745', '1541'],
        ['adb', 'shell', 'input', 'tap', '201', '2265'],
        ['adb', 'shell', 'input', 'tap', '212', '1583'],
        ['adb', 'shell', 'input', 'text', '11100001110'],
        ['adb', 'shell', 'input', 'tap', '149', '1028'],
        ['adb', 'shell', 'input', 'text', 'test1110'],
        ['adb', 'shell', 'input', 'tap', '215', '1130'],
        ['adb', 'shell', 'input', 'tap', '540', '1273']
    ]
    intervals = [3, 5, 1, 2, 2, 2, 3, 1, 3]

# oneplus9 [devicesId:ad3dec98]
if device_id == 'ad3dec98':
    commands = [
        ['adb', 'shell', 'am', 'start', '-n', 'com.iqiyi.knowledge/.splash.SplashActivity'],
        ['adb', 'shell', 'input', 'tap', '718', '1531'],
        ['adb', 'shell', 'input', 'tap', '185', '2304'],
        ['adb', 'shell', 'input', 'tap', '257', '1571'],
        ['adb', 'shell', 'input', 'text', '11100001110'],
        ['adb', 'shell', 'input', 'tap', '225', '1029'],
        ['adb', 'shell', 'input', 'text', 'test1110'],
        ['adb', 'shell', 'input', 'tap', '537', '1279'],
        ['adb', 'shell', 'input', 'tap', '725', '1377']
    ]
    intervals = [3, 5, 2, 2, 2, 2, 3, 3, 3]
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
    intervals = [3, 5, 2, 2, 2, 2, 3, 3, 3]
for i in range(len(commands)):
    subprocess.run(commands[i])
    time.sleep(intervals[i])
# 设置datetime和日志路径
now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
logcat_file_path = f"logcat_{date_time}.log"
monkey_file_path = f"monkey_{date_time}.log"
subprocess.run(['adb', 'logcat', '-c'])
# 运行前设置音量静音
subprocess.run(['adb', 'shell', 'input', 'keyevent', '164'])
# 运行前再重启一次app
subprocess.run(['adb', 'shell', 'am', 'force-stop', 'com.iqiyi.knowledge'])
time.sleep(3)
subprocess.run(['adb', 'shell', 'am', 'start', '-n', 'com.iqiyi.knowledge/.splash.SplashActivity'])
# 运行adb logcat
subprocess.run("adb logcat -c", shell=True)
logcat_process = subprocess.Popen(['adb', 'logcat', '|', 'grep', 'com.iqiyi.knowledge', '-v', 'time', '-f',
                                   f'/sdcard/logcat_{date_time}.log'])
# 运行adb monkey
subprocess.run(['adb', 'shell', 'monkey', '-p', 'com.iqiyi.knowledge', '--pct-syskeys', '0',
                '--pct-touch', '60', '--pct-motion', '5', '--kill-process-after-error',
                '--ignore-timeouts', '--ignore-security-exceptions', '--ignore-crashes',
                '--throttle', '500', '-v-v-v', '200000', '>', f'/sdcard/monkey_{date_time}.log'])

time.sleep(5)
logcat_process.kill()
# 把日志从手机移动到电脑，因为日志不存到手机上没办法锁屏
subprocess.run(['adb', 'pull', f'/sdcard/logcat_{date_time}.log', './'])
subprocess.run(['adb', 'pull', f'/sdcard/monkey_{date_time}.log', './'])
# 提取app_version
package_name = "com.iqiyi.knowledge"
version_cmd = f"adb shell dumpsys package {package_name} | grep versionName"
version_output = subprocess.run(version_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
app_version = version_output.stdout.strip()
match = re.search(r'\d+(\.\d+){2}', app_version)
if match:
    app_version = match.group()
else:
    print("无法提取有效的应用程序版本号")
    exit(1)
# 提取os_version
version_cmd = "adb shell getprop ro.build.version.release"
version_output = subprocess.run(version_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
os_version = version_output.stdout.strip()
# 提取设备型号
model_cmd = "adb shell getprop ro.product.model"
model_output = subprocess.run(model_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
model = model_output.stdout.strip()
# 调用mtt接口提交PMS
api_url = "http://webrec.qiyi.domain/mtt/createbug"
payload = {
    'pms_project': 'LIGHTHOUSEBUG',
    'creater': 'yanshuaijia',
    'assignee': 'yanshuaijia',
    'component': '独立APP安卓',
    'step': 'monkeytest',
    'customfield_10021': 'monkeytest',
    'customfield_10022': 'monkeytest',
    'bug_type': 'kpp_android_check',
    'customfield_11304': 'Monkey Test',
    'app_version': app_version,
    'os_version': os_version,
    'hardware': model
}
keywords = ['FATAL EXCEPTION', 'ANR EXCEPTION', 'VirtualMachineError', 'InternalError', 'OutOfMemoryError', 'IOError',
            'StackOverflowError', 'UnknownError',  'LinkageError', 'NoClassDefFoundError', 'NoSuchMethodError',
            'NoSuchFieldError', 'NoSuchMethodException', 'NoSuchFieldException', 'InterruptedException',
            'InstantiationException', 'IllegalAccessException', 'CloneNotSupportedException', 'ClassNotFoundException',
            'UnsupportedOperationException', 'IndexOutOfBoundsException', 'SecurityException', 'NumberFormatException',
            'NullPointerException', 'NegativeArraySizeException', 'StringIndexOutOfBoundsException',
            'IllegalThreadStateException', 'IllegalStateException', 'IllegalMonitorStateException',
            'IllegalArgumentException', 'BufferOverflowException', 'ArithmeticException', 'ClassCastException',
            'ArrayStoreException', 'ArrayIndexOutOfBoundsException', 'RuntimeException']
# 读取文件并检测编码方式
chunk_size = 64 * 1024 * 1024
buffer = b''  # 初始化缓冲区
with open(logcat_file_path, 'rb') as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        buffer += chunk
    encodings = ['utf-8', 'gbk', 'latin-1']
    lines = None
    for encoding in encodings:
        try:
            decoded_chunk = buffer.decode(encoding)
            lines = decoded_chunk.splitlines()
            break
        except UnicodeDecodeError:
            continue
    if lines is None:
        print("无法解码文件内容")
        exit(1)
    # 继续执行剩余的代码
    total_requests = 0
    success_count = 0
    failure_count = 0
    i = 0
    exception_found = False
    processed_titles = set()  # 存储唯一的 title

    while i < len(lines):
        line = lines[i]
        found = False
        for keyword in keywords:
            if keyword in line and i + 20 < len(lines):
                for j in range(i, i + 20):
                    if "at com.iqiyi.knowledge" in lines[j]:
                        title_lines = line.split("): ", 1)[1].strip()
                        if "Caused by" not in title_lines:
                            desc_lines = lines[i:i + 20]
                            if title_lines not in processed_titles:  # 检查 title 是否已存在
                                payload['title'] = title_lines
                                payload['desc'] = "".join(desc_lines)
                                response = requests.post(api_url, data=payload)
                                processed_titles.add(title_lines)  # 将 title 添加到集合中
                                print("Title:", title_lines)
                                print("Desc:", "".join(desc_lines))
                                print("Response:", response.text)
                                found = True
                                total_requests += 1
                                if response.status_code == 200:
                                    response_data = response.json()
                                    if 'code' in response_data and response_data['code'] == 'A00000':
                                        success_count += 1
                                    else:
                                        failure_count += 1
                                break  # 跳出内部循环
                if found:
                    break  # 跳出外部循环
        i += 1

    if not exception_found:
        print("未出现异常")
    print("总共调用了接口次数:", total_requests)
    print("返回值中code字段为A00000的数量:", success_count)
    print("返回值中code字段非A00000的数量:", failure_count)
