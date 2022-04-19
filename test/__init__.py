'''
    功能测试
'''
"""测试db"""
from contrib.db.db_singleton_connector import db_connector_shujuchi
from contrib.db.init_database import Init_DB

if __name__ == '__main__':
    # 1 测试单例数据库
    db0 = db_connector_shujuchi.DB_Singleton_Shujuchi()
    lis = db0.select_all_articles()
    print('测试是否可用 文章数量： ', len(lis))
    print('测试是否单例：')
    db1 = db_connector_shujuchi.DB_Singleton_Shujuchi()
    db2 = db_connector_shujuchi.DB_Singleton_Shujuchi()
    print('db0 id: ', id(db0))
    print('db1 id: ', id(db1))
    print('db2 id: ', id(db2))
    """本单例数据库测试通过"""

    # 2 测试连接其它数据库
    db0.check_ifsame_database('commentdatabase', True)
    print('是否是 commentdatabase， 期望输出True', db0.check_ifsame_database('commentdatabase', False))
    db1.check_ifsame_database('dbfreeh', False)
    print('是否是 dbfreeh， 期望输出True', db0.check_ifsame_database('commentdatabase', False))

