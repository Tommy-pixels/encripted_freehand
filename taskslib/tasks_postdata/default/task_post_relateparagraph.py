#coding=utf-8
'''
    自动化引擎
        从相关段落数据库中获取数据 进行 清洗 筛选 并上传 （已完成）
'''
from freehand.utils import globalTools
from freehand.middleware.filter.relativeparagraph_mid import Filter_Relativeparagraph
from freehand.contrib.poster.old_datapool import poster_paragraph as Poster
from freehand.core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from freehand.contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_DEFAULT


class Task_Post_Relativeparagraph(Base_Task_Post):
    def __init__(self):
        Base_Task_Post.__init__(self)
        self.keyword_list = ['个股', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段']

    def run(self, table_name, classification, **kwargs):
        # 1 获取对应数据
        db = DB_Singleton_DEFAULT()
        db.cursor.execute("SELECT id, account,password,api_uri FROM `tb_datapool_info` WHERE `classification`='{}';".format(classification))
        db_res = db.cursor.fetchone()
        datapool_id = db_res[0]
        userName = db_res[1]
        password = db_res[2]
        api_uri = db_res[3]
        dataList = db.default_select_unposted_data(table_name=table_name, datapool_id = datapool_id)

        # 2 过滤操作 输入的列表为从数据库中获取的列表（过滤操作包含清洗操作，不用单独进行清洗）
        filterInstance = Filter_Relativeparagraph()
        postableList = filterInstance.integratedOp(paragraphList=dataList, keywordList=self.keyword_list)
        # 3 上传列表
        if(postableList):
            posterInstance = Poster.Poster_Paragraph(interface=api_uri+'/relation_paragraph_api', userName=userName, password=password)
            res = posterInstance.post_auto_2(postableList, task_type='relativeParagraph')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1', datapool_id=datapool_id)

        globalTools.finishTask()
        return res
