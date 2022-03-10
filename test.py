import re

_text = "hello,world!!%[545]你好234世界。。。"
_text = re.sub(u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", _text)
print(_text)