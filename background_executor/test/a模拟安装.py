import multiprocessing
import time

def task(progress_queue):
    for i in range(10):
        time.sleep(1)  # 模拟任务执行
        progress_queue.put(i + 1)  # 将进度发送到队列中

if __name__ == "__main__":
    progress_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=task, args=(progress_queue,))
    p.start()

    p.join()
