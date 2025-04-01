#주피터에다가 코드 붙여넣기기

import time
import numpy as np
from pop import Util
from pop import Pilot
from IPython.display import clear_output
import cv2

dt_full = 0.08
dt_stop = 0.15

thBin = 80

min_Val = 40; max_Val = 500

deadzone = 0.1

def freeCam(cam,msg):
  cam.release()
  print("\nMain thread finished:", msg)

def getImg(cam):
  ret, frame = cam.read()
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  if not ret:
    freeCam(cam, "read frame error")
  else:
    return frame

def rotation(centerX, width, bot):
  global gain, dt_full, dt_stop, deadzone

  steering = (centerX - (width/2)) / (width/2)
  bot.steering = steering

  if(steering < -deadzone):
    bot.turnLeft()
  elif(steering > deadzone):
    bot.turnRight()
  else:
    bot.stop()
  
  dt = float(dt_full * abs(steering))
  time.sleep(dt)

  bot.stop()
  time.sleep(dt_stop)

  return steering

bot = Pilot.SerBot()
bot.setSpeed(30)

#카메라 초기화화
Util.enable_imshow()
cam = Util.gstrmer(width=320, height=240)
vid = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
if not vid.isOpened():
  print("Not found camera")
else:
  print("Camera initiated")

imgTemp = getImg(vid)
width = imgTemp.shape[1]; height = imgTemp.shape[0]

#index image 만들기기
row_vector = np.arange(1, width+1)
img_X = np.tile(row_vector, (height,1))
img_X = img_X.astype(np.uint16)

frameBg = getImg(vid)
meanX = round(width/2); meanY = round(height/2)

for i in range(240):
  frame = getImg(vid)
  imgDiff = cv2.absdiff(frame, frameBg)
  ret, mask = cv2.threshold(imgDiff, thBin, 1, cv2.THRESH_BINARY)
  imgBin16 = mask.astype(np.uint16)

  img_X2 = cv2.multiply(img_X, imgBin16)
  img_X2 = img_X2.astype(np.unit32)

  count = np.count_nonzero(img_X2)
  if (count > min_Val) and (count < max_Val):
    meanX = round(img_X2.sum()/count)

    steer = rotation(meanX, width, bot)
    print("\rcenter = ", meanX, "(", steer, ")", "count = ", count, end = "")

  if(False):
    maskCp = cv2.multiply(mask, 255)
    imgClr = cv2.cvtColor(maskCP, cv2.COLOR_GRAY2BGR)
  else:
    imgClr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

  cv2.circle(imgClr, (meanX, meanY), 5, (0,0,255), 2)
  cv2.imshow("soda", imgClr)

  time.sleep(0.03)
  frameBg = getImg(vid)

freeCam(vid, 'no error')