import os, sys
lib_path = os.path.abspath(os.path.join('../..'))
sys.path.append(lib_path)

from freehand.core.base.middleware.mid_filter.base import BaseFilter
from freehand.middleware.cleaner.paragraph_mid import ParagraphMiddleware

class Filter_Relativeparagraph(BaseFilter):
    # -> 关联段落的集成操作方法
    def integratedOp(self, paragraphList, keywordList):
        result = []
        cleanerInstance = ParagraphMiddleware()
        for item in paragraphList:
            # 1 进行清洗操作
            paragraph = cleanerInstance.process_operation(item[2])
            for keyword in keywordList:
                # 2 根据字符串长度125-250间进行筛选
                if (not self.filter_BetweenNumberOfWords(paragraph, whichKind='relativeParagraph')):
                    continue

                # 3 对每个段落进行关键词筛选 若有关键词则跳出当前循环
                if (self.checkIfHasKeyword_relativeParagraph(paragraph, keyword)):
                    # 4 根据筛选结果导入可上传的数据
                    result.append(
                        (
                            item[0],
                            item[1],
                            paragraph,  # 段落内容
                            keyword,  # 相关关键词
                            item[4],
                            item[5],
                            item[6],
                            item[7],
                        )
                    )
                    break
        return result