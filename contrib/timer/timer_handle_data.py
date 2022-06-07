# coding=utf-8
from freehand.core.timer.base import Base_Timer
from freehand.core.utils.module_loading import import_string, import_module

class TaskTimer_AutoDealwithPost(Base_Timer):
    def task(self):
        datapool = self.timerConfig["datapool"]
        dotted_path = 'freehand.taskslib.tasks_postdata.' + datapool
        if (self.timerConfig["task_type"] == 'keyParagraph'):
            key_p = import_string(dotted_path + '.task_post_keyparagraph')
            t = key_p.Task_Post_Keyparagraph()
            t.env_config = self.timerConfig
            t.run(table_name='tb_key_paragraph', classification=datapool)
        elif (self.timerConfig["task_type"] == 'relativeParagraph'):
            rela_p = import_string(dotted_path + '.task_post_relateparagraph')
            t_rela = rela_p.Task_Post_Relativeparagraph()
            t_rela.env_config = self.timerConfig
            t_rela.run(table_name='tb_relative_paragraph', classification=datapool)
        elif (self.timerConfig["task_type"] == 'contentImgs'):
            contentimg_p = import_string(dotted_path + '.task_post_contentimg')
            contentimg_p.run(proj_absPath=self.timerConfig["proj_absPath"], origin=self.timerConfig["origin"],database=self.timerConfig['databaseName'],
                                     tableNameList=self.timerConfig['tableName'], maskFilt=self.timerConfig['maskFilt'])
        elif (self.timerConfig["task_type"] == 'thumbnailImgs'):
            thumbnail_p = import_string(dotted_path + '.task_post_thumbnail')
            thumbnail_p.run(proj_absPath=self.timerConfig["proj_absPath"], origin=self.timerConfig["origin"],database=self.timerConfig['databaseName'],
                                    tableNameList=self.timerConfig['tableName'])
        elif (self.timerConfig["task_type"] == 'articleComment'):
            commotn_p = import_string(dotted_path + '.task_post_comment')
            t_comment = commotn_p.Task_Post_Comment()
            t_comment.env_config = self.timerConfig
            t_comment.run(table_name='tb_comment', classification=datapool)
        elif (self.timerConfig['task_type'] == 'articles'):
            article_p = import_string(dotted_path + '.task_post_articles')
            t_articles = article_p.Task_Post_Article()
            t_articles.env_config = self.timerConfig
            t_articles.run(table_name='tb_article', classification=datapool)
        elif(self.timerConfig['task_type'] == 'questions'):
            question_p = import_module(dotted_path + '.task_post_question')
            t_articles = question_p.Task_Post_Question()
            t_articles.env_config = self.timerConfig
            t_articles.run(table_name='tb_question', classification=datapool)
        else:
            print('参数 task_type 出错')

