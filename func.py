import jieba
import jieba.posseg
import re


def seg_depart(_text):
    stopwords = [line.strip() for line in open('./stopwords.txt', encoding='utf-8').readlines()]
    _text = re.sub(u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", _text)
    sentence_depart = jieba.posseg.cut(_text.strip(), use_paddle=True)
    text = ''
    for word, flag in sentence_depart:
        if word not in stopwords:
            if word != '\t' and flag in ['n', 's', 'ns', 'nt', 'nw', 'nz', 'PER', 'LOC', 'ORG']:
                text = text + word + ' '
    return text if text != '' else None
