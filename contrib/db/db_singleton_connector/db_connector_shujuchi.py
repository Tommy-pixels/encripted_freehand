import os, sys
lib_path = os.path.abspath(os.path.join('../../..'))
sys.path.append(lib_path)

from .db_connector_default import DB_Singleton_DEFAULT
from freehand.static import default_variable_map

class DB_Singleton_Shujuchi(DB_Singleton_DEFAULT):
    def insert_key_paragraph(self, ori_uri, tag_origin, paragraph, publish_time, crawl_time, site, classfication):
        sql_insert = default_variable_map.SQL_INSERT_KEYPARAGRAPH.format(
            ori_uri, tag_origin, paragraph, publish_time, crawl_time, site, classfication
        )
        res = self.default_execute_sql(execute_type='insert', sql=sql_insert)
        return res

    def insert_relative_paragraph(self, ori_uri, paragraph, publish_time, crawl_time, site, classfication):
        sql_insert = default_variable_map.SQL_INSERT_RELATIVEPARAGRAPH.format(
            ori_uri, paragraph, publish_time, crawl_time, site, classfication
        )
        res = self.default_execute_sql(execute_type='insert', sql=sql_insert)
        return res

    def insert_comment(self, ori_uri, comment, publish_time, crawl_time, site, classfication):
        sql_insert = default_variable_map.SQL_INSERT_COMMENT.format(
            ori_uri, comment, publish_time, crawl_time, site, classfication
        )
        res = self.default_execute_sql(execute_type='insert', sql=sql_insert)
        return res

    def insert_article(self, ori_uri, title, content, publish_time, crawl_time, site, classfication):
        sql_insert = default_variable_map.SQL_INSERT_ARTICLE.format(
            ori_uri, title, content, publish_time, crawl_time, site, classfication
        )
        res = self.default_execute_sql(execute_type='insert', sql=sql_insert)
        return res

    def insert_img(self, img_type, ori_uri, reco, crawl_time, local_path, site, classfication):
        sql_insert = default_variable_map.SQL_INSERT_IMG.format(
            img_type, ori_uri, reco, crawl_time, local_path, site, classfication
        )
        res = self.default_execute_sql(execute_type='insert', sql=sql_insert)
        return res

    def insert_video(self, ori_uri, title, publish_time, crawl_time, local_path, site, classfication):
        sql_insert = default_variable_map.SQL_INSERT_VIDEO.format(
            ori_uri, title, publish_time, crawl_time, local_path, site, classfication
        )
        res = self.default_execute_sql(execute_type='insert', sql=sql_insert)
        return res

    def select_all_data(self, table_name):
        d_lis = self.getAllDataFromDB('SELECT * FROM `{}`;'.format(table_name))
        return d_lis

