import requests
import re
import os
import datetime
import bs4
import time
import db
import func

def getText(url):
    """

    :param url:
    :return:
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text


def gen_dates(startDate, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield startDate + day * i


def getPageList(year, month, day, dir):
    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'
    html = getText(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    pageList = bsobj.find('div', attrs={'class': 'swiper-container'}).find_all('div', attrs = {'class': 'swiper-slide'})
    linkList = []

    for page in pageList:
        link = page.a["href"]
        url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
        linkList.append(url)

    return linkList


def getTitleList(year, month, day, pageUrl):
    '''
    功能：获取报纸某一版面的文章链接列表
    '''
    html = getText(pageUrl)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    titleList = bsobj.find('ul', attrs={'class': 'news-list'}).find_all('li')
    linkList = []

    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:
                url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
                linkList.append(url)

    return linkList


def getContent(text):
    '''
    功能：解析 HTML 网页，获取新闻的文章内容
    '''
    bsobj = bs4.BeautifulSoup(text, 'html.parser')

    # 获取文章 标题
    title = bsobj.h3.text + '\n' + bsobj.h1.text + '\n' + bsobj.h2.text + '\n'
    # print(title)

    # 获取文章 内容
    pList = bsobj.find('div', attrs={'id': 'ozoom'}).find_all('p')
    content = ''
    for p in pList:
        content += p.text + '\n'
        # print(content)

    # 返回结果 标题+内容
    resp = title + content
    return resp


def saveFile(content, path, filename):
    '''
    功能：将文章内容 content 保存到本地文件中
    参数：要保存的内容，路径，文件名
    '''
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)
        print(filename + ' success')


def peoplesDaily(startDate, endDate, dir):
    """
    20210101-
    :param startDate:
    :param endDate:
    :param dir:
    :return:
    """
    time.sleep(0.5)
    start = datetime.datetime.strptime(startDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")
    contentList = []

    for date in gen_dates(start, (end - start).days):
        year = str(date.year)
        month = str(date.month) if date.month >= 10 else '0' + str(date.month)
        day = str(date.day) if date.day >= 10 else '0' + str(date.day)
        pageList = getPageList(year, month, day, dir)
        for page in pageList:
            titleList = getTitleList(year, month, day, page)
            for url in titleList:
                text = getText(url)
                content = getContent(text)

                temp = url.split('_')[2].split('.')[0].split('-')
                pageNo = temp[1]
                titleNo = temp[0] if int(temp[0]) >= 10 else '0' + temp[0]
                # path = dir + '/' + year + month + day + '/'
                # fileName = year + month + day + '-' + pageNo + '-' + titleNo + '.txt'
                createTime = year + month + day + '-' + pageNo + '-' + titleNo
                # saveFile(content, path, fileName)
                # contentList.append(content)
                item = {}
                item['id'] = year + month + day + pageNo + titleNo
                item['createTime'] = createTime
                item['text'] = func.seg_depart(content)
                db.PD_table_insert(item)
                print(item['id'] + '存储成功！')

    # print(len(contentList))
    # return contentList


if __name__ == '__main__':
    a = '20220101'
    b = '20220105'
    peoplesDaily(a, b, '.')




















