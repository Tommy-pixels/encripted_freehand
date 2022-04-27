#coding=utf-8
from freehand.core.base.poster.base import BasePoster
from freehand.middleware.filter.comment_mid import CommentMiddleware
from freehand.middleware.filter.comment_mid import Filter_Comment
import json


class Poster_Comment(BasePoster):
    def __init__(self, interface='http://121.40.187.51:8088/api/articlecomment_api', userName='', password=''):
        BasePoster.__init__(self, uri=interface, userName=userName,password=password)
        self.interface = interface
        self.filter_keyword = ['个股', '股市', 'A股', '港股', '新股', '炒股', '散户', '短线', '操盘', '波段', '股票','接口','通达信','证券','api','交易','同花顺']
        self.cleaner = CommentMiddleware()
        self.filter = Filter_Comment()


    def post_auto(self, effectiveDataList, task_type):
        posted_success_lis = []
        posted_failed_lis = []
        res = ''
        effectiveDataList = self.filter.integratedOp(effectiveDataList,self.filter_keyword)

        for item in effectiveDataList:
            if (task_type == 'keyParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1],
                    'rekeyword': '配资'
                }
                res = self.poster(postableData=postableData, interface=self.interface)
            elif (task_type == 'relativeParagraph'):
                postableData = {
                    "key": self.key,
                    "account": self.userName,
                    "password": self.password,
                    'content': item[0],
                    'keyword': item[1]
                }
                res = self.poster(postableData=postableData, interface=self.interface)
            elif (task_type == 'articleComment'):
                # comment = self.cleaner.process_operation(item[0])
                comment = item[0]
                if(comment and 'zhihu.com' not in comment and 'http' not in comment and len(comment) > 45 and len(comment) < 250):
                    postableData = {
                        "key": self.key,
                        "account": self.userName,
                        "password": self.password,
                        'comment': comment
                    }
                    res = self.poster(postableData=postableData, interface=self.interface)
                    # 更新数据库
                    # self.update_postedurldb(item)
            elif (task_type == 'article'):
                title_clean_lis = ['</em>', '<em>', '&', '-CSDN博客', '_CSDN博客', 'CSDN博客', 'CSDN博', 'CSDN', '.', '『', '』',
                                   '【', '】',
                                   '。', '#']
                title = item[1]
                for c_li in title_clean_lis:
                    title = title.replace(c_li, '')
                rep_lis = ['、', ',', '，', ';', '；', '-', '—', '|', '(', ')', '（', '）', ':']
                for r_li in rep_lis:
                    title = title.replace(r_li, ' ')
                content = item[2].replace('一.', '').replace('二.', '').replace('三.', '').replace('四.', '').replace('五.',
                                                                                                                  '').replace(
                    '六.', '').replace('七.', '')
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



