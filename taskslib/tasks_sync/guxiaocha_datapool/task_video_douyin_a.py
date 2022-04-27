from freehand.spider.selenium import selenium_video_douyin
from freehand.utils.common import Controler_Time,Controler_Dir, Encode
from freehand.contrib.poster.guxiaocha.poster_video import Poster_Video
from freehand.contrib.db.db_notsingleton_connector.db_connector_default import DB_NotSingleton_DEFAULT
import os

def get_url():
    sql_get = 'SELECT `name`, `code` FROM `tb_namecode`;'
    contraler_db = DB_NotSingleton_DEFAULT()
    contraler_db.check_ifsame_database(database='data_usable_database')
    stocks_lis = contraler_db.getAllDataFromDB(sql_get)
    stocks_lis = stocks_lis[50:]
    url_lis = []
    for item in stocks_lis:
        name = Encode.str2urlcode(item[0])
        code = item[1]
        url = 'https://www.douyin.com/search/' + code + name + '?publish_time=7&sort_type=1&source=tab_search&type=video'
        url_lis.append(url)
    contraler_db.cursor.close()
    contraler_db.conn.close()
    del contraler_db
    return url_lis

# Selenium 爬取 爬取视频源 抖音
def run_douyin_guxiaocha(proj_absPath, crawlUrl_list, origin):
    updateTime = Controler_Time.getCurDate("%Y%m%d")
    videoDirPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + origin + '\\'
    coverSavedPath = proj_absPath + '\\assets\\videos\\' + updateTime + '\\' + origin + '\\cover_douyin.jpg'
    captchaPath = proj_absPath + '\\assets\\captcha\\' + updateTime + '\\' + origin + '\\'
    # 判断配置里的目录是否存在，不存在则创建对应目录
    Controler_Dir.checkACreateDir(videoDirPath)
    Controler_Dir.checkACreateDir(captchaPath)

    # 抖音视频的爬取及上传
    spider_douyin = selenium_video_douyin.Crawler_Douyin(
        captchaPath=captchaPath,
        videoDirPath=videoDirPath,
        coverSavedPath=coverSavedPath,
        interface='https://121.196.238.250/api/video_upload',
        userName='',
        password='',
        chromeDriverPath=r'E:\Projects\webDriver\\chrome\\chromedriver.exe'
    )
    spider_douyin.poster = Poster_Video(
        videoDirPath=spider_douyin.videoDirPath,
        coverSavedPath=spider_douyin.coverSavedPath,
        interface=spider_douyin.interface,
        userName=spider_douyin.userName,
        password=spider_douyin.password
    )
    for url in crawlUrl_list:
        stock_code = url.split('search/')[-1].split('?')[0][0:6]
        stock_name = Encode.urlcode2str(url.split('search/')[-1].split('?')[0][6:])
        unfilted_video_lis = spider_douyin.get_videolis(sliderTimes=1, url_index=url)
        if (unfilted_video_lis):
            filted_video_lis = spider_douyin.filter.filter_by_hotnum(unfilted_video_lis)
            effective_lis = spider_douyin.handle_videolis(filted_video_lis, stock_code=stock_code, stock_name=stock_name, classification='guxiaocha', filter_curday=False)
        else:
            print('当前链接无符合条件的视频：', url)
    # spider_douyin.videolis_browser.close()
    # spider_douyin.video_browser.close()
    # globalTools.finishTask()


if __name__=='__main__':
    origin = 'douyin_guxiaocha_hot500'
    proj_absPath = os.path.abspath(os.path.dirname(__file__))
    config = {
        "beginTime": '00:01:59',  # 注意表示 一位数字的要0开头
        "endTime": '23:51:01',
        "taskExcuteDelta": 3600,  # 任务间隔1h
        "timeExcuteDelta": 43200 * 100,  # 定时器间隔 每个一天运行一次
        "whichKind": 'video',
        "tasktype": 'selenium',
        'origin': 'douyin_guxiaocha',
        "crawlMethod": 'Selenium',
        "proj_absPath": proj_absPath,  # 当前环境路径
        "crawlUrl_list": [],
        'databaseName': 'videodatabase',
        'tableName2Clear': 'tb_douyin_videoinfo'
    }
    run_douyin_guxiaocha(proj_absPath=proj_absPath,crawlUrl_list=get_url(), origin=origin)
