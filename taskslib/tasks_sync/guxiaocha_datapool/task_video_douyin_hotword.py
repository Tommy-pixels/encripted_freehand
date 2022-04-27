from freehand.spider.selenium import selenium_video_douyin
from freehand.utils.common import Controler_Time,Controler_Dir, Encode
from freehand.contrib.poster.guxiaocha.poster_video import Poster_Video
import os

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
            effective_lis = spider_douyin.handle_videolis(filted_video_lis, stock_code='', stock_name='', classification='guxiaocha', filter_curday=False)
        else:
            print('当前链接无符合条件的视频：', url)
    # spider_douyin.videolis_browser.close()
    # spider_douyin.video_browser.close()
    # globalTools.finishTask()


if __name__=='__main__':
    origin = 'douyin_guxiaocha'
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
        "crawlUrl_list": [
            "https://www.douyin.com/search/%23%E8%82%A1%E7%A5%A8?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E7%A5%A8?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E5%A4%A7%E7%9B%98?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E5%A4%A7%E7%9B%98?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%B4%A2%E7%BB%8F?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%B4%A2%E7%BB%8F?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E5%B8%82?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E5%B8%82?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E6%B8%AF%E8%82%A1?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E6%B8%AF%E8%82%A1?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E7%BE%8E%E8%82%A1?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E7%BE%8E%E8%82%A1?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23A%E8%82%A1?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23A%E8%82%A1?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E5%B8%82?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E5%B8%82?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E6%B0%91?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E8%82%A1%E6%B0%91?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E6%B8%B8%E8%B5%84?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E6%B8%B8%E8%B5%84?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E6%95%A3%E6%88%B7?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E6%95%A3%E6%88%B7?publish_time=1&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E9%87%91%E8%9E%8D?publish_time=7&sort_type=1&source=tab_search&type=video",
            "https://www.douyin.com/search/%23%E9%87%91%E8%9E%8D?publish_time=1&sort_type=1&source=tab_search&type=video"
        ],
        'databaseName': 'videodatabase',
        'tableName2Clear': 'tb_douyin_videoinfo'
    }
    run_douyin_guxiaocha(proj_absPath=proj_absPath,crawlUrl_list=config['crawlUrl_list'], origin=origin)
