#coding=utf-8
from freehand.core.manager.base import Manager
import time

"""任务管理器"""

class Default_Manager(Manager):
    def __init__(self, task_type):
        self.crawler_queue = self.init_queue(task_type=task_type)

    def run_manager(self, *tasks):
        # 入队
        self.push_task(self.crawler_queue, tasks)
        # 执行
        while (self.crawler_queue.qsize() != 0):
            """间隔60s执行任务"""
            self.crawler_queue.get()()
            time.sleep(10)
        print('文章爬取任务执行完毕')