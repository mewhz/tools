import requests
import re
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 邮件发送配置
sender = ''  # 发件人邮箱

password = ''  # QQ邮箱授权码(不是QQ密码)

receiver = ''  # 收件人邮箱

smtp_server = 'smtp.qq.com'

smtp_port = 587  # 或者465(SSL)

yesterday = datetime.now() - timedelta(days=1)

today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

user_url = "https://www.linovelib.com/userdetail.php"

book_url = "https://www.linovelib.com/modules/article/bookcase.php"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

cookie = "" # 账号的 Cookie

headers = {

    'User-Agent': user_agent,
    'Cookie': cookie

}

book_list = []

def send_email():
    # 创建邮件内容
    message = MIMEMultipart()
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    message['Subject'] = Header('收藏的轻小说更新啦！', 'utf-8')

    # 邮件正文
    content = today + "\n" + " 和 ".join(str(x) for x in book_list) + " 已更新"
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    try:
        # 连接到SMTP服务器
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        smtp_obj.ehlo()
        smtp_obj.starttls()  # 使用TLS加密

        # 登录
        smtp_obj.login(sender, password)

        # 发送邮件
        smtp_obj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")

        # 关闭连接
        smtp_obj.quit()
    except Exception as e:
        print(f"发送失败: {e}")

# 获取用户积分
def get_integral():
    response = requests.get(user_url, headers=headers)

    content = response.text

    pattern = r'<td colspan="2" class="tdr">(.*?)</td>'

    match = re.findall(pattern, content)

    print("正则获取的列表是:", match)

    if match[3]:
        print(today, "积分:", match[3])
    else:
        print(today, "ERROR")

# 获取图书列表
def get_book_update():

    response = requests.get(book_url, headers=headers)

    content = response.text

    pattern = r'<td[^>]*?>\s*(?:<span[^>]*?>.*?</span>\s*)?<a[^>]*?>(.*?)<\/a><\/td>.*?<td[^>]*?align="center">(.*?)<\/td>'

    # re.DOTALL 可以使 . 匹配换行符
    match = re.findall(pattern, content, re.DOTALL)

    print("正则获取的列表是:", match)

    for title, update_time in match:

        if title != '移除':

            print(f"书名: {title} 更新时间: {update_time}")

            update_time  = datetime.strptime(update_time, "%m-%d/%Y")

            if update_time == yesterday:

                book_list.append(title)

    if len(book_list) > 0:
        send_email()


get_integral()
get_book_update()