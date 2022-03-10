import codecs

import db
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def main(cls):
    sql = db.WB_table_readall()
    sql_text = []
    for i in sql:
        if i[2] != '':
            sql_text.append(i[2])

    with open('calcu_res/text.txt', 'w') as f:
        for i in sql_text:
            f.write(i)
            f.write('\r\n')

    vec = CountVectorizer()
    trf = TfidfTransformer()

    tf_idf = trf.fit_transform(vec.fit_transform(sql_text))
    # word = vec.get_feature_names_out()
    # word_list = vec.get_feature_names()
    # print(word_list)

    w = tf_idf.toarray()

    """
    for i in range(len(w)):
        print(u"------第", i, u"段文本的词语TF—IDF权重------")
        for j in range(len(word_list)):
            if w[i][j]:
                print(word_list[j], w[i][j])
    result = codecs.open("calcu_res/tf_idf_result.txt", 'w', 'utf-8')
    for j in range(len(word)):
        result.write(word[j] + ' ')
    result.write('\r\n\r\n')
    print(u"正在存储文本单词TF-IDF权重...")
    for i in range(len(w)):
        for j in range(len(word)):
            result.write(str(w[i][j]) + ' ')
        result.write('\r\n\r\n')
    result.close()
    print(u"存储完毕！")
    """
    clf = KMeans(n_clusters=cls)
    s = clf.fit(w)
    print(s)

    # n个中心点
    print(clf.cluster_centers_)
    """
    # 每个样本所属的簇
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        i = i + 1
    """
    i = 1
    with open('calcu_res/cluster_result.txt', 'w') as f:  # 存储每个文本对应的类
        while i <= len(clf.labels_):
            f.write(str(i) + ' ' + str(clf.labels_[i - 1]) + '\r\n')
            i = i + 1

    # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print(clf.inertia_)


if __name__ == '__main__':
    main(3)
