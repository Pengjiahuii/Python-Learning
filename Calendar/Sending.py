import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 邮件发送者和接收者
sender_email = "pengjiahui7692@gmail.com"
receiver_email = "eugene.liujing.zh@gmail.com"
password = "20040211pjh"  # 使用应用专用密码

# 创建邮件对象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "比赛日历"

# 邮件正文
body = "请查收附带的比赛日历。"
msg.attach(MIMEText(body, 'plain'))

# 附件
filename = "111.csv.ics"  # 你的 .ics 文件名
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename= {filename}')

msg.attach(part)

# 发送邮件
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()  # 启动 TLS 加密
    server.login(sender_email, password)
    server.send_message(msg)

print("邮件发送成功！")
