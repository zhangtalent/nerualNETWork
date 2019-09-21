import requests
import re
import json
import sys
import rsa
import base64
import binascii
from bs4 import BeautifulSoup
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from trimPicgo import processPic
import threading



global bh
global attempt_count
#登陆
def login():
    s = requests.Session()
    # 这是一个图片的url
    url = 'http://192.168.116.8:801/eportal/?c=main&a=getCode&v=3.0_1567555169953'
    response = s.get(url)
    # 获取的文本实际上是图片的二进制文本
    img = response.content
    cookies="PHPSESSID="+response.cookies['PHPSESSID']
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    with open( 'D:/web/code.jpg','wb' ) as f:
        f.write(img)
    #print(cookies)
    code_str = processPic('D:/web/code.jpg')
    #print('验证码自动识别结果：',code_str)    
    '''lena = mpimg.imread('D:/web/code.jpg')
    plt.imshow(lena)
    plt.show()

    code_str = input("关闭验证码窗口并输入验证码：")'''

    #模拟头部信息
    headersp = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Cookie': cookies
        }
        
    code = code_str    
    url = "http://192.168.116.8:801/eportal/?c=Portal&a=check_captcha&callback=dr1567554170954&captcha=%s&_=1567554113390" % (code)

    #print(data_1)
    #f = s.get(url, headers=headersp, allow_redirects=False)
    #res = f.text
    #data = res.find('"1"',0)

    #url_login = "http://192.168.116.8/drcom/login?callback=dr1567554170962&DDDDD=201610902227&upass=yss870222&0MKKey=123456&R1=0&R3=0&R6=0&para=00&v6ip=&_=1567554113391" 

    #print(data_1)
    #fs = s.get(url_login, headers=headersp, allow_redirects=False)
    #print('No.',c)
    #bh = ''
    #return fs.text,cookies
    
attempt_count = 1
bh = ''
'''while(True):
    print('尝试登录第%s次' % (attempt_count))
    if bh == '':
        res = login()
        data = res.find('张荣生',0)
        if(data>0):
            print('登录成功')
            break;
        attempt_count+=1'''
        
def fun_timer():
    print('尝试登录' )
    if bh == '':
        res,cookie = login()
        data = res.find('荣',0)
        timers = threading.Timer(1,start_timer)
        timers.start()
        global timer  #定义变量
        if(data>0):
            print('登录成功')
            '''timers = threading.Timer(1,start_timer(cookie))
            timers.start()'''
            #break;
        else:
            timer = threading.Timer(1,fun_timer)
            timer.start()

'''def start_timer():
    print('检测断网' )
    if bh == '':
        res = login()
        data = res.find('荣',0)
        global timers  #定义变量
        if(data>0):
            print('登录成功')
            #break;
        else:
            timers = threading.Timer(1,start_timer)
            timers.start()'''

#timer = threading.Timer(0,fun_timer)  #首次启动
#timer.start()    
attempt_count = 0
right = 0
while True:
    login()
    anwser = input('是否正确,正确回复1')
    if anwser == "1" :
        right += 1
        attempt_count += 1
        print('测试:%s次,成功%s次,成功率:%s' % (attempt_count,right,float(right/attempt_count)))
    else :
        attempt_count += 1
        print('测试:%s次,成功%s次,成功率:%s' % (attempt_count,right,float(right/attempt_count)))
