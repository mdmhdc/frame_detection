import numpy as np
import time
import cv2
from target_detection import target_detection
from analyze import frame_analyze
import logging
import os

class frame_detection():
	def __init__(self):
		self.detection=target_detection()
		self.anal=frame_analyze()
		self.ball_color = 'green'
		self.color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
		              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
		              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
		              }		
		logging.basicConfig(filename='P:/frame_detection/log/'+time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())+'.log',format='%(asctime)s===%(message)s',level=logging.DEBUG,filemode='a',datefmt='"%Y-%m-%d %H:%M:%S')
		self.log=logging

	def run(self,x_max,x_min,delta):
		last_position=0
		frame_count=0
		lose_frames=0
		#测试代码这里用读图片的格式，需要读视频时要更换输入方式
		for s in range(1,179):
			frame = cv2.imread('P:/frame_detection/test_frames/frame{A}.jpg'.format(A=s))  #测试图片的路径
			if True:
				#把读到的帧做目标检测，注意这里返回的结果数据是数组，包含检测帧本身、还有结果坐标。
				detection_result=self.detection.find_target(frame,self.color_dist[self.ball_color])
				#打印结果坐标，调试用
				self.log.info("****************box****************{A}".format(A=detection_result[3]))
				#如果是第一帧，直接初始化位置变量，然后直接进入下一帧的检测
				if frame_count == 0:
					position = detection_result[1]
					last_position = detection_result[1]
					frame_count = frame_count + 1
					self.log.info("position is {A},last_position is {B}".format(A=position,B=last_position))
					#实时显示当前检测的帧和检测结果
					cv2.imshow('frame_detection',detection_result[0])
					cv2.waitKey(1)
					continue
				position=detection_result[1]
				self.log.info("position is {A},last_position is {B}".format(A=position,B=last_position))
				#如果帧位置没变，打印当前帧，并标记error
				if position - last_position == 0:
					#这里其实也包含了环绕的情况，需要想下怎么处理，目前处理只是打印帧后手动检查
					self.log.info("【ERROR】 this frame does not move，please check!!!")
					cv2.imwrite('P:/frame_detection/error_frames/frame{A}.jpg'.format(A=frame_count),detection_result[0])
				else:
					#根据偏移量判断是否丢帧，并计算丢帧数量
					if not self.anal.analyze(position,last_position,delta,x_max-x_min):
						#偏移量大于0，直接算即可
						if position-last_position > 0:
							lose=int((position-last_position)/delta)-1  #减1是因为前一帧的色块本真也有宽度，不能算在丢帧里
							self.log.info("【WARN】 lose {A} framdes".format(A=lose))
							lose_frames=lose_frames+lose
						#偏移量小于0，即为跨边界丢帧的情况，用帧间相对距离计算
						else:
							lenth=x_max-x_min
							lose=int((lenth-last_position+position)/delta)  #这里不需要减1，因为此时当前帧和前一帧的相对位置是反的，此时直接计算得到的就是正确丢帧数
							self.log.info("【WARN】 lose {A} framdes".format(A=lose))
							lose_frames=lose_frames+lose
				#判断完毕，更新变量
				last_position=position
				frame_count=frame_count+1
				cv2.imshow('frame_detection',detection_result[0])
				cv2.waitKey(1)
		self.log.info(("final result ---------frame_count:{A},lose_frames:{B}".format(A=frame_count,B=lose_frames)))
		self.log.info("detection done ^_^")

if __name__ == '__main__':
	s=frame_detection()
	s.run()



