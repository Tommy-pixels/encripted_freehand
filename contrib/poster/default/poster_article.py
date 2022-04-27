#coding=utf-8
from freehand.core.base.poster.base import BasePoster
from freehand.core.utils import encription
from freehand.middleware.cleaner.article_mid import ArticleMiddleware
import json

class Poster_Article(BasePoster):
    def __init__(self, interface='http://121.40.187.51:9088/api/article_get', userName='', password=''):
        BasePoster.__init__(self, uri=interface, userName=userName,password=password)
        self.interface = interface
