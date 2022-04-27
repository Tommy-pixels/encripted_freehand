#coding=utf-8
from freehand.utils import globalTools
from freehand.utils.common import Controler_Time, Controler_Dir
from freehand.spider import selenium_douyin,selenium_sougou_weixin, selenium_kuaishou, selenium_douyin_stockA


class Sele_Spider_Runner:

    @classmethod
    def run_kuaishou(cls):
        # 视频的爬取上传
        kuaishou = selenium_kuaishou.Crawler_Kuaishou()
        kuaishou.run()
        globalTools.finishTask()
        del kuaishou

    @classmethod
    def run_sougou(cls):
        sougou = selenium_sougou_weixin.Crawler_Sougou()
        sougou.run()
        globalTools.finishTask()
        del sougou




