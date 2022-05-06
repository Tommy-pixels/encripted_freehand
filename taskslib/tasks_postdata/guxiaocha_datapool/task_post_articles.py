# coding=utf-8
from freehand.core.base.tasksmixin.tasks_postdata.base import Base_Task_Post
from freehand.core.utils.encription import get_encript_key_new
from freehand.contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_DEFAULT
from freehand.contrib.poster.default import poster_article
from freehand.middleware.cleaner.article_mid import ArticleMiddleware

"""20220402本类修正完毕 可正常使用"""

"""
    文章上传
    筛选条件：
        完整清洗过后的 文章内容 content 字数>500
        完整清洗过后的 标题 title 字数>10
    清洗条件：
"""


class Task_Post_Article(Base_Task_Post):
    def handle_article_lis(self, lis):
        res_lis = []
        cleaner_Article = ArticleMiddleware()
        for article in lis:
            title = article[2]
            content = article[3]
            if (title and content):
                title = cleaner_Article.clean_title(title=title)
                content = cleaner_Article.clean_content(content=content)
            else:
                continue
            if (title and content and len(title) >= 10 and len(content) > 550):
                res_lis.append((article[0], article[1], title, content, article[4], article[5], article[6], article[7], article[8]))
        return res_lis

    def run(self, table_name, classification, by_classification=True):
        """
            主要针对 段落、文章、评论 且保存在数据路里的这类数据（字符串类型）的处理和上传， 图片、视频等类型数据不适合本类方法
            注意：
                本类方法不做任何过滤操作和其它数据清洗操作，特殊操作根据不同task_type选择不同task 如 task_post_articles.py
        """
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

        # 2 去重
        dataList = self.del_repeatdata(task_type='articles', lis=dataList)

        # 3 清洗 根据不同 task_type 通用数据清洗操作 作为上传数据前的最后一步清洗
        dataList = self.handle_article_lis(lis=dataList)

        # 4 上传 处理后的列表
        if (dataList):
            posterInstance = poster_article.Poster_Article(interface=api_uri + '/article_get', userName=userName,password=password)
            posterInstance.key = get_encript_key_new('guxiaocha', '', '')
            res = posterInstance.post_auto_2(dataList, task_type='article')
            # 6 更新数据状态
            for i in res['success']:
                db.default_update_posted(table_name=table_name, record_id=i['id'], posted='1', datapool_id=datapool_id)
        return dataList

