import time
import numpy as np
import cv2

def freeCam(cam, msg):
  cam.release()
  print("\nMian thread finished: ", msg)

def getImg(cam):
  ret, frame = cam.read()
  if not ret:
    freeCam(cam, '프레임 읽기 에러')
  else:
    return frame

#카메라 초기화
vid = cv2.VideoCapture(0)
if not vid.isOpened():
  print("카메라 없다")
  exit()
else:
  print("카메라 시작")

imgTemp = getImg(vid)
width = imgTemp.shape[1]; height = imgTemp.shape[0]

row_vector = np.arange(1, width+1)
img_X = np.tile(row_vector, (height, 1))

column_vector = np.arange(1, height+1).reshape(-1, 1)
img_Y = np.tile(column_vector, (1, width))

img_X = img_X.astype(np.uint16)
img_Y = img_Y.astype(np.uint16)

frameBg = getImg(vid)
frameBg = cv2.cvtColor(frameBg.copy(), cv2.COLOR_BGR2GRAY)
meanX = round(width/2); meanY = round(height/2)

while(True):
  frame = getImg(vid)
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  imgDiff = cv2.absdiff(frame, frameBg)
  ret, mask = cv2.threshold(imgDiff, 120, 1, cv2.THRESH_BINARY)
  maskCp = cv2.multiply(mask, 255)
  imgBin16 = mask.astype(np.uint16)

  img_X2 = cv2.multiply(img_X, imgBin16)
  img_Y2 = cv2.multiply(img_Y, imgBin16)

  img_X2 = img_X2.astype(np.uint32)
  img_Y2 = img_Y2.astype(np.uint32)

  count = np.count_nonzero(img_X2)
  if count > 300:
    meanX = round(img_X2.sum()/count)
    meanY = round(img_Y2.sum()/count)

    print('\rcenter = ', meanX, meanY, count, end="")

  imgClr = cv2.cvtColor(maskCp, cv2.COLOR_GRAY2BGR)
  cv2.circle(imgClr, (meanX, meanY), 5, (0,0,255), 2)
  cv2.imshow("soda", imgClr)

  key = cv2.waitKey(33)
  if (key==ord('q')):
    break

freeCam(vid, "no error")