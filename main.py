#author zhangtalent
#-recognize code
#--use NW

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
import math


class neuralWork:
    def __init__(self,in_node,hi_node,out_node,lr):
        #初始化基本数据
        self.input_node = in_node
        self.output_node = out_node
        self.hidden_node = hi_node
        self.learning_rate = lr

        #pow() 取 input节点数的根号的倒数 ，正太内取值
        self.weight_ih = np.random.normal(0.0, pow(self.input_node, -0.5), (self.hidden_node, self.input_node))

        #pow() 取 隐藏节点数的根号的倒数 ，正太内取值
        self.weight_ho = np.random.normal(0.0, pow(self.hidden_node, -0.5), (self.output_node, self.hidden_node))

        #print('init:',weight_ho,weight_ih)

    def train(self,input_list,output_list):
        input_datas = input_list.reshape(self.input_node,1)
        #print('now---->',input_datas)
        output_datas = output_list.reshape(self.output_node,1)
        #print(output_datas)
        ih_in = self.weight_ih.dot(input_datas)
        ih_out = np.zeros(self.hidden_node).reshape(self.hidden_node,1)
        for i in range(self.hidden_node):
            ih_out[i][0] = 1/(1+pow(math.exp(ih_in[i][0]),-1))
        ho_in = self.weight_ho.dot(ih_out)
        ho_out = np.zeros(self.output_node).reshape(self.output_node,1)
        for i in range(self.output_node):
            ho_out[i][0] = 1/(1+pow(math.exp(ho_in[i][0]),-1))
        #计算误差（loss function）(tk-ok)^2   -(tk-ok)*sigmoid(sum(w(j,k)*oj)(1-sigmoid(sum(wjk*oj))))*oj
        output_error = output_datas - ho_out
        hidden_error = self.weight_ho.T.dot(output_error)
        self.weight_ho += self.learning_rate*np.dot((output_error*ho_out*(1.0-ho_out)),np.transpose(ih_out))
        self.weight_ih += self.learning_rate*np.dot((hidden_error*ih_out*(1.0-ih_out)),np.transpose(input_datas))
        #print('update:',weight_ho,weight_ih)
        #return hidden_error 

    def query(self,input_list):
        input_datas = input_list.reshape(self.input_node,1)
        ih_in = self.weight_ih.dot(input_datas)
        ih_out = np.zeros(self.hidden_node).reshape(self.hidden_node,1)
        for i in range(self.hidden_node):
            ih_out[i][0] = 1/(1+pow(math.exp(ih_in[i][0]),-1))
        ho_in = self.weight_ho.dot(ih_out)
        ho_out = np.zeros(self.output_node).reshape(self.output_node,1)
        for i in range(self.output_node):
            ho_out[i][0] = 1/(1+pow(math.exp(ho_in[i][0]),-1))
        return ho_out        
        
    