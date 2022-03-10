import jieba
import re


def seg_depart(_text):
    stopwords = [line.strip() for line in open('./stopwords.txt', encoding='utf-8').readlines()]
    _text = re.sub(u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", _text)
    sentence_depart = jieba.cut(_text.strip())
    text = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                text = text + word + ' '
    return text if text != '' else None
