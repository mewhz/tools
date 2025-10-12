import os

import requests
import xmltodict
from dateutil.parser import parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import json

# 蜜柑计划 RSS 订阅地址
mikanani_rss_url = []
# 大橘猫和朋友们周刊 RSS 订阅地址
rrorangeandfriends_rss_url = ""

# 蜜柑计划最后一次更新时间，设置环境变量
rrorangeandfriends_update_time = os.getenv("rrorangeandfriends_update_time")
# 大橘猫和朋友们周刊最后一次更新时间，设置环境变量
mikanani_update_time = os.getenv("mikanani_update_time")

email_title = ""
email_content = ""

# qinglong 的 client_id
client_id = ""
# qinglong 的 client_secret
client_secret = ""
# qinglong 的地址
qinglong_url = ""

# 邮件发送配置
sender = ''  # 发件人邮箱

password = ''  # QQ邮箱授权码(不是QQ密码)

receiver = ''  # 收件人邮箱

smtp_server = 'smtp.qq.com'

smtp_port = 587  # 或者465(SSL)

def init():
    rrorangeandfriends_rss_response = requests.get(rrorangeandfriends_rss_url).text

    mikanani_rss_response = []

    for url in mikanani_rss_url:
        mikanani_rss_response.append(requests.get(url).text)

    rrorangeandfriends_rss_dict = xmltodict.parse(rrorangeandfriends_rss_response)

    mikanani_rss_dict = []

    for response in mikanani_rss_response:
        mikanani_rss_dict.append(xmltodict.parse(response))

    print("=== 获取 RSS 完成 ===")


    for mikanani_rss in mikanani_rss_dict:
        mikanani(mikanani_rss)

    rrorangeandfriends(rrorangeandfriends_rss_dict)

    print("=== 开始更新环境变量 ===")

    update_env()

    print("=== 更新环境变量完成 ===")

    if email_content != "":

        print("=== 开始发送邮件 ===")

        send_email()

def mikanani(rss_dict):

    print("=== 开始解析 mikanani ===")

    # 声明使用全局变量
    global email_content
    global email_title
    global mikanani_update_time

    rss_items = rss_dict['rss']['channel']['item']

    max_time = ""

    for item in rss_items:

        title = item['title']
        pub_date = parse(item['torrent']['pubDate']).strftime("%Y-%m-%d %H:%M:%S")

        # 若获取的时间晚于更新时间
        if pub_date > mikanani_update_time:
            email_content += f"{title} {pub_date}\n"
            if rss_dict['rss']['channel']['title'] is not None:
                temp = rss_dict['rss']['channel']['title'].replace("Mikan Project - ", "")
                if email_title.find(temp) == -1:
                    email_title = email_title + temp.replace("Mikan Project - ", "") + " "
            if max_time == "":
                max_time = pub_date

    if max_time != "":
        mikanani_update_time = max_time

    print("=== mikanani 解析完成 ===")

def rrorangeandfriends(rss_dict):

    print("=== 开始解析 rrorangeandfriends ===")

    # 声明使用全局变量
    global email_content
    global email_title
    global rrorangeandfriends_update_time

    rss_items = rss_dict['rss']['channel']['item']
    max_time = ""

    for item in rss_items:

        title = item['title']
        pub_date = parse(item['pubDate']).strftime("%Y-%m-%d %H:%M:%S")

        # 若获取的时间晚于更新时间
        if pub_date > rrorangeandfriends_update_time:
            email_content += f"{title} {pub_date}\n"
            if max_time == "":
                max_time = pub_date

    if max_time != "":
        rrorangeandfriends_update_time = max_time

    print("=== rrorangeandfriends 解析完成 ===")

def update_env():

    global email_content

    data = json.loads(requests.get(qinglong_url + "/open/auth/token?client_id=" + client_id + "&client_secret=" + client_secret).text)['data']

    auth = "Bearer " + data['token']

    headers = {
        "Accept": "application/json",
        "Authorization": auth
    }

    data = json.loads(requests.get(qinglong_url + "/open/envs?searchValue=rrorangeandfriends_update_time",
                             headers=headers).content.decode('utf-8'))['data']

    response = requests.put(qinglong_url + "/open/envs/", headers=headers,
                            json={
                                "id": data[0]['id'],
                                "name": "rrorangeandfriends_update_time",
                                "value": rrorangeandfriends_update_time
                            }).content.decode('utf-8')

    if json.loads(response)['code'] == 200:
        print("=== rrorangeandfriends 时间更新成功 ===")

    data = json.loads(requests.get(qinglong_url + "/open/envs?searchValue=mikanani_update_time",
                             headers=headers).content.decode('utf-8'))['data']

    response = requests.put(qinglong_url + "/open/envs/", headers=headers,
                            json={
                                "id": data[0]['id'],
                                "name": "mikanani_update_time",
                                "value": mikanani_update_time
                            }).content.decode('utf-8')

    if json.loads(response)['code'] == 200:
        print("=== mikanani 时间更新成功 ===")
        # email_content += "mikanani 时间更新成功\n"

def send_email():
    # 创建邮件内容
    message = MIMEMultipart()
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    message['Subject'] = Header(email_title + "RSS 更新啦！", 'utf-8')

    # 邮件正文
    message.attach(MIMEText(email_content, 'plain', 'utf-8'))

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

if __name__ == '__main__':
    init()
    print(email_content)