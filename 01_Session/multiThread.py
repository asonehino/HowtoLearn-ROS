import threading
import time
from queue import Queue

#생성자
def data_generator(queue):
  for i in range(10):
    time.sleep(1)
    queue.put(i)
    print(f'Data {i} generated and sent')

#소비자
def data_consumer(queue):
  while True:
    data = queue.get()
    if data is None:
      break
    print(f'Data {data} received')

data_queue = Queue()
generator_thread = threading.Thread(target=data_generator, args={data_queue,})
consumer_thread = threading.Thread(target=data_consumer, args={data_queue,})

generator_thread.start()
consumer_thread.start()

#루프가 끝나는 시점이 달라서 속도가 다르지만
#join을 사용하면 속도를 맞출 수 있다
generator_thread.join()
data_queue.put(None)
consumer_thread.join()

print('All done')