import os, sys
lib_path = os.path.abspath(os.path.join('../..'))
sys.path.append(lib_path)

import os
import subprocess
from freehand.taskslib import task_selenium_auto
from freehand.core.timer.base import Base_Timer
from freehand.core.timer.base import TaskTimer_Spider_By_Queue

class TaskTimer_Spider(Base_Timer):
    """定时任务 ———— 爬取数据的的类
    特殊配置
    crawler_method 基于哪种框架的爬取 有 scrapy selenium
        - crawler_method为 scrapy：
        · spiderPath 爬虫项目的路径
        · command 采用scrapy爬取的执行命令 如 Scrapy crawl XXXSpider
        - crawler_method为 selenium：
    """
    def task(self):
        """方案1 单任务执行 每个新任务都创建新线程"""
        if(self.timerConfig['crawler_method']=='scrapy'):
            # 通过os改变工作路径,注意路径是绝对路径，而且还要是\\  只要环境是同一个 这样可以执行对应的爬虫项目
            os.chdir(self.timerConfig['spiderPath'])
            subprocess.Popen(self.timerConfig['command'])
        elif(self.timerConfig['crawler_method']=='selenium'):
            if(self.timerConfig['origin'] == 'douyin'):
                task_selenium_auto.Sele_Spider_Runner.run_douyin(proj_absPath=self.timerConfig['proj_absPath'],crawlUrl_list=self.timerConfig['crawlUrl_list'],
                                                                 origin='douyin')
            elif(self.timerConfig['origin'] == 'kuaishou'):
                task_selenium_auto.Sele_Spider_Runner.run_kuaishou()
            elif(self.timerConfig['origin'] == 'sougou'):
                task_selenium_auto.Sele_Spider_Runner.run_sougou()
            elif(self.timerConfig['origin'] == 'douyin_guxiaocha'):
                task_selenium_auto.Sele_Spider_Runner.run_douyin_guxiaocah(proj_absPath=self.timerConfig['proj_absPath'], crawlUrl_list=self.timerConfig['crawlUrl_list'], origin='douyin')
        else:
            print('crawler_method参数出错')


class TaskTimer_SpiderBy_Queue(TaskTimer_Spider_By_Queue):
    """固定任务 根据参数执行对应爬虫项目"""
    def __init__(self, timerConfig:dict, env_configs_dict:dict):
        TaskTimer_Spider_By_Queue.__init__(self=self, timerConfig=timerConfig, env_configs_dict=env_configs_dict)



