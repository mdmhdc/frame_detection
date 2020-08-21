import numpy as np 
import time
import cv2
from target_detection import target_detection

class test():
	def __init__(self):
		self.detection=target_detection()
		self.ball_color = 'white'
		self.color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
		              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
		              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
		              'white': {'Lower': np.array([0, 0, 221]), 'Upper': np.array([180, 30, 255])},
		              }
	def go(self):
		for s in range(1,178):
			frame = cv2.imread('P:\\frame_detection\\test_frames\\frame{A}.jpg'.format(A=s))
			result=self.detection.find_target(frame,self.color_dist[self.ball_color])
			cv2.imshow("test",result[0])
			cv2.waitKey(1)

if __name__ == '__main__':
	s=test()
	s.go()
