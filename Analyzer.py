import os

from jieba.analyse import *
from wordcloud import WordCloud


class TextAnalyzer(object):
    '''分析器类，用于文本分析'''

    def __init__(self, dir):
        self.fontdir = dir

    def MainAnalyzer(self):
        '''按年度生成词云'''
        rootDir = 'dataSource'
        resultDir = 'dataResult'
        for yearDir in os.listdir(rootDir):
            path = os.path.join(rootDir, yearDir)
            yearContent = ''
            for file in os.listdir(path):
                with open(os.path.join(rootDir, yearDir, file), mode='r', encoding='utf-8') as f:
                    yearContent = yearContent + f.read()
            keyWordList = extract_tags(
                yearContent, topK=25, allowPOS=('ns', 'n', 'vn', 'v'))
            textRankKeyList = textrank(
                yearContent, topK=25, allowPOS=('ns', 'n', 'vn', 'v'))
            keyWord = ' '.join(keyWordList)
            textRankKeyWord = ' '.join(textRankKeyList)
            wc = WordCloud(font_path=self.fontdir,
                           background_color='black', width=600, height=400)
            wc.generate(keyWord).to_file(
                resultDir + '\\' + 'tfidf' + yearDir + '.png')
            wc.generate(textRankKeyWord).to_file(
                resultDir + '\\' + 'tr' + yearDir + '.png')

    def AllAnalyzer(self):
        '''词云汇总'''
        rootDir = 'dataSource'
        resultDir = 'dataResult'
        yearContent = ''
        for yearDir in os.listdir(rootDir):
            path = os.path.join(rootDir, yearDir)
            for file in os.listdir(path):
                with open(os.path.join(rootDir, yearDir, file), mode='r', encoding='utf-8') as f:
                    yearContent = yearContent + f.read()
        keyWordList = extract_tags(
            yearContent, topK=25, allowPOS=('ns', 'n', 'vn', 'v'))
        textRankKeyList = textrank(
            yearContent, topK=25, allowPOS=('ns', 'n', 'vn', 'v'))
        keyWord = ' '.join(keyWordList)
        textRankKeyWord = ' '.join(textRankKeyList)
        wc = WordCloud(font_path=self.fontdir,
                       background_color='black', width=600, height=400)
        wc.generate(keyWord).to_file(resultDir + '\\' + 'tfidf.png')
        wc.generate(textRankKeyWord).to_file(resultDir + '\\' + 'tr.png')
