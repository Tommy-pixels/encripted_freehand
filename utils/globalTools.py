#coding=utf-8
import os, time, re, requests
import hashlib, base64
from selenium import webdriver


def finishTask():
    print("流程结束，单次任务结束（爬取、处理、上传数据， 对应数据库数据的清空以及posturldatabase数据库的更新）")


# 通过selenium获取指定信息的类
class GetParams_Selenium:
    def __init__(self, *driverPath):
        if(driverPath!=()):
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_experimental_option('useAutomationExtension', False)
            self.browser = webdriver.Chrome(driverPath, options=option)


    def getCookies(self, *url, browser):
        '''
        类方法，以对象形式输出指定链接返回的cookies
        :param url: 待打开的链接
        :param browser: 浏览器引擎
        :return: cookies对象
        '''
        # 获取cookie
        dictCookies = browser.get_cookies()
        cookies = {}
        for item in dictCookies:
            key = item['name']
            cookies[str(key)] = str(item['value'])
        return cookies

    def del_all_cookies(self):
        self.browser.delete_all_cookies()

    def get_params(self, url, *browser):
        if(browser==()):
            self.browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, self.browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }
        else:
            browser.get(url)
            time.sleep(1)
            cookies = self.getCookies(url, browser)
            headers = {}
            return {
                'cookies': cookies,
                'headers': headers
            }


    def closeBrowser(self, *browser):
        '''
        关闭指定浏览器，若浏览器为None则关闭对象浏览器
        :param browser:
        :return: None
        '''
        if(browser==()):
            self.browser.close()
        else:
            browser.close()




class Handle_PackageInfo:
    '''
        处理报文信息 如 cookie和headers字符串和对象的转换
    '''
    def translate_Cookies_Row2Obj(self, cookiesRow):
        cookieList = cookiesRow.split(";")
        self.cookies = {}
        for cookieItem in cookieList:
            i = cookieItem.strip().split("=")
            k = i[0]
            v = i[1]
            self.cookies[k] = v
        return self.cookies

    def translate_Headers_Row2Obj(self, headersRow):
        headerList = headersRow.split('\n')
        self.headers = {}
        for headerItem in headerList:
            i = headerItem.strip().split(":")
            if (i != ['']):
                k = i[0]
                v = i[1]
                self.headers[k] = v
        return self.headers
