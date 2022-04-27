#coding=utf-8
from freehand.utils import globalTools
from freehand.middleware.filter.keyparagraph_mid import Filter_Keyparagraph
from freehand.contrib.poster.old_datapool import poster_paragraph as Poster
from freehand.core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from freehand.contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_Shujuchi


class Task_Post_Keyparagraph(Base_Task_Post):
    def run(self, table_name, classification):
        db = DB_Singleton_Shujuchi()
        db.cursor.execute("SELECT id, account,password,api_uri FROM `tb_datapool_info` WHERE `classification`='{}';".format(classification))
        db_res = db.cursor.fetchone()
        datapool_id = db_res[0]
        userName = db_res[1]
        password = db_res[2]
        api_uri = db_res[3]
        dataList = db.default_select_unposted_data(table_name=table_name, datapool_id=datapool_id)

        # 更新状态
        for i in dataList:
            db.default_update_posted(table_name=table_name, record_id=i[0], posted='2')

        # 2 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter_Keyparagraph()
        postableList = filterInstance.integratedOp(
            paragraphList=dataList
        )
        print("过滤操作完成， 接下来完成上传操作")
        # 4 上传列表
        if(postableList):
            posterInstance = Poster.Poster_Paragraph(interface=api_uri + '/key_paragraph_api', userName=userName, password=password)
            res = posterInstance.post_auto_2(postableList, task_type='keyParagraph')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1', datapool_id=datapool_id)

        print("上传操作完成， 接下来完成 postedurldatabase 数据库的更新操作")
        globalTools.finishTask()
        return postableList