#coding=utf-8
from core.base.poster.base import BasePoster
from middleware.filter.comment_mid import CommentMiddleware
from middleware.filter.comment_mid import Filter_Comment


class Poster_Comment(BasePoster):
    def __init__(self, interface='http://121.40.187.51:8088/api/articlecomment_api', userName='', password=''):
        BasePoster.__init__(self, uri=interface, userName=userName,password=password)
        self.interface = interface
        self.filter_keyword = ['个股', '股市', 'A股', '港股', '新股', '炒股', '散户', '短线', '操盘', '波段', '股票','接口','通达信','证券','api','交易','同花顺']
        self.cleaner = CommentMiddleware()
        self.filter = Filter_Comment()


