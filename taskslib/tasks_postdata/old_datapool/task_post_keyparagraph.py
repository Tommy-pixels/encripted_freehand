import os, sys
lib_path = os.path.abspath(os.path.join('../../..'))
sys.path.append(lib_path)

from utils import globalTools
from middleware.filter.keyparagraph_mid import Filter_Keyparagraph
from contrib.poster.old_datapool import poster_paragraph as Poster
from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_Shujuchi


class Task_Post_Keyparagraph(Base_Task_Post):
    def run(self, table_name):
        db = DB_Singleton_Shujuchi()
        dataList = db.default_select_unposted_data(table_name=table_name)

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
            posterInstance = Poster.Poster_Paragraph(interface='http://121.40.187.51:8088/api/key_paragraph_api')
            res = posterInstance.post_auto_2(postableList, task_type='keyParagraph')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1')

        print("上传操作完成， 接下来完成 postedurldatabase 数据库的更新操作")
        globalTools.finishTask()
        return postableList