import db
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

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

    # TfidfTransformer
    vec = CountVectorizer(strip_accents='unicode',
                          max_features=n_features,
                          stop_words=None,  # 设置为 None 且 max_df 在0.7~1.0时根据当前语料库自动建立停用词表
                          max_df=0.95,  # float 比例，关键词阈值，大于这个则变为停用词
                          min_df=2)  # int，小于则不当关键词
    lda = LatentDirichletAllocation(n_components=cls,  # 主题个数
                                    max_iter=20,  # EM算法最大迭代次数，实际应用时上千次
                                    learning_method='online',
                                    learning_offset=50,
                                    random_state=0)
    tf = vec.fit_transform(sql_text)
    # LDA 应选择 TF，参考文档：https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda
    # .html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py
    s = lda.fit(tf)
    print(s)

    # n个中心点
    print(lda.components_)

    n_top_words = 20
    tf_feature_names = vec.get_feature_names_out()
    print_top_words(lda, tf_feature_names, n_top_words)
    # 可视化
    pic = pyLDAvis.sklearn.prepare(lda, tf, vec)
    pyLDAvis.save_html(pic, 'lda_pass'+str(cls)+'.html')


if __name__ == '__main__':
    main(4)

"""
Topic #0:
疫情 防控 核酸 病例 工作 检测 深圳 人员 香港 确诊 新冠 隔离 新增 感染者 健康 社区 28 本土 视频 防疫
Topic #1:
考研 视频 复试 微博 真的 残奥会 北京 cn http 调剂 学校 英语 老师 2022 23 专业 哈尔滨 喜欢 孩子 生活
Topic #2:
俄罗斯 中国 美国 国家 公司 乌克兰 经济 制裁 全球 银行 发展 国际 2021 欧洲 北约 市场 增长 影响 系统 金融
Topic #3:
乌克兰 视频 俄罗斯 微博 电影 cn 谈判 http 俄乌 网友 普京 时间 总统 新闻 记者 战争 中国 报道 提供 国家
"""
