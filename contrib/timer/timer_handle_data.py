import os, sys
lib_path = os.path.abspath(os.path.join('../..'))
sys.path.append(lib_path)

from freehand.taskslib.tasks_postdata.old_datapool import task_post_comment, task_post_articles, task_post_thumbnail, task_post_relateparagraph, task_post_keyparagraph, task_post_contentimg

from freehand.core.timer.base import Base_Timer
"""处理数据相关的定时器"""
class TaskTimer_AutoDealwithPost(Base_Timer):
    """定时任务 ———— 处理数据及上传 段落数据 到接口的类（完成）"""
    def task(self):
        if(self.timerConfig["task_type"] == 'keyParagraph'):
            t = task_post_keyparagraph.Task_Post_Keyparagraph()
            t.env_config = self.timerConfig
            t.run(table_name='tb_key_paragraph')
        elif(self.timerConfig["task_type"] == 'relativeParagraph'):
            t_rela = task_post_relateparagraph.Task_Post_Relativeparagraph()
            t_rela.env_config = self.timerConfig
            t_rela.run(table_name='tb_relative_paragraph')
        elif(self.timerConfig["task_type"] == 'contentImgs'):
            task_post_contentimg.run(proj_absPath=self.timerConfig["proj_absPath"], origin=self.timerConfig["origin"], database=self.timerConfig['databaseName'], tableNameList=self.timerConfig['tableName'], maskFilt=self.timerConfig['maskFilt'])
        elif(self.timerConfig["task_type"] == 'thumbnailImgs'):
            task_post_thumbnail.run(proj_absPath=self.timerConfig["proj_absPath"], origin=self.timerConfig["origin"], database=self.timerConfig['databaseName'], tableNameList=self.timerConfig['tableName'])
        elif(self.timerConfig["task_type"]=='articleComment'):
            t_comment = task_post_comment.Task_Post_Comment()
            t_comment.env_config = self.timerConfig
            t_comment.run('t_comment')
        elif(self.timerConfig['task_type']=='articles'):
            t_articles = task_post_articles.Task_Post_Article()
            t_articles.env_config = self.timerConfig
            t_articles.run('tb_article')
        else:
            print('参数 task_type 出错')
