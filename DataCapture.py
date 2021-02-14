import datetime
import os
import time

import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class Capture(object):
    '''爬虫类，抓取豆瓣指定网站一整页的文章列表'''
    '''后面爬的时候要注意自己chrome的版本和chromeDriver的版本'''
    '''todo 第一次爬全部，后面每年只爬增量数据(from 2021) 程序留给 2022 年再修改 ( by vivi at 2021/2/14'''

    def __init__(self, url):
        self.Url = url

    def Login(self, username: str, password: str) -> WebDriver:
        browser_obj = webdriver.Chrome()
        browser_obj.maximize_window()
        browser_obj.get(self.Url)

        loginTab = browser_obj.find_element_by_class_name(
            'account-tab-account')  # 切换到密码登录模式
        loginTab.click()

        userNameInput = browser_obj.find_element_by_id('username')  # 获取用户名输入框
        userNameInput.send_keys(username)
        userPwdInput = browser_obj.find_element_by_id('password')  # 获取密码输入框
        userPwdInput.send_keys(password)
        loginButton = browser_obj.find_element_by_class_name(
            'btn-account')  # 登录按钮
        loginButton.click()

        # 此处可能浏览器会卡住，因为尝试次数太多需要手动验证（拖拼图）需要打点等待
        time.sleep(5)  # 等待登录
        return browser_obj

    def RequestAndSave(self, browser_obj: WebDriver):
        try:
            cookies = browser_obj.get_cookies()
            cookie_dict = {}
            for i in cookies:
                cookie_dict[i['name']] = i['value']
            UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
            headers = {'User-Agent': UserAgent}

            reqHtml = requests.get(
                self.Url, headers=headers, cookies=cookie_dict)
            reqText = reqHtml.text
            analyseHtml = html.etree.HTML(reqText)
            noteContainers = analyseHtml.xpath(
                '//div[@class="note-container"]')  # 目录
            dataUrls = []  # dataurls 就是所有日志的URL
            for item in noteContainers:
                dataUrls.append(item.attrib['data-url'])

            # 处理页数，从不同分页中获取目标数据
            pageSpan = analyseHtml.xpath(
                '//span[@class="thispage"]/@data-total-page')
            totalPage = int(pageSpan[0])
            currentPage = 1  # 因为第一页在上面已经访问完了，所以不用继续访问，直接从第二页开始
            while currentPage <= totalPage:
                currentPage = currentPage + 1
                urlStartNo = (currentPage - 1) * 10
                pageUrl = '?start=' + str(urlStartNo) + '&type=note'
                urlList = self.GetPageAllUrl(
                    self.Url + pageUrl, headers, cookie_dict)
                dataUrls.extend(urlList)

            for item in dataUrls:
                requestResult = requests.get(
                    item, headers=headers, cookies=cookie_dict)
                resultText = requestResult.text
                resultHtml = html.etree.HTML(resultText)
                fileDateList = resultHtml.xpath(
                    '//span[@class="pub-date"]/text()')  # 日志的日期所在的span
                fileDateStr = fileDateList[0]
                fileDate = datetime.datetime.strptime(
                    fileDateStr, '%Y-%m-%d %H:%M:%S')  # 转换成日期格式，待传入保存方法中
                titleList = resultHtml.xpath(
                    '//div[@class="note-header note-header-container"]/h1/text()')  # 标题所在的DIV
                title = titleList[0]
                if not self.IsExistsTargetFile(str(fileDate.year), title):
                    notes = resultHtml.xpath(
                        '//div[@class="note"]/p/text()')  # 内容列表
                    fullNotes = ""
                    fullNotes = fullNotes.join(notes)  # 将日志内容拼接为一个文档
                    self.SaveResponseFile(str(fileDate.year), title, fullNotes)
        except Exception as e:
            print(e.args)

    def GetPageAllUrl(self, url: str, headers, cookie_dict) -> list:
        '''获取本页所有URL'''
        reqHtml = requests.get(url, headers=headers, cookies=cookie_dict)
        reqText = reqHtml.text
        analyseHtml = html.etree.HTML(reqText)
        noteContainers = analyseHtml.xpath(
            '//div[@class="note-container"]')  # 目录
        dataUrls = []  # dataurls 就是所有日志的URL
        for item in noteContainers:
            dataUrls.append(item.attrib['data-url'])
        return dataUrls

    def IsExistsTargetFile(self, year: str, title: str) -> bool:
        '''判断是否已经存在目标文件，决定要不要保存'''
        return os.path.isfile('dataSource/'+year+'/'+title+'.txt')

    def SaveResponseFile(self, year: str, title: str, content: str):
        '''保存文件内容'''
        if(not os.path.isdir('dataSource')):
            os.mkdir('dataSource')
        if(not os.path.isdir('dataSource/'+year)):
            os.mkdir('dataSource/'+year)
        '''todo 此处文件名要替换掉 【\/:*?"<>|】 字符，不然无法保存'''
        fileName = 'dataSource/' + year + '/' + title + '.txt'  # 此处要注意保存的文件名
        if not os.path.isfile(fileName):
            with open(fileName, mode='w', encoding='utf-8') as fd:
                fd.write(content)
