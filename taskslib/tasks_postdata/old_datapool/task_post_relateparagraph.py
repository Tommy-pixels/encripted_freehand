'''
    自动化引擎
        从相关段落数据库中获取数据 进行 清洗 筛选 并上传 （已完成）
'''
import os, sys
lib_path = os.path.abspath(os.path.join('../../..'))
sys.path.append(lib_path)

from utils import globalTools
from middleware.filter.relativeparagraph_mid import Filter_Relativeparagraph
from contrib.poster.old_datapool import poster_paragraph as Poster
from core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_DEFAULT


class Task_Post_Relativeparagraph(Base_Task_Post):
    def __init__(self):
        Base_Task_Post.__init__()
        self.keyword_list = ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']

    def run(self, table_name):
        # 1 获取对应数据
        db = DB_Singleton_DEFAULT()
        dataList = db.default_select_unposted_data(table_name=table_name)

        # 2 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter_Relativeparagraph()
        postableList = filterInstance.integratedOp(paragraphList=dataList, keywordList=self.keyword_list)

        # 3 上传列表
        if(postableList):
            posterInstance = Poster.Poster_Paragraph(interface='http://121.40.187.51:8088/api/relation_paragraph_api')
            res = posterInstance.post_auto_2(postableList, task_type='relativeParagraph')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1')

        globalTools.finishTask()
        return res