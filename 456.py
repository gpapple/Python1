from email import encoders
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr,parseaddr
from email.mime.multipart import MIMEMultipart,MIMEBase
import smtplib

def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))

from_addr = '15727702823@163.com'
to_addr = '3429224057@qq.com'
passwd = '51testing'
smtp_server = 'smtp.163.com'

msg = MIMEMultipart('alternative')
msg['From'] = _format_addr('罗密欧<%s>' % from_addr)
msg['to']  = _format_addr('朱丽叶<%s>' % to_addr)
msg['Subject'] = Header('四大悲剧','utf-8').encode()

mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

# 指定图片为当前目录
fp = open('Jellyfish.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# 定义图片 ID，在 HTML 文本中引用
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)

att1 = MIMEText(open('D:/nice.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="new.txt"'
msg.attach(att1)

with open('D:/Koala.jpg', 'rb') as f:
   att2 =  MIMEBase('image', 'jpg', filename='Koala.jpg')
   att2.add_header('Content-Disposition', 'attachment', filename='Koala.jpg')
   att2.add_header('Content-ID', '<0>')
   att2.set_payload(f.read())
   encoders.encode_base64(att2)
   msg.attach(att2)

try:
    ser = smtplib.SMTP_SSL(smtp_server,465)
    ser.login(from_addr,passwd)
    ser.sendmail(from_addr,[to_addr],msg.as_string())
    print('邮件发送成功')
    ser.quit()
except Exception:
    print('邮件发送失败')
