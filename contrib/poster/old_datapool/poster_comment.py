#coding=utf-8
from core.base.poster.base import BasePoster

class Poster_Comment(BasePoster):
    def __init__(self, interface, userName, password):
        BasePoster.__init__(self, uri=interface, userName=userName,password=password)
        self.interface = interface

    def update_postedurldb(self, item):
        sql = "INSERT INTO `postedurldatabase`.`tb_comment_posted` (`comment`) VALUES (\'{}\');".format(item[0].strip())
        return self.dbOperator.insertData2DB(sql)

