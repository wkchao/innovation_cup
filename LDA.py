import db
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


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

    n_features = 1000
    vec = CountVectorizer(strip_accents='unicode',
                          max_features=n_features,
                          stop_words='english',
                          max_df=0.5,
                          min_df=10)
    trf = TfidfTransformer()

    tf_idf = trf.fit_transform(vec.fit_transform(sql_text))

    w = tf_idf.toarray()
    lda = LatentDirichletAllocation(n_components=cls, max_iter=50,  # 主题个数和EM算法最大迭代次数
                                    learning_method='online',
                                    learning_offset=50,
                                    random_state=0)

    s = lda.fit(w)
    print(s)

    # n个中心点
    print(lda.components_)

    n_top_words = 20
    tf_feature_names = vec.get_feature_names_out()
    print_top_words(lda, tf_feature_names, n_top_words)


if __name__ == '__main__':
    main(5)
