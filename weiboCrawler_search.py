import urllib
from urllib.parse import urlencode
import requests
import func
from pyquery import PyQuery as pq
import time
import db


head_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type'
tail_url = '&page_type=searchall&page='


def base_url(_word, i):
    _word = urllib.parse.quote("=1&q=" + _word)
    return head_url + str(_word) + tail_url + str(i)


headers = {
    'Referer': 'https://m.weibo.cn/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_page(_word, _page):
    """
    web 请求
    :param _page: 页数
    :return: 对应 web API返回的 json
    """
    _page = str(_page)
    url = base_url(_word, _page)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(_page + '搜索成功！')
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(_json):
    """
    对返回的 json 进行解析
    :param _json: web API 返回的 json
    :return:
    """
    if _json is not None:
        items = _json.get('data').get('cards')
        for i in items:
            if i is None:
                continue
            i = i.get('card_group')[0].get('mblog')
            weibo = {'id': i.get('mid'), 'createTime': i.get('created_at')}
            isLongText = i.get('isLongText')
            if isLongText:
                states = 'https://m.weibo.cn/statuses/extend?id=' + weibo['id']
                print("开始查看全文，为：" + states)
                try:
                    resp = requests.get(states, headers=headers)
                    if resp.status_code == 200:
                        print('查看全文成功！')
                except requests.ConnectionError as e:
                    print('Error', e.args)
                    continue
                try:
                    if resp.json().get('ok') == 0:
                        print(resp.json().get('msg'))
                    else:
                        _text = resp.json().get('data').get('longTextContent')
                        _text = pq(_text).text().replace(" ", "").replace("\n", "")
                except requests.AttributeError as e:
                    print('Error', e.args)
                    continue
            else:
                _text = pq(i.get('text')).text().replace(" ", "").replace("\n", "")
            weibo['text'] = func.seg_depart(_text)

            db.WB_table_insert(weibo)


def main(_word, num):
    for page in range(2, num):
        try:
            time.sleep(0.1)
            json = get_page(_word, page)
            parse_page(json)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    word = input(":")
    main(word, 100)

