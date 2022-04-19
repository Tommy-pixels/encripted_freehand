import os, sys
lib_path = os.path.abspath(os.path.join('../../..'))
sys.path.append(lib_path)

from utils import globalTools
from contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_DEFAULT
from middleware.filter.comment_mid import Filter_Comment
from contrib.poster.new_datapool.poster_comment import Poster_Comment
from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post

class Task_Post_Comment(Base_Task_Post):
    def __init__(self):
        Base_Task_Post.__init__(self)
        self.keyword_list = ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']

    def run(self, table_name):
        # 1 获取 对应数据
        db = DB_Singleton_DEFAULT()
        dataList = db.default_select_unposted_data(table_name)

        # 更新状态
        for i in dataList:
            db.default_update_posted(table_name=table_name, record_id=i[0], posted='2')

        # 2 去重
        dataList = self.del_repeatdata(task_type='articleComment', lis=dataList)

        # 4 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter_Comment()
        postableList = filterInstance.integratedOp(commentList=dataList, keywordList=self.keyword_list)

        # 5 上传列表
        if (postableList):
            posterInstance = Poster_Comment(interface='http://121.40.187.51:9088/api/articlecomment_api')
            # posterInstance.post_auto(postableList, task_type='articleComment')
            res = posterInstance.post_auto_2(postableList, task_type='articleComment')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1')

    globalTools.finishTask()