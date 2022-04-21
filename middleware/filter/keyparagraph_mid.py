#coding=utf-8
from core.base.middleware.mid_filter.base import BaseFilter
from middleware.cleaner.paragraph_mid import ParagraphMiddleware
from contrib.db.db_singleton_connector.db_connector_shujuchi import DB_Singleton_Shujuchi

class Filter_Keyparagraph(BaseFilter):
    def __init__(self):
        db = DB_Singleton_Shujuchi()
        self.stocksNameCodeList = db.select_all_data('tb_stocks')
        del db

    def integratedOp(self, paragraphList):
        result = []
        cleanerInstance = ParagraphMiddleware()
        for item in paragraphList:
            paragraph = item[2]
            keyword = item[3]
            # 筛选有标签的
            if (self.filter_hasTag_keyParagraph(paragraph, keyword)):
                # 进行清洗操作
                paragraph = cleanerInstance.process_operation(paragraph)
                # 筛选判断 ：
                #   1 字符串长度不在125-250之间；
                #   2 段落含有股票名或代码
                #   3 段落包含日期关键词
                ##  但凡满足上面任何一个的段落筛选条件的段落都过滤掉
                check = (not self.filter_BetweenNumberOfWords(paragraph, whichKind='keyParagraph')) or self.filter_hasStockCode(paragraph, self.stocksNameCodeList) or self.filter_dateRef(paragraph, self.dateRefList)
                if (check):
                    # 进入该判断条件说明对应段落无效跳过， 因此希望有效段落的check最终为false
                    continue
                result.append(
                    (
                        item[0],
                        item[1],
                        paragraph,  # 段落内容
                        keyword,
                        item[4],
                        item[5],
                        item[6],
                        item[7],
                    )
                )
            else:
                continue
        return result