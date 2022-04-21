#coding=utf-8
from freehand.core.base.poster.base import BasePoster
from freehand.core.utils import encription
from freehand.middleware.cleaner.article_mid import ArticleMiddleware
import json

class Poster_Article(BasePoster):
    def __init__(self, interface='http://121.40.187.51:9088/api/article_get', userName='', password=''):
        BasePoster.__init__(self, uri=interface, userName=userName,password=password)
        self.interface = interface

    # 原上传方法
    def post_auto(self, effectiveDataList, task_type):
        # self.key = encription.get_encript_key()
        posted_success_lis = []
        posted_failed_lis = []
        res = ''
        for item in effectiveDataList:
            if (task_type == 'article'):
                title_clean_lis = ['</em>', '<em>', '&', '-CSDN博客', '_CSDN博客', 'CSDN博客', 'CSDN博', 'CSDN', '.', '『', '』',
                                   '【', '】',
                                   '。', '#']
                title = item[1]
                for c_li in title_clean_lis:
                    title = title.replace(c_li, '')
                rep_lis = ['、', ',', '，', ';', '；', '-', '—', '|', '(', ')', '（', '）', ':']
                for r_li in rep_lis:
                    title = title.replace(r_li, ' ')
                content = item[2].replace('一.', '').replace('二.', '').replace('三.', '').replace('四.', '').replace('五.','').replace('六.','').replace('七.','')
                if (len(item[2]) > 500 and '；' not in title):
                    postableData = {
                        "key": self.key,
                        "account": self.userName,
                        "password": self.password,
                        'title': title,
                        'content': content
                    }
                    print(postableData)
                    res = self.poster(postableData=postableData, interface=self.interface)
            elif (task_type == 'question'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'question': str(item[0]),
                    'answer': json.dumps(item[1])
                }
                res = self.poster(postableData=postableData, interface=self.interface)
            if (res and res.json()['code'] == 1):
                # 上传成功的
                posted_success_lis.append(item)
            else:
                posted_failed_lis.append(item)
        self.log_post_res(effectiveDataList, lis_success=posted_success_lis, lis_failed=posted_failed_lis)  # 日志记录
        return res

