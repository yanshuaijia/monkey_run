import subprocess
import datetime
import time
import requests
import re
import chardet


now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
logcat_file_path = f"logcat_{date_time}.log"
subprocess.run("adb logcat -c", shell=True)
logcat_cmd = f"adb logcat -v time > {logcat_file_path}"
logcat_process = subprocess.Popen(logcat_cmd, shell=True)
monkey_cmd = f"adb shell monkey -p com.iqiyi.knowledge -v 1000 > monkey_{date_time}.log"
monkey_output = subprocess.run(monkey_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

logcat_process.kill()
time.sleep(5)

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
print(app_version)
version_cmd = "adb shell getprop ro.build.version.release"
version_output = subprocess.run(version_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
os_version = version_output.stdout.strip()

model_cmd = "adb shell getprop ro.product.model"
model_output = subprocess.run(model_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
model = model_output.stdout.strip()

keywords = ['Exception']
api_url = "http://webrec.qiyi.domain/mtt/createbug"

payload = {
    'pms_project': 'LIGHTHOUSEBUG',
    'creater': 'yanshuaijia',
    'assignee': 'lijiaying01',
    'component': '独立APP安卓',
    'step': 'monkeytest',
    'customfield_10021': 'monkeytest',
    'customfield_10022': 'monkeytest',
    'bug_type': 'android_crash',
    'customfield_11304': 'Monkey Test',
    'app_version': app_version,
    'os_version': os_version,
    'hardware': model
}

chunk_size = 64 * 1024 * 1024  # 每次读取的字节数 (64MB)
buffer = b''  # 初始化缓冲区

with open(logcat_file_path, 'rb') as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        buffer += chunk

    # 尝试多种编码类型解码
    encodings = ['utf-8', 'gbk', 'latin-1']  # 可根据实际情况添加其他常见编码类型
    lines = None

    for encoding in encodings:
        try:
            decoded_chunk = buffer.decode(encoding)
            lines = decoded_chunk.splitlines()
            break  # 成功解码，跳出循环
        except UnicodeDecodeError:
            continue  # 解码失败，尝试下一个编码类型

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

