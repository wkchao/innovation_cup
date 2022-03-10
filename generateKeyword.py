from sklearn.feature_extraction.text import TfidfVectorizer
import dataCrawler
corpus = [
     'This is the first document.',
     'This document is the second document.',
     'And this is the third one.',
     'Is this the first document?',
]
corpus = dataCrawler.peoplesDaily('20210101', '20210102', '.')
print(corpus[0])
tfidf = TfidfVectorizer()
re = tfidf.fit_transform(corpus)
print(tfidf.get_feature_names())
print(re.toarray())

