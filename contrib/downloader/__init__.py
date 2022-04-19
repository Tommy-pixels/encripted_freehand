"""
    下载器
"""
import os, sys
lib_path = os.path.abspath(os.path.join('../..'))
sys.path.append(lib_path)

from freehand.core.base.download.base import BaseDownloader

class Downloader(BaseDownloader):
    pass