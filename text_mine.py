#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 13:38:25 2017

@author: bella
"""

import data_preprocess
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tweet_dt = data_preprocess.tweet()
inst_dt = data_preprocess.instagram()

tweet_df = pd.DataFrame(tweet_dt)
inst_df = pd.DataFrame(inst_dt)


############### HISTOGRAM #################

''' tweet_df.describe() all 0 for numerical data, so drop the columns'''
tweet_df = tweet_df.drop(['favor_cnt', 'favor_t_cnt', 'retweet_cnt', 'retweet_t_cnt'], axis =1)
tweet_df.tweet_cnt.quantile([0, .25, .5, .75, 1])
plt.hist(tweet_df.tweet_cnt, bins = 10)
plt.xlabel('number of posts per event')
plt.ylabel('frequency')
plt.savefig('output/tweet_histogram.png')

plt.hist(inst_df.inst_cnt, bins = 100)
plt.xlabel('number of posts per event', size = 15)
plt.ylabel('frequency', size = 15)
plt.savefig('output/instagram_histogram.png')

hist_t = tweet_df.loc[:, ['oid', 'tweet_cnt']]
hist_i = inst_df.loc[:, ['oid', 'inst_cnt']]
hist_t.to_csv('output/tweet_hist.csv')
hist_t.to_csv('output/instagram_hist.csv')

tweet_df.to_csv('output/tweet_data.csv')
inst_df.to_csv('output/instagram_data.csv')



################### VIZ ################
inst_viz = data_preprocess.inst_viz()
viz_df = pd.DataFrame(inst_viz)
viz_df.to_csv('output/viz_df.csv')
viz_df.to_csv('viz/viz_df.csv')

''' topic model

le = LabelEncoder()
doc_y = le.fit_transform(tweet_df.oid)

## data clean
docs = [''.join(i) for i in tweet_df.tweets]

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in docs]  


## document-term matrix
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

## LDA Model
Lda = gensim.models.ldamodel.LdaModel
ldamodel =Lda(doc_term_matrix, num_topics =4, id2word = dictionary, passes =50)


ldamodel.print_topics(num_topics = 4, num_words =10)


'''