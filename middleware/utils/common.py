import re
from freehand.contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_Shujuchi
d = DB_Singleton_Shujuchi()


class Regexp_Base:
    @staticmethod
    def regexp_clean_html_tap(h_tag:str='p', regexp_word_lis:list=[], s:str="")->str:
        """正则清洗字符串标签内容
        :param h_tag    html标签 默认为p标签
        :param s        待清洗的字符串
        :param regexp_word  正则待清洗的相关词
        例子：
        输入：
            regexp_word_lis = ['赞', '评论', '注明出处', '不得转载', '版权所有','扫二维码进','转载请','下方留言','欢迎留言','可以留言','可留言','下面留言','阅读原文','支持我们',
                '后台回复','可领取','点击下载','点个关注','群号','免费领取','交流群','回复“加群”','本文来自','一起交流','感谢','参考：','敬请关注','文/','进行留言',
                '感谢支持','声明：','领取','编辑|','阅读原文','QQ群','文|','整理|','原文地址'
                ]
            s = "<p>XXX</p><img /><p>XXX</p><img /><p>XX点关注：</p><p>QQ群：54516</p>"
        输出：
            s = "<p>XXX</p><img /><p>XXX</p><img />"
        """
        if(s):
            for regexp_word in regexp_word_lis:
                rep = re.compile(r'<{}>.*?</{}>'.format(h_tag))
                lis = rep.findall(s)
                for li in lis:
                    if(regexp_word in li):
                        s = s.replace(li, '')
            return s
        else:
            raise Exception('待处理的字符串为空')

class Regexp_Articles(Regexp_Base):
    def __init__(self):
        self.key_word_lis = ['赞', '评论', '注明出处', '不得转载', '版权所有', '扫二维码进', '转载请', '下方留言', '欢迎留言', '可以留言', '可留言', '下面留言', '阅读原文',
                    '支持我们','后台回复', '可领取', '点击下载', '点个关注', '群号', '免费领取', '交流群', '回复“加群”', '本文来自', '一起交流', '感谢', '参考：', '敬请关注',
                    '文/', '进行留言','感谢支持', '声明：', '领取', '编辑|', '阅读原文', 'QQ群', '文|', '整理|', '原文地址'
             ]

    """针对文章进行清洗并更新数据库"""
    def run(self):
        d.cursor.execute('SELECT id,title,content from tb_article;')
        res = d.cursor.fetchall()
        for it in res:
            content = it[2]
            if (not content):
                continue
            content = self.regexp_clean_html_tap(h_tag='p', regexp_word_lis=self.key_word_lis, s=content)
            sql_update = "UPDATE tb_article SET content=\"{}\" WHERE id=\'{}\';".format(content, it[0])
            d.cursor.execute(sql_update)
