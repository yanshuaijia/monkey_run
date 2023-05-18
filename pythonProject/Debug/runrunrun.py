import subprocess
import datetime
import time
import chardet
now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
logcat_file_path = f"logcat_{date_time}.log"
monkey_file_path = f"monkey_{date_time}.log"

logcat_process = subprocess.Popen(['adb', 'logcat', '|', 'grep', 'com.iqiyi.knowledge', '-v', 'time', '-f',
                                   f'/sdcard/logcat_{date_time}.log'])
# 运行adb monkey
subprocess.run(['adb', 'shell', 'monkey', '-p', 'com.iqiyi.knowledge', '--pct-syskeys', '0',
                '--pct-appswitch', '20', '--pct-touch', '60', '--pct-motion', '5',
                '--ignore-timeouts', '--ignore-security-exceptions', '--ignore-crashes',
                '--kill-process-after-error', '--throttle', '500', '-v-v-v', '200',
                '>', f'/sdcard/monkey_{date_time}.log'])
time.sleep(5)
logcat_process.kill()
subprocess.run(['adb', 'pull', f'/sdcard/logcat_{date_time}.log', './'])
with open(logcat_file_path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
