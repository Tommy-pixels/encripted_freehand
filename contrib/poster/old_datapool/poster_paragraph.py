import os, sys
lib_path = os.path.abspath(os.path.join('../../..'))
sys.path.append(lib_path)

from freehand.core.base.poster.base import BasePoster


class Poster_Paragraph(BasePoster):
    def __init__(self, interface='http://121.40.187.51:8088/api/article_get'):
        self.interface = interface