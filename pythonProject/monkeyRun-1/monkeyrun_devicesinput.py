import subprocess
# package_name = "com.iqiyi.knowledge"
# check_cmd = subprocess.run(["adb", "shell", "pm", "list", "packages", "|", "grep", package_name], shell=True)

import subprocess

package_name = "com.iqiyi.knowledge"
uninstall_cmd = 'adb uninstall {}'.format(package_name)

check_cmd = ["adb", "shell", "pm", "list", "packages", "|", "grep", f'{package_name}']
result = subprocess.run(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if package_name in result.stdout:
    uninstall_result = subprocess.run(uninstall_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if uninstall_result.returncode == 0:
        print('已卸载本地apk')
    else:
        print('卸载命令执行失败：{}'.format(uninstall_result.stderr.strip()))
else:
    print('未找到指定应用')
