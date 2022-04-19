from db.backends.mysql.init_default_db import Init_DB

if __name__ == '__main__':
    """测试——生成数据库及对应的表"""
    db = Init_DB()
    db.run_default()