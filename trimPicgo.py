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

'''num_indexs = [11,11,11,11,11,11,11,11,15,11]
input_node = 300
output_node = 10
hidden_node = 50
learning_rate = 0.005
n = neuralWork(input_node,hidden_node,output_node,learning_rate)       
for k in range(300):
    for i in range(0,10):
        for j in range(1,num_indexs[i]):
            right_result = i
            right_index = j
            targets = np.zeros(output_node)+0.01
            targets[right_result] = 0.99
            data = convert_to_onedarray('D:/python_work/neuralwork/pic/code%s_%s.png' % (right_result,right_index),input_node)
            n.train(data,targets)
            #print('now',n.weight_ih)
    print('训练-->%s次' % (k))

#测试识别率
rightcount = 0
resultcount = 0
#num_indexs = [11,11,11,11,11,11,11,11,15,11]
while True:
    data_res,img_data = processPic('D:/web/code.jpg')
    result_right = np.zeros(4)
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
    print(result_right)    
    reply = input('依次四个数字-该位置识别正确输入3，错误输入0\n')
    while len(reply) != 4:
        reply = input('输入有误，重试，依次四个数字-该位置识别正确输入3，错误输入0\n')    
    if reply == '3333':
        rightcount += 1
    for cur in range(4):
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
                    n.train(data,targets)
    resultcount += 1
    print('总次数 %s 正确 %s 正确率 %s' % (resultcount,rightcount,float(rightcount/resultcount))) '''       