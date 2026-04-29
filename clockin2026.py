import requests
import csv
import re
import time
import json
import sys
from dotenv import load_dotenv
import os


print(time.strftime("%Y-%m-%d",time.localtime()), time.strftime("%H:%M:%S",time.localtime()))

load_dotenv()
uid = os.getenv("UID")
client = os.getenv("CLIENT")
ENABLE_DINGTALK = os.getenv("ENABLE_DINGTALK", "false").strip().lower() == "true"

string = "_uid="+uid+";__client_id="+client # 这里的string为拼接的cookie

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    #"x-requested-with":"XMLHttpRequest",
    "origin": "https://www.luogu.com.cn",
    "referer": "https://www.luogu.com.cn/",
    "cookie": string
}

response = requests.get("https://www.luogu.com.cn",headers=headers)
response.encoding = 'utf-8'
s = response.text
b = re.search("csrf-token",s)

if(b):
    csrf_token = re.search(r'<meta name="csrf-token" content="(.*?)">', s).group(1)
    headers["x-csrf-token"]=csrf_token
    print("csrf-token: "+csrf_token)
else:
    print("QWQ没找到csrf-token")

def send_dingtalk_msg(content):
    if not ENABLE_DINGTALK:
        return
    url = os.getenv("DINGTALK_WEBHOOK")
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {"content": content}
    }
    requests.post(url, data=json.dumps(data), headers=headers)
    print("钉钉提醒发送成功")

def clockin():
    """
    data = {"content":"3333test4444"}
    url = "https://www.luogu.com.cn/api/feed/postBenben"
    response = requests.post(url=url, data=data, headers=headers)
    print(response.text)
    print("成功发送犇犇")
    """
    response = requests.get("https://www.luogu.com.cn",headers=headers)
    response.encoding = 'utf-8'
    s = response.text
    try:
        daynum = re.search(r'你已经在洛谷连续打卡了 <strong>(.*?)</strong> 天', s).group(1)
    except:
        daynum = ""
    if daynum:
        msg = ""
        print("机房电脑已打卡")
    else:
        # msg = "机房电脑未打卡 "
        msg = ""
        print("机房电脑未打卡")

        url = "https://www.luogu.com.cn/index/ajax_punch"
        response = requests.post(url=url, headers=headers)
        print(f"打卡发送成功 {response.status_code}")

        response = requests.get("https://www.luogu.com.cn",headers=headers)
        response.encoding = 'utf-8'
        s = response.text
        try:
            daynum = re.search(r'你已经在洛谷连续打卡了 <strong>(.*?)</strong> 天', s).group(1)
        except:
            daynum = ""
        if daynum:
            # msg += "服务器打卡成功 "
            print("服务器打卡成功")
        else:
            msg += "服务器打卡失败 请立即处理"
            print("服务器打卡失败")
            send_dingtalk_msg(msg)
            print()
            sys.exit()

    
    fate = "§" + re.search(r'§ (.*?) §', s).group(1) + "§"
    print("运势: "+fate)
    print("打卡天数: "+daynum)

    new_data = {"日期": time.strftime("%Y-%m-%d",time.localtime()), "时刻": time.strftime("%H:%M:%S",time.localtime()), "运势": fate, "天数": daynum}

    with open("data.csv", mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["日期","时刻","运势","天数"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(new_data)

    msg+=f"你已经在洛谷连续打卡了 {daynum} 天"
    send_dingtalk_msg(msg)


p = re.search(r"<h2 style='margin-bottom: 0'>(.*?)</h2>",s)
if p:
    s = p.group()
    p = re.search(r"target=\"_blank\">(.*?)</a>",s)
    print("成功登录1 " + p.group(1))
    clockin()
else:
    p = re.search(r"<h2>欢迎回来，(.*?)</h2>",s)
    if p:
        p = re.search(r"target=\"_blank\">(.*?)</a>",s)
        print("成功登录2 " + p.group(1))
        clockin()
    else:
        ref = "https://www.luogu.com.cn/api/user/search?keyword="+uid
        response = requests.get(ref,headers=headers)
        response.encoding = 'utf-8'
        id = response.json()
        id = id['users'][0]["name"]
        print("登录失败","uid:",uid,"id:",id)
        send_dingtalk_msg("登录失败 请立即处理")
        
print()
time.sleep(3)