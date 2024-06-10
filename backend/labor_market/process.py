import re
import nltk
from nltk import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

class ProcessData:

    @classmethod
    def token_and_stem(cls, text):
        stemmer = SnowballStemmer('russian')
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

        filtered_tokens = []
        for token in tokens:
            if re.search('[а-яА-Яa-zA-Z]', token):
                filtered_tokens.append(token)

        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems


    @classmethod
    def get_stopwords(cls):
        stopwords = nltk.corpus.stopwords.words('russian')
        stopwords.extend(nltk.corpus.stopwords.words('english'))
        return stopwords


    @classmethod
    def get_tfidf(cls, dataset):
        tfidf_vectorizer = TfidfVectorizer(min_df=0.01,
                                        token_pattern=r'[(?u)\b\w\w+\bа-яА-Я]+')
        tfidf_matrix = tfidf_vectorizer.fit_transform(dataset)

        return tfidf_matrix.toarray()
        #tokenizer=cls.token_and_stem(dataset)
        #stop_words=cls.get_stopwords(),


    @classmethod
    def dbscan(cls, tfidf_matrix, eps=0.001, min_samples=2, n_jobs=-1, leaf_size=100):
        return DBSCAN(eps=eps, min_samples=min_samples, n_jobs=n_jobs, leaf_size=leaf_size).fit(tfidf_matrix)
    

    @classmethod
    def get_formatted_data(cls, dataset, clusters):
        out = dict(zip(dataset, clusters.labels_.tolist()))
        new_out = {}
        for key, value in out.items():
            if value not in new_out:
                new_out[value] = [key]
            else:
                new_out[value].append(key)

        return {k: v for k, v in sorted(new_out.items(), key=lambda item: len(item[1]), reverse=True)}


    @classmethod
    def get_values(cls, formatted_data):
        return list(formatted_data.values())[1:]