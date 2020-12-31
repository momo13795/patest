import time
from threading import Thread
class CountDownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)

if __name__ == '__main__':
    c = CountDownTask()
    t = Thread(target=c.run, args=(10,))
    t.start()
    #c.terminate()
    if t.is_alive():
        print('Still running')
    else:
        print('Completed, Go out !')
    t.join()
    if t.is_alive():
        print('Still running')
    else:
        print('Completed, Go out !')
