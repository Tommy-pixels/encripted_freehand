#coding=utf-8
from freehand.core.base.poster.base import BasePoster


class Poster_Paragraph(BasePoster):
    def __init__(self, interface='http://121.40.187.51:8088/api/article_get', userName='', password=''):
        BasePoster.__init__(self,uri=interface, userName=userName,password=password)
        self.interface = interface