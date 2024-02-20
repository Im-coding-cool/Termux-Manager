import time
import sys
import multiprocessing

def display_progress(progress_queue):
    while True:
        if not progress_queue.empty():
            progress = progress_queue.get()
            sys.stdout.write(f"\rProgress: {progress}/10")
            sys.stdout.flush()
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    progress_queue = multiprocessing.Queue()
    display_process = multiprocessing.Process(target=display_progress, args=(progress_queue,))
    display_process.start()

    display_process.join()
