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
import numpy as np
from PIL import Image
from main import neuralWork
import os
import time
import multiprocessing as mp

#制作二值化数组
def make_imgarr(lena):
    matchitem = [255,255,255]
    img = np.array(lena)
    for i in range(len(img)):
        for j in range(len(img[i])):
            item = img[i][j]
            if (item == matchitem).all():
                #print('match')
                continue
            else:
                img[i][j] = [0,0,0]
    return img
    #print(lena)




#对比结果
def patter_result(arrays,patter_arrays):
    #matchitem = [255,255,255]
    #print(arrays)
    #print('go',patter_arrays)


    matchitem = [1,1,1]
    count_patter_black = 0;
    count_all_black = 0;
    for i in range(len(patter_arrays)):
        for j in range(len(patter_arrays[i])):
            item = patter_arrays[i][j]
            patter_item = arrays[i][j]
            
            ib = 1;
            if item[0] < 0.5:
                ib = 0
            #print(item[0],ib,patter_item[0])
            #print(patter_item)
            if ib == 1:
                #print('match')
                continue
            else:
                if ib == 0 :
                    if patter_item[0] == 0:
                        #print('black')
                        count_all_black +=1
                        count_patter_black +=1
                    else:
                        count_all_black +=1;
    #print(count_patter_black,count_all_black)                
    return float(count_patter_black/count_all_black)


def getCode(img,h,v):   
    '''result = ''
    #print(pos)
    pos = h+13
    end = v+9'''
    #print('长度',h,v,pos,end)
    
    cilpsrc = img#[h:pos,v:end,:3]
    #print(img.shape)
    
    array =Image.fromarray(cilpsrc)
    #print(cilpsrc.shape)
    array.save("D:/download/codeprocess/codetest%s.png" % (h))
    #array = np.array(cilpsrc)
    #array = make_imgarr(array)
    #max = 0.00
    #num = 0
    '''for i in range(0,10):
        patter_img = mpimg.imread("D:/download/codeprocess/code%s.png" % (i))
        patter_array = np.array(patter_img)
        size = patter_result(array,patter_array)
        if  size > max:
            max = size
            num = i
            #print(i,size,max)
        
        #else :
            #print(i,size)
                
    result = str(num)'''
    return cilpsrc    
#array =Image.fromarray(array)
#array.save("D:/download/codeprocess/code%s.png" % (7))

#处理图片，帅选出数字大概位置
def processPic(img):
    lena = mpimg.imread(img)
    pos = 0;
    result = [[],[],[],[]]
    imgresult = [[],[],[],[]]
    arr = [1,2,3,4]
    while pos<60:
        #print(pos)
        end = pos + 15
        cilpsrc = lena[0:20,pos:end,:3]
        array = np.array(cilpsrc)
        array = make_imgarr(array)
        max = 0.00
        num = 0
        barray = array
        #print(barray.shape)
        v = 0
        h = 0
        for i in range(20):
            for j in range(15):
                total = 0
                count = 0
                if i != 0 and j!=0 and i !=19 and j != 14  :
                    for k in range(-1,2):
                        for l in range(-1,2):
                            if array[i+k][j+l][0] == 255 :
                                count += 1
                            
                else:
                    barray[i][j][0] = 255
                    barray[i][j][1] = 255
                    barray[i][j][2] = 255
                    #print(barray[i][j])
                if count > 4:
                    #print(count,i,j)
                    barray[i][j][0] = 255
                    barray[i][j][1] = 255
                    barray[i][j][2] = 255
                    #print(barray[i][j])
                    #barray[i][j][3] == 255
                if  barray[i][j][0] == 0:
                    if h == 0:
                        h = i
                        
                        #print('high',h,i,j,barray[i][j][0])
                    if v == 0:
                        v = j
                    else :
                        if j < v:
                            v = j
                    
                        
              
            
        b = getCode(barray,int(pos/15),v)        
        result[int(pos/15)] = b/255
        imgresult[int(pos/15)] = b
        #print(result)
        pos+=15
    return result,imgresult
#print(processPic("D:/download/codeprocess/9.gif"))
#print(processPic("D:/download/codeprocess/code17.jpg"))
def convert_to_onedarray(fileurl,size):
        datas = np.zeros(size)
        lena = mpimg.imread(fileurl)
        for i in range(len(lena)):
            for j in range(len(lena[i])):
                item = lena[i][j]
                datas[i*15+j] = item[0]*0.99+0.01
        #print(count_patter_black,count_all_black)                
        return datas
#初始化基本数据
#lena = mpimg.imread('D:/web/code.jpg')

###多核
def muilt_run1(q,begin,end,input_node,output_node,hidden_node,learning_rate):
    
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                n = q.get()
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                q.put(n)  
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
      
def muilt_run2(q,begin,end,input_node,output_node,hidden_node,learning_rate):
    
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                n = q.get()
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                q.put(n)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
         
def muilt_run3(q,begin,end,input_node,output_node,hidden_node,learning_rate):
    
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                n = q.get()
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                q.put(n)   
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
      
def muilt_run4(q,begin,end,input_node,output_node,hidden_node,learning_rate):
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                n = q.get()
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                q.put(n) 
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))    
    

'''def muilt_run1(n,begin,end,input_node,output_node,hidden_node,learning_rate):
    #n = q.get()
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
    return n
def muilt_run2(n,begin,end,input_node,output_node,hidden_node,learning_rate):
    #n = q.get()
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
    return n
def muilt_run3(n,begin,end,input_node,output_node,hidden_node,learning_rate):
    #n = q.get()
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
    return n
def muilt_run4(n,begin,end,input_node,output_node,hidden_node,learning_rate):
    #n = q.get()
    for k in range(50):
        for i in range(0,10):
            for j in range(begin,end):
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))    
    return n'''

if __name__ == '__main__':
    start_time = time.time()
    num_indexs = [730,730,730,730,730,730,730,730,730,730]
    input_node = 300
    output_node = 10
    hidden_node = 45
    learning_rate = 0.005
    n = neuralWork(input_node,hidden_node,output_node,learning_rate)       
    for k in range(450):
        for i in range(0,10):
            for j in range(700,num_indexs[i]):
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))
    print('隐藏节点 %s, 迭代 %s ， 训练样本 %s 学习率 %s 训练时长：%s' % (hidden_node,'500','5','0.005',str(time.time() - start_time))) 
    #多进程
    #pool = Pool(processes=4)
    '''for k in range(300):
        for i in range(0,10):
            for j in range(begin,end):
                right_result = i
                right_index = j
                targets = np.zeros(output_node)+0.01
                targets[right_result] = 0.99
                data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                #print('now',n.weight_ih)
        print('训练-->%s次' % (k))  ''' 
    
    '''pool = Pool(4) # 创建线程池，小于等于 cpu 的线程
    st = 100
    while st < 600:
        n = pool.map(muilt_run, [n,st,st+100,input_node,output_node,hidden_node,learning_rate])
        st+=100'''
        
    '''q = mp.Queue()
    q.put(n)
    #要把q放入参数中,若只有q一个参数，一定要加逗号，否则会报错
    for i in range(4):
        p = mp.Process(target=muilt_run1,args=(q,100,200,input_node,output_node,hidden_node,learning_rate,))
        p.start()'''
    #p2 = mp.Process(target=muilt_run2,args=(q,200,300,input_node,output_node,hidden_node,learning_rate,))
    #p3 = mp.Process(target=muilt_run3,args=(q,300,400,input_node,output_node,hidden_node,learning_rate,))
    #p4 = mp.Process(target=muilt_run4,args=(q,400,500,input_node,output_node,hidden_node,learning_rate,))
    #p1.start()
    #p2.start()
    #p3.start()
    
    '''p.join()
    n = q.get()'''
    #res2 = q.get() 
    '''p1 = mp.Process(target=muilt_run1,args=(n,100,200,input_node,output_node,hidden_node,learning_rate))
    p2 = mp.Process(target=muilt_run2,args=(n,200,300,input_node,output_node,hidden_node,learning_rate))
    p3 = mp.Process(target=muilt_run3,args=(n,300,400,input_node,output_node,hidden_node,learning_rate))
    p4 = mp.Process(target=muilt_run4,args=(n,400,500,input_node,output_node,hidden_node,learning_rate))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()'''
    #测试识别率
    rightcount = 0
    resultcount = 0
    #num_indexs = [11,11,11,11,11,11,11,11,15,11]
    #s = requests.Session()
    bb = 0
    while bb<1000:
        s = requests.Session()
        #获取新验证码
        url = 'http://192.168.116.8:801/eportal/?c=main&a=getCode&v=3.0_1567555169953'
        response = s.get(url)
        # 获取的文本实际上是图片的二进制文本
        img = response.content
        cks = response.cookies
        #print(cks)
        if len(cks.keys()) > 0:
            cookies="PHPSESSID="+cks['PHPSESSID']
            #print(cookies)
        else:
            print(cks.keys(),len(cks.keys()))
            bb += 1   
            print('cookie Get Fail')
            continue
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        with open( 'D:/web/code.jpg','wb' ) as f:
            f.write(img)
            
        #开始处理验证码    
        data_res,img_data = processPic('D:/web/code.jpg')
        result_right = np.zeros(4)
        code_str = ''
        for cur in range(4):
            data_cur = np.zeros(input_node)
            lena_cur = data_res[cur] 
            #print(lena_cur.shape)
            #lena_cur = mpimg.imread(fileurl)
            for i in range(len(lena_cur)):
                for j in range(len(lena_cur[i])):
                    item = lena_cur[i][j]
                    data_cur[i*15+j] = item[0]*0.99+0.01 
            #print('current:',n.query(data_cur))
            now_res = np.argmax(n.query(data_cur))
            result_right[cur] = now_res
            code_str += str(int(now_res))
        print(result_right,code_str)
        # 这是一个图片的url
        
        #print(cookies)
        #code_str = processPic('D:/web/code.jpg')
        #print('验证码自动识别结果：',code_str)    
        '''lena = mpimg.imread('D:/web/code.jpg')
        plt.imshow(lena)
        plt.show()

        code_str = input("关闭验证码窗口并输入验证码：")'''
        #比对验证码结果
        #模拟头部信息
        headersp = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Cookie': cookies
            }       
        code = code_str    
        url = "http://192.168.116.8:801/eportal/?c=Portal&a=check_captcha&callback=dr1567554170954&captcha=%s&_=1567554113390" % (code)
        #print(data_1)
        f = s.get(url, headers=headersp, allow_redirects=False)
        res = f.text
        data = res.find('"1"',0)
        if(data>0):
            rightcount += 1
            #保存正确图片
            for cur in range(4):
                data_cur = np.zeros(input_node)
                lena_cur = data_res[cur] 
                #保存图片
                array =Image.fromarray(img_data[cur])
                num_indexs[int(result_right[cur])] += 1
                array.save('D:/python_work/neuralwork/pic/code%s_%s.png' % (int(result_right[cur]),num_indexs[int(result_right[cur])]))
            print('成功')
            #保存完继续训练
            '''for i in range(0,10):
                for j in range(500,num_indexs[i]):
                    right_result = i
                    right_index = j
                    targets = np.zeros(output_node)+0.01
                    targets[right_result] = 0.99
                    data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                    n.train(data,targets)'''
                #print('now',n.weight_ih)    
        #reply = input('依次四个数字-该位置识别正确输入3，错误输入0\n')
        #while len(reply) != 4:
        #    reply = input('输入有误，重试，依次四个数字-该位置识别正确输入3，错误输入0\n')    
        #if reply == '3333':
            
        '''for cur in range(4):
            pos = int(reply[cur:(cur+1)])
            if pos == 3:        
                data_cur = np.zeros(input_node)
                lena_cur = data_res[cur] 
                #保存图片
                array =Image.fromarray(img_data[cur])
                num_indexs[int(result_right[cur])] += 1
                array.save('D:/python_work/neuralwork/pic/code%s_%s.png' % (int(result_right[cur]),num_indexs[int(result_right[cur])]))
                #print(lena_cur.shape)
                #lena_cur = mpimg.imread(fileurl)
                for i in range(len(lena_cur)):
                    for j in range(len(lena_cur[i])):
                        item = lena_cur[i][j]
                        data_cur[i*15+j] = item[0]*0.99+0.01 
                right_result = result_right[cur]
                #print(right_result)
                #right_index = j
                targets = np.zeros(output_node)+0.01
                targets[int(right_result)] = 0.99
                data = data_cur#convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                n.train(data,targets)
                for i in range(0,10):
                    for j in range(1,num_indexs[i]):
                        right_result = i
                        right_index = j
                        targets = np.zeros(output_node)+0.01
                        targets[right_result] = 0.99
                        data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
                        n.train(data,targets)'''
        resultcount += 1
        print('总次数 %s 正确 %s 正确率 %s' % (resultcount,rightcount,float(rightcount/resultcount)))
        bb += 1    