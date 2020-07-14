# 无限白嫖脚本
# 使用说明：将下面的部分数据修改为你的，然后挂在腾讯云函数即可
# 本程序基于python3.6开发,仅做技术交流
# 更新时间：2020.07.13
# 作者；ck
import requests
import re
import time
import json
import imaplib
import smtplib

######以下为需要修改的信息##########
####——————请认真阅读——————————####
#主域名,一般情况下不用修改，除非此次站倒闭，理论上兼容所有sspanel系统搭建的机场
url='https://baoziss.xyz'
#需要准备2个邮箱，一个发送，一个接受邮件
#1：修改为你的发件邮箱地址,请使用QQ邮箱
email='fffd@qq.com'
#2：发件邮箱的授权码(需开启POP3/IMAP/SMTP)等服务
password_key='tvogcfh'
#收件人邮箱,支持发送给多人
#示例：take_email= ['aaa@qq.com'，'bbbb@qq.com','ccc@qq.com']
take_email= ['12082@qq.com']
#sever酱获取地址，https://sc.ftqq.com，不会可不填写
sever='SCU963315ead8cf7a620c'
#修改完后挂在腾讯云函数即可，注意，超时时间一定要设置为60s。

######通用信息，全局调用######
#子域名
loginurl =url +'/auth/login'
user = url +'/user#'
checkinUrl = url+'/user/checkin'
deleurl = url+'/user/kill'
sendurl =url+'/auth/send'
regurl = url+'/auth/register'
nodeurl = url+'/user/node'
#使用requests.Session进行cookie保留登陆
ssr = requests.Session()
#默认注册时所用的密码
password='Aa112211'



#登陆进行判断，如果账号不存在则进行注册，存在则效验流量和会员天数。
def login():
    # 带表单的登陆参数
    loginparams = {'email': email, 'passwd': password}
    # post数据实现登陆
    loginhtml = ssr.post(loginurl, data=loginparams).text
    login = json.loads(loginhtml)['ret']
    if login==1:
        print('登陆成功')
        usermessage()
    else:
        print('登陆失败')
        send()

#签到并查询页面信息
def usermessage():
    try:
        loginparams = {'email': email, 'passwd': password}
        # post数据实现登陆
        ssr.post(loginurl, data=loginparams)
        # 签到
        Url = checkinUrl
        urlhtml = ssr.post(Url).text
        checkin = json.loads(urlhtml)['msg']
        print(checkin)
        # 获取网页详情
        userhtml = ssr.get(user).text
        # 查询剩余流量
        pattern = re.compile('(?<=<span class="counter">).*(?=B)')
        userstr = pattern.findall(userhtml)[0]
        userstr1 =userstr.replace('</span>',' ')
        pattern = re.compile('(?<=).*(?=</span>)')
        userstr = pattern.findall(userstr)[0]
        userres = float(userstr)
        if userres <= 0.00:
            print('没流量了')
            deleacc()

        else:
            # 查询剩余天数
            pattern = re.compile('(?<= <span class="counter">).*(?=</span> 天)')
            time = pattern.findall(userhtml)
            if time == []:
                print('可能为永久版')
                # 查询订阅链接
                pattern = re.compile('(?<= data-clipboard-text=").*(?="><i class="malio-v2rayng"></i> 复制 V2Ray 订阅链接)')
                v2rayurl = pattern.findall(userhtml)
                print(v2rayurl)
                v2rayurl = json.dumps(v2rayurl)
                print(v2rayurl)
                # 查询订阅节点详情
                v2ray = ssr.get(nodeurl).text
                pattern = re.compile('(?<=VMess链接: <code>).*(?=</code></div>)')
                v2raytext = pattern.findall(v2ray)
                v2ray = json.dumps(v2raytext)
                print(v2ray)
                data = '签到成功：' + checkin + '\n' + '剩余流量：' + userstr1 + 'B' + '\n\n' + 'v2ray链接为：' + v2ray + '\n\n' + 'v2ray订阅链接链接为：' + v2rayurl
                print(data)
                sendEmail(data)
            else:
                time = int(pattern.findall(userhtml)[0])
                if time == 0:
                    print('没天数了，删除账号重新注册')
                    deleacc()
                else:
                    # 查询订阅链接
                    pattern = re.compile(
                        '(?<= data-clipboard-text=").*(?="><i class="malio-v2rayng"></i> 复制 V2Ray 订阅链接)')
                    v2rayurl = pattern.findall(userhtml)[0]
                    v2rayurl = json.dumps(v2rayurl)
                    print(v2rayurl)
                    # 查询订阅节点详情
                    v2ray = ssr.get(nodeurl).text
                    pattern = re.compile('(?<=VMess链接: <code>).*(?=</code></div>)')
                    v2raytext = pattern.findall(v2ray)
                    v2ray = json.dumps(v2raytext)
                    print(v2ray)
                    data = '签到成功：' + checkin + '\n' + '剩余流量：' + userstr1 + 'B' + '\n\n' + 'v2ray链接为：' + v2ray + '\n\n' + 'v2ray订阅链接链接为：' + v2rayurl
                    print(data)
                    sendEmail(data)
    except Exception as e:
        text='查询页面信息时发生了错误，请查看运行日志'
        print(text)
        lose(text)


#失败通知
def lose(text):
    requests.get('https://sc.ftqq.com/'+sever+'.send?text=SSR签到脚本运行失败&desp=%s' +text)


def sendEmail(data):
    from email.mime.text import MIMEText
    # email 用于构建邮件内容
    from email.header import Header
    # 用于构建邮件头
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = email
    password = password_key
    # 收信方邮箱
    to_addr =  ','.join(take_email)
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(data, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('ss签到状态')
    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr.split(','), msg.as_string())
    # 关闭服务器
    server.quit()

#删除账号
def deleacc():
    print('开始删除账号')
    deleparams = {'passwd': password}
    deleacc = ssr.post(deleurl,data=deleparams).text
    print(deleacc)
    deleacc = json.loads(deleacc)['ret']
    if deleacc ==1 :
        print('账号删除成功')
        send()
    else:
        text = '删除账号时发生了错误，正在重试'
        send()
        print(text)


#发送验证码
def send():

    sendparams = {'email': email}
    send = ssr.post(sendurl, data=sendparams).text
    print(send)
    send = json.loads(send)['ret']
    print(send)
    if send == 1:
        print('验证码发送成功')
        time.sleep(10)
        emailcode()
    elif send == 0:
        print('您已经注册过了')
        usermessage()
    else:
        text = '查询页面信息时发生了错误，请查看运行日志'
        print(text)
        lose(text)

#接受验证码
def emailcode():
    # 账户密码
    emailcode = email
    password = password_key
    # 链接邮箱服务器
    conn = imaplib.IMAP4_SSL("imap.qq.com", 993)
    # 登录
    conn.login(emailcode, password)
    # 收邮件
    INBOX = conn.select("INBOX")
    # 全部邮件
    type, data = conn.search(None, 'ALL')
    # 邮件列表
    msgList = data[0].split()
    # 最后一封
    last = msgList[len(msgList) - 1]
    # 取最后一封
    type, datas = conn.fetch(last, '(RFC822)')
    # 把取回来的邮件写入txt文档
    data = datas[0][1].decode('utf-8')
    pattern = re.compile('(?<=font-weight: 600;">).*(?=</span>)')
    code = pattern.findall(data)
    print('验证码获取成功，开始注册账号')
    time.sleep(5)
    register(code)


#注册账号
def register(data):
    try:

        regparams = {'email': email, 'name': 'ddd', 'passwd':password, 'repasswd': password,
                     'code': '0', 'emailcode': data}
        register = ssr.post(regurl, data=regparams).text
        register = json.loads(register)['ret']
        if register == 1:
            print('注册成功')
            usermessage()
        else:
            print('注册失败,正在重试')
            send()
    except Exception as e:
        text='注册账号时发生了错误，请查看运行日志'
        print(text)
        lose(text)

def main_handler(event, context):
  return login()


if __name__ == '__main__':
    login()
