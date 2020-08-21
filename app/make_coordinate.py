import numpy as np 
import time
import cv2
from target_detection import target_detection
import os
import logging

class coordinate():
	def __init__(self):
		self.detection=target_detection()
		self.ball_color = 'white'
		self.color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
		              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
		              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
		              'white': {'Lower': np.array([0, 0, 221]), 'Upper': np.array([180, 30, 255])},
		              }		
		logging.basicConfig(filename='P:/frame_detection/log/'+time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())+'.log',format='%(asctime)s===%(message)s',level=logging.DEBUG,filemode='a',datefmt='"%Y-%m-%d %H:%M:%S')
		self.log=logging

	def get_coordinate(self):
		frame_count=0
		count=0
		x_min=0
		x_max=0
		self.log.info("start get coordinate!!")
		#测试代码这里用读图片的格式，需要读视频时要更换输入方式
		for s in range(1,179):
			frame = cv2.imread('P:/frame_detection/test_frames/frame{A}.jpg'.format(A=s))
			if count < 120: #获取2倍帧率的数据，正常来说足够定位到最大和最小坐标点了，超出这个范围的证明丢帧非常严重，不属于这个工具的测试范畴
				detection_result=self.detection.find_target(frame,self.color_dist[self.ball_color])
				#如果是第一帧，标记初始位置，然后直接进入下一帧
				if frame_count == 0:
					x_min=detection_result[1]
					x_max=detection_result[1]
					frame_count=frame_count+1
					continue
				position=detection_result[1]
				if position > x_max:
					x_max=position
				if position < x_min:
					x_min=position
				frame_count=frame_count+1
				count=count+1
		self.log.info(("x_min:{A},x_max:{B}".format(A=x_min,B=x_max)))
		self.log.info("get coordinate done ^_^")
		return [x_max,x_min,int((x_max-x_min)/60)] #60是帧率

		