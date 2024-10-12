import pandas as pd
from ics import Calendar, Event
from datetime import datetime

# 读取 CSV 文件
csv_file = '111.csv'

# 尝试用不同编码读取 CSV 文件
try:
    df = pd.read_csv(csv_file, encoding='utf-8', on_bad_lines='skip')  # 跳过错误行
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding='ISO-8859-1', on_bad_lines='skip')  # 如果失败，尝试 ISO-8859-1 编码

# 清理列名，去除多余的空格
df.columns = df.columns.str.strip()

# 创建一个日历对象
calendar = Calendar()

# 遍历 CSV 文件的每一行并创建事件
for index, row in df.iterrows():
    if row['对阵双方'] != '待定':  # 跳过对阵双方为待定的赛事
        event = Event()
        event.name = row['对阵双方'].strip()  # 去除多余空格
        event.location = '待定'  # 根据需要可以设置地点

        # 处理日期和时间
        if row['日期'] != '待定':
            # 将日期字符串转换为datetime对象
            start_time = datetime.strptime(row['日期'], "%Y-%m-%d")
            event.begin = start_time
            event.duration = {'hours': 2}  # 假设每场比赛持续2小时

            calendar.events.add(event)

# 将 ICS 文件保存到本地
ics_file_path = '111.csv.ics'
with open(ics_file_path, 'w', encoding='utf-8') as f:
    f.writelines(calendar)

print("ICS 文件已成功创建！")
