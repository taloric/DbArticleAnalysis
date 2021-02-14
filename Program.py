import configparser

from Analyzer import TextAnalyzer
from DataCapture import Capture

'''
douban 爬文章 并保存到datasource文件夹(selenuim & requests)
分别用tf-idf textrank算法计算高频词（20个）(jiaba)
做词云(wordcloud)
'''
if __name__ == '__main__':
    '''获取配置'''
    config = configparser.ConfigParser()
    config.read("appconfig.ini")
    configKey = "RemoteInfo"
    RemoteUrl = config.get(configKey, "StartUrl")  # 配置的远端地址
    UserName = config.get(configKey, "UserName")
    Password = config.get(configKey, "Password")
    FontsDir = config.get(configKey, 'FontsDir')

    '''爬取日志'''
    # dataCapture = Capture(RemoteUrl)
    # driver = dataCapture.Login(UserName, Password)
    # dataCapture.RequestAndSave(driver)

    '''分词器生成分词结果'''
    textanalyzer = TextAnalyzer(FontsDir)
    textanalyzer.AllAnalyzer()
