#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as py
import time
import cv2

##这个脚本提取视频帧，用来生成测试用例

print("[INFO] starting video stream")
cap = cv2.VideoCapture('P:/frame_detection/video/hdc.mov')
i=0
while i <= 180: #提取的数量
	ret,frame=cap.read()
	if ret:
		i=i+1
		cv2.imwrite('P:/frame_detection/test_frames/frame{A}.jpg'.format(A=i),frame)
		cv2.putText(frame,str(i),(50,300),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),2)
		cv2.imshow('frames',frame)
		cv2.waitKey(1)
	else:
		break
print("get {A} frames".format(A=i))
cap.release()