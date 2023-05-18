

# log_file_path = '/Users/yanshuaijia/PycharmProjects/pythonProject/monkeyRun-2/logcat_2023-05-16_13-41-55.log'  # 替换为实际的日志文件路径
import codecs
def analyze_logs(logs):
    # 在这里实现日志分析逻辑，判断关键字命中规则并调用接口等操作
    for log in logs:
        if 'keyword' in log:
            # 执行调用接口的操作
            print(f"调用接口：{log}")
# 配置文件路径和批次大小
log_file_path = '/Users/yanshuaijia/PycharmProjects/pythonProject/monkeyRun-2/logcat_2023-05-16_13-41-55.log'  # 替换为实际的日志文件路径
batch_size = 1000000  # 调整批次大小以适应你的需求

# 打开日志文件
with codecs.open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
    batch_logs = []
    for line in log_file:
        line = line.strip()
        batch_logs.append(line)
        if len(batch_logs) >= batch_size:
            analyze_logs(batch_logs)
            batch_logs = []
    # 处理剩余的日志（如果有）
    if batch_logs:
        analyze_logs(batch_logs)
