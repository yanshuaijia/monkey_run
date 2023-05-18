import chardet
import codecs
log_file_path = "/Users/yanshuaijia/PycharmProjects/logcat.log"   # 日志文件的路径
keywords = ['FATAL']                # 要搜索的关键字

with open(log_file_path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

lines = None
encodings = ['utf-8', 'gbk', 'latin-1']
for encoding in encodings:
    try:
        with codecs.open(log_file_path, 'r', encoding=encoding) as f:
            # 分批读取文件内容并处理
            while True:
                chunk = f.readlines(10000)  # 每次读取10000行
                if not chunk:
                    break  # 已读完所有行，退出循环
                for line in chunk:
                    # 处理每一行日志
                    # ...
                    pass
    except UnicodeDecodeError:
        continue
i = 0
exception_found = False
while i < len(lines):
    line = lines[i]
    for keyword in keywords:
        if keyword in line and i + 20 < len(lines):
            found = False
            for j in range(i, i + 20):
                if "com.iqiyi.knowledge" in lines[j]:
                    title_line = lines[i].split("): ", 1)[1].strip()
                    if "Caused by" not in title_line:
                        desc_lines = lines[i:i + 20]
                        print("Title:", title_line)
                        print("Desc:", "".join(desc_lines))
                        found = True
                        break
            if found:
                exception_found = True
                break
    i += 1

if not exception_found:
    print("未找到命中规则的异常")
