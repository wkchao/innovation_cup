import db
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


if __name__ == '__main__':
    main(4)

"""
Topic #0:
俄罗斯 乌克兰 美国 国家 俄乌 普京 中国 局势 谈判 制裁 银行 时间 欧洲 总统 国际 战争 央视 全球 27 北约
Topic #1:
中国 视频 微博 残奥会 北京 公司 2022 哈尔滨 工作 信息 2021 疫情 发展 相关 真的 增长 发布 网友 服务 世界
Topic #2:
考研 复试 cn 视频 http 微博 真的 调剂 英语 学校 老师 电影 23 专业 喜欢 2023 大学 孩子 希望 生活
Topic #3:
疫情 防控 核酸 病例 检测 深圳 工作 香港 确诊 人员 隔离 新冠 新增 健康 28 感染者 社区 防疫 管控 发现
"""
