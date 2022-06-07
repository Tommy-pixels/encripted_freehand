#coding=utf-8
import os
import time
import requests
import hashlib
from core.base.poster.base import BasePoster
from core.utils import encription
import json

class Poster_Question(BasePoster):
    def __init__(self, interface='', userName='', password=''):
        BasePoster.__init__(self, uri=interface, userName=userName,password=password)
        self.interface = interface
        self.key = hashlib.md5(('guxiaocha' + self.curDate).encode('utf-8')).hexdigest()
