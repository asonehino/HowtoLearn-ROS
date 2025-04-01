import cv2
import queue
import threading
import numpy as np

min_Val = 40; max_Val = 1500

threadStat = True
imgSrc = None
imgList = []

imgQ = queue.Queue()

cap = cv2.VideoCapture(0)
ret, imgSrc = cap.read()
if not ret:
  exit()
imgSrc = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2GRAY)
imgQ.put(imgSrc)

width = imgSrc.shape[1]; height = imgSrc.shape[0]
meanX = round(width/2); meanY = round(height/2)

def freeCam(cam, msg):
  cam.release()
  print("\nMain thread finished:", msg)

def getImg(cam):
  ret, frame = cam.read()
  if not ret:
    freeCam(cam, 'read frame error')
  else:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

def capture_thread():
  global threadStat, cap, meanX, meanY

  while threadStat:
    imgSrc = getImg(cap)
    imgQ.put(imgSrc)

    imgBGR = cv2.cvtColor(imgSrc, cv2.COLOR_GRAY2BGR)
    cv2.circle(imgBGR, (meanX, meanY), 5, (0,0,255), 3)
    cv2.imshow('Processed Frame', imgBGR)
    key = cv2.waitKey(10)

    if(key == ord('q')):
      threadStat = False

cap.release()

def processing_thread():
  global threadStat, meanX, meanY

  row_vector = np.arange(1, width+1)
  img_X = np.tile(row_vector, (height,1))
  column_vector = np.arange(1, height+1).reshape(-1,1)
  img_Y = np.tile(column_vector, (1,width))

  img_X = img_X.astype(np.uint16)
  img_Y = img_Y.astype(np.uint16)

  #배경 초기화화
  if not imgQ.empty():
    imgBg = imgQ.get()

  while threadStat:
    if not imgQ.empty():
      imgCur = imgQ.get()
      imgDiff = cv2.absdiff(imgCur, imgBg)
      ret, imgBin = cv2.threshold(imgDiff, 100, 1, cv2.THRESH_BINARY)
      imgBin16 = imgBin.astype(np.uint16)

      img_X2 = cv2.multiply(img_X, imgBin16)
      img_Y2 = cv2.multiply(img_Y, imgBin16)

      count = np.count_nonzero(imgBin16)
      if (count > min_Val) and (count < max_Val):
        meanX = round(img_X2.sum()/count)
        meanY = round(img_Y2.sum()/count)
        print("\rcenter = ", meanX, meanY, count, end = "")

      imgBg = imgCur

    else:
      cv2.waitKey(10)

capture_thread = threading.Thread(target=capture_thread)
processing_thread = threading.Thread(target=processing_thread)

capture_thread.start()
processing_thread.start()

keyVal = input('enter the quit')
threadStat = False

capture_thread.join()
processing_thread.join()