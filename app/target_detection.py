#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np

class target_detection():
	def __init__(self):
		pass

	def find_target(self,frame,target):
                # 高斯模糊
                s_frame = cv2.GaussianBlur(frame, (5, 5), 0)
                # 转化成HSV图像                     
                hsv = cv2.cvtColor(s_frame, cv2.COLOR_BGR2HSV) 
                # 腐蚀，粗的变细                
                erode_hsv = cv2.erode(hsv, None, iterations=2)
                # 将制定颜色意外的其他部分去除，并将图像转化为二值化图像                   
                inRange_hsv = cv2.inRange(erode_hsv,target['Lower'],target['Upper'])
                # 在目标区域绘制矩形边框
                cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                c =max(cnts,key=cv2.contourArea,default=0)
                rect = cv2.minAreaRect(c)
                # 获取目标矩形的四个点坐标，返回的是数组，对应从上往下逆时针的坐标，在某几个特定的点坐标顺序有变，需要注意
                box = cv2.boxPoints(rect)
                cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)
                tmp=np.int0(box[3][0])-np.int0(box[1][0])  #计算当前检测目标的宽度，也就是色块的宽度，取第二和第四个点，能应对坐标顺序有变的情况。
                return [frame,np.int0(box[1][0]),tmp,box]
