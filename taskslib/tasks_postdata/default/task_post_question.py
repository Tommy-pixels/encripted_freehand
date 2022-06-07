# coding=utf-8
from freehand.core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from freehand.core.utils.encription import get_encript_key_new
from freehand.contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_DEFAULT
from freehand.contrib.poster.guxiaocha import poster_question

class Task_Post_Question(Base_Task_Post):
    def run(self, table_name, classification, by_classification=True):
        # 1 获取数据
        db = DB_Singleton_DEFAULT()
        db.cursor.execute("SELECT id, account,password,api_uri FROM `tb_datapool_info` WHERE `classification`='{}';".format(classification))
        db_res = db.cursor.fetchone()
        datapool_id = db_res[0]
        userName = db_res[1]
        password = db_res[2]
        api_uri = db_res[3]
        dataList = db.default_select_unposted_data(table_name=table_name, datapool_id=datapool_id, by_classification=by_classification)

        # 更新状态
        for i in dataList:
            db.default_update_posted(table_name=table_name, record_id=i[0], posted='2')

        # 4 上传 处理后的列表
        if(dataList):
            posterInstance = poster_question.Poster_Question(interface=api_uri + '/question_answer')
            posterInstance.key = get_encript_key_new('guxiaocha', '', '')
            res = posterInstance.post_auto_2(dataList, task_type='question')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1', datapool_id=datapool_id)
            for i in res['failed']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='2', datapool_id=datapool_id)
        else:
            print('无有效数据')
        return dataList

