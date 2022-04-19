from conf import setting
from contrib.db.db_singleton_connector.db_connector_default import DB_Singleton_DEFAULT

"""
    数据库操作测试成功
"""
if __name__ == '__main__':
    print(setting.DATABASES)
    db_instance = DB_Singleton_DEFAULT()
    db_instance.check_ifsame_database('data_usable_database')
    lis = db_instance.getAllDataFromDB('select * from `filter_video_keyword`;')
    print(lis)