#coding=utf-8
"""连接默认数据库 创建单例连接 调用的基类"""
from freehand.db.backends.mysql.base import BaseDatabase
import threading

class DB_Singleton_DEFAULT(BaseDatabase):
    _instance_lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if(not hasattr(DB_Singleton_DEFAULT, '_instance')):
            with DB_Singleton_DEFAULT._instance_lock:
                if (not hasattr(DB_Singleton_DEFAULT, '_instance')):
                    DB_Singleton_DEFAULT._instance = object.__new__(cls)
        return DB_Singleton_DEFAULT._instance

    def getAllDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print('getAllDataFromDB(sql)方法 出错： ', sql)
            return -1
        data = self.cursor.fetchall()
        # 将数据转换成列表
        result = []
        for item in data:
            result.append(
                [
                    item[i] for i in range(len(item))
                ]
            )
        return result


    def getOneDataFromDB(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            # 查找不到的话返回None
            return data
        except Exception as e:
            # 报错才返回-1
            print(e, 'sql: ', sql)
            return -1

    def insertData2DB(self, sql):
        try:
            self.cursor.execute(sql)
            return '数据插入成功'
        except Exception as e:
            print(e, 'sql: ', sql)
            return -1


