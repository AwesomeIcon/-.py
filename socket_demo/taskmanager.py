#!/usr/bin/env python
# coding=utf-8

import random,time,Queue
from multiprocessing.managers import BaseManager

# 发送任务队列
task_queue = Queue.Queue()

# 接受结果队列
result_queue = Queue.Queue()

class QueueManager(BaseManager):
    pass

# 把队列注册到网络上
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

manager = QueueManager(address=('0.0.0.0',5000),authkey='abc')

manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

# 发布几个任务
for i in range(10):
    n = random.randint(0,10000)
    print ('Put task %d...' % n)
    task.put(n)

print 'Try get results...'
for i in range(10):
    r = result.get(timeout=10)
    print ('Result: %s' % r)

manager.shutdown()
