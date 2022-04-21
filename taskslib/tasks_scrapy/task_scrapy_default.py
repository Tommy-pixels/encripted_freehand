#coding=utf-8
# scrapy 项目默认调用
from core.base.tasksmixin.tasks_scrapy.base import Task_Scrapy

class Task_Default_Scrapy(Task_Scrapy):
    """使用方法： 生成本类实例化对象并执行run()"""
    def __init__(self, env_config):
        self.env_config = env_config

