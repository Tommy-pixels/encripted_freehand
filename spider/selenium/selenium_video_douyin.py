#coding=utf-8
import random
import time
from time import sleep
from freehand.contrib.poster.guxiaocha.poster_video import Poster_Video as VideoPoster
from freehand.middleware.filter.video_mid import DouyinFilter
from freehand.utils import tools
from freehand.contrib.db.db_notsingleton_connector.db_connector_default import DB_NotSingleton_DEFAULT
from freehand.core.base.selenium.base import BaseSelenium
from freehand.core.base.cracker import cracker_douyin
from freehand.contrib.downloader import Downloader
from ..universal.special_methods_douyin import Douyin_SpecialMethod

# --------------------------- 爬取抖音视频的类 ----------------------------------
"""
    要求： 爬取抖音上所有a股股票得视频。按照最多点赞，一周内得爬取。
        a股股票定时更新数据库。
        然后按照 股票代码和股票名字 合起来 搜索  :  688019安集科技
    过滤视频列表
        筛选条件：
            判断视频时长 1~6min
            必须包含 #财经 这个标签 没有得 都过滤
    上传视频
"""
class Crawler_Douyin(
    BaseSelenium,
    Douyin_SpecialMethod
):
    def __init__(self, captchaPath, videoDirPath, coverSavedPath, interface='https://121.196.238.250/api/video_upload', userName='', password='', chromeDriverPath=r'E:\Projects\webDriver\\chrome\\chromedriver.exe'):
        self.chromeDriverPath = chromeDriverPath
        self.videoDirPath = videoDirPath
        self.coverSavedPath = coverSavedPath
        self.interface = interface
        self.userName = userName
        self.password = password
        self.captchaPath = captchaPath  # 滑块验证参数
        self.init_default_instance()
        self.videolis_browser.get('https://www.douyin.com')
        self.video_browser.get('https://www.douyin.com')
        sleep(4)
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser)  # 滑块验证
        # self.roll_tobottom_method1(browser=self.videolis_browser, times=350)

    def init_default_instance(self):
        self.dbOperator = DB_NotSingleton_DEFAULT()
        self.cracker = cracker_douyin.DouyinCrack(captchaDstDirPath=self.captchaPath)
        self.filter = DouyinFilter(dirOriPath=self.videoDirPath)
        # self.poster = VideoPoster(videoDirPath=self.videoDirPath, coverSavedPath=self.coverSavedPath, interface=self.interface, userName=self.userName, password=self.password)
        # 为了可移植，poster需要在类外部定义传入
        self.videolis_browser = self.init_webdriver(self.chromeDriverPath)
        self.video_browser = self.init_webdriver(self.chromeDriverPath)

    # 首次进入 move2BottomTimes 为向下滑动的次数 默认350
    def get_videolis(self, sliderTimes, url_index):
        """
        获取符合条件 时间长度在 1-6min 之间的视频信息（title,url, publishtime）
        :param sliderTimes 向下滑动的距离
        :parma url_index 待爬取链接
        """
        self.videolis_browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defneProperty(navigator, "webdriver", {get: () => undefined})'
        })
        self.videolis_browser.get(url_index)
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证

        # 2.通过浏览器向服务器发送URL请求
        self.videolis_browser.get(url_index)
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证

        # 等待某个元素是否出现
        # WebDriverWait(self.videolis_browser, 10).until(
        #     # EC.text_to_be_present_in_element((By.XPATH, ''))
        #     EC.presence_of_element_located((By.XPATH, "//ul[@class='_3636d166d0756b63d5645bcd4b9bcac4-scss']"))
        # )
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        liEffectiveList = []  # 可上传的视频信息列表
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        # 向下滚动
        self.roll_tobottom_method1(browser=self.videolis_browser, times=sliderTimes)
        try:
            # 1. 获取视频信息列表
            ul = self.videolis_browser.find_element_by_xpath("//ul[@class='qrvPn3bC H2eeMN3S']")
            liList = ul.find_elements_by_xpath("./li")
            for li in liList:
                try:
                    a = li.find_element_by_xpath(".//a[@class='B3AsdZT9 yf0WMGW6 OuiStkZo']")
                except Exception as e:
                    continue
                title = a.text
                videoPageUrl = a.get_attribute("href")
                timeLength = li.find_element_by_xpath(".//span[@class='uK7yEPTZ']").text
                publishTime = li.find_element_by_xpath(".//span[@class='uPLxyScW yJE4WUkV']").text
                like_num = li.find_element_by_xpath('.//span[@class="VjkQxGgO"]').text
                if (self.check_timelength_between(timeLength)):
                    liEffectiveList.append((title, videoPageUrl, publishTime, timeLength, like_num))
                else:
                    continue
        except Exception as e:
            print('获取不到视频信息列表')
        return liEffectiveList

    def handle_single_video(self, video, filter_curday=False):
        # 2.通过浏览器向服务器发送URL请求
        self.video_browser.get(video[1])
        # 滑块验证
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证
        self.video_browser.get(video[1])
        sleep(3)
        self.handleSlideCheck(self.cracker, self.videolis_browser, self.videolis_browser) # 滑块验证

        # 获取发布时间，判断发布时间是否是当天，是的话才进行下一步操作，不是的话跳出循环进入下一个循环
        try:
            pubTime = self.video_browser.find_element_by_xpath("//span[@class='_87bab22a14dd86d6a0038ee4b3fdaea4-scss']").text.split("：")[1].split(' ')[0]
        except Exception as e:
            try:
                pubTime = self.video_browser.find_element_by_xpath("//span[@class='aQoncqRg']").text.split("：")[1].split(' ')[0]
            except Exception as e:
                print('获取不到视频页发布日期')
                return None
        timelength = self.video_browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-controls/xg-inner-controls/xg-left-grid/xg-icon[2]/span[3]').text

        if(video[0].replace(' ','')==''):
            # 无标题
            return None

        if(filter_curday):
            # 验证当天
            if(not self.check_is_curday(pubTime=pubTime)):
                return None

        # 视频有效，获取准确的可下载的视频链接
        time.sleep(2)
        videoUrl = self.video_browser.find_elements_by_xpath("//video//source")
        if (videoUrl):
            videoUrl = videoUrl[0].get_attribute("src")
        else:
            # 针对douyin 通过blob方式传输视频的处理
            print('当前链接的视频通过blob传输')
            self.temp_driver = self.init_webdriver(self.chromeDriverPath, True)
            self.temp_driver.get(video[1])
            time.sleep(2)
            try:
                videoUrl = self.temp_driver.find_elements_by_xpath("//video")[0].get_attribute("src")
                self.temp_driver.close()
            except Exception as e:
                print('无法获取到视频源链接(用于下载)： ', video[0], ' ', video[1])
                return None
        return (video[0], video[1], video[2], videoUrl)

    def handle_videolis(self, video_lis, classification, filter_curday, **kwargs):
        stock_code = kwargs.get('stock_code')
        stock_name = kwargs.get('stock_name')
        # 1. 过滤掉上传过的视频 去重
        if (video_lis):
            video_lis = self.filter.filter_posted(video_lis)  # 过滤掉上传过的视频
            video_lis = tools.cleanRepeated(video_lis)  # 去重
        else:
            print('经过去重操作，待处理视频列表为空')
            return None

        # 2. 处理单个视频 - 下载和上传
        effective_lis = []
        for video in video_lis:
            res = self.handle_single_video(video, filter_curday=filter_curday)
            if(res):
                # 视频有效 可下载上传
                i = random.randint(1, 100)
                print('下载视频: ', res[0], ' ', res[3])
                Downloader.download_video(urlpath=res[3], name=str(i), dstDirPath=self.videoDirPath)
                print('上传视频: ', res[0], ' ', str(i) + '.mp4')
                if(res[0].split('#')[0]!=''):
                    title = res[0].split('#')[0] + " #财经"
                else:
                    title = res[0].split('#')[1] + " #财经"

                post_res = self.poster.post_videoSingle(str(i) + '.mp4', title=title, **kwargs)
                print('上传结果：', post_res.text if (post_res) else post_res)
                effective_lis.append(res)
                # 更新视频数据表
                sql = "INSERT INTO `tb_video` (`ori_uri`, `title`, `local_path`, `site`, classification) VALUES ('{}', '{}', '{}', '{}', '{}');".format(
                    res[3], video[0], self.poster.videoDirPath.replace('\\','\\\\')+str(i)+'.mp4','douyin', classification
                )
                self.dbOperator.insertData2DB(sql=sql)
        return effective_lis


