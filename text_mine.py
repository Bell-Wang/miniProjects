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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sys
from collections import Counter
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS

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



################### SHINY VIZ 1 ################
inst_viz = data_preprocess.inst_viz()
viz_df = pd.DataFrame(inst_viz)
viz_df.to_csv('output/viz_df.csv')
viz_df.to_csv('viz/viz_df.csv')



############ TEXT MINING #########

le = LabelEncoder()
doc_y = le.fit_transform(inst_df.oid)

## data clean
docs = [''.join(i) for i in inst_df.inst]
tags_docs = [' '.join(i) for i in inst_df.tag]

inst_txt = [list(i)[0] + list(i)[1] for i in zip(docs, tags_docs)]

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean1(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean1(doc).split() for doc in inst_txt]  

## term frequency
top_15 = [[i[0] for i in sorted(dict(Counter(i)).items(), key = lambda s:s[1], reverse= True)[:15]] for i in doc_clean]


## tfidf clustering
def clean2(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized.split()

def tfidf_kmean(num_clusters, num_term):

    tfidf_vectorizer = TfidfVectorizer(max_df = 0.8, max_features = 200000,
                                  min_df = 0.1, stop_words = 'english',
                                  use_idf = True, tokenizer = clean2,
                                  ngram_range = (1, 3))

    tfidf_matrix =  tfidf_vectorizer.fit_transform(inst_txt)
    term = tfidf_vectorizer.get_feature_names()

    dist = 1 - cosine_similarity(tfidf_matrix)
    km = KMeans(num_clusters)
    km.fit(tfidf_matrix)

    order_centroids = km.cluster_centers_.argsort()[:,::-1]
    clusters = km.labels_.tolist()
    cluster_term = {s : [term[i] for i in order_centroids[s,:num_term]] for s in range(order_centroids.shape[0])}
    doc_cluster_term = [' '.join(cluster_term.get(i)).title() for i in clusters]
    cluster_term = {s: ' '.join(t).title() for s, t in cluster_term.items()}

    my_dict = {'event': inst_df.oid, 'cluster': clusters, 'instagram': inst_txt, 'cluster_term': doc_cluster_term}
    my_dataframe = pd.DataFrame(my_dict)    
    return my_dataframe, cluster_term

my_dataframe, cluster_term = tfidf_kmean(6, 7)
my_dataframe.cluster.value_counts()

my_dataframe['topic'] = np.where()
{0: 'Concert',
 1: 'Holiday',
 2: 'Party',
 3: 'Fashion',
 4: 'Superbowl',
 5: 'Game'}

%matplotlib
## cluster visualization
def cluster_viz(show_arg, output):

    MDS()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist) 
    xs, ys = pos[:, 0], pos[:, 1]
    
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e',
                     5: '#f9e79f', 6: '#3498db'}
    
    df = pd.DataFrame(dict(x=xs, y=ys, label=my_dataframe.cluster.values, title=show_arg)) 
    
    groups = df.groupby('label')
    fig, ax = plt.subplots(figsize=(40, 20)) # set size
    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
                label=cluster_term[name], color=cluster_colors[name], 
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')
        ax.tick_params(\
            axis= 'y',         # changes apply to the y-axis
            which='both',      # both major and minor ticks are affected
            left='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelleft='off')    
    ax.legend(numpoints=1)  #show legend with only 1 point
    
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  
    
    plt.show() 
    plt.savefig(output)


cluster_viz(my_dataframe.event.values, 'output/event_cluster.png')
cluster_viz(my_dataframe.instagram.values, 'output/instagram_cluster.png')


#################### SHINY VIZ 2################
# get lat and lng from viz_df
tm1 = viz_df.loc[:, ['oid', 'mid_lat', 'mid_lng']].drop_duplicates()

## LDA document-term matrix
dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

## LDA Model
Lda = gensim.models.ldamodel.LdaModel
ldamodel =Lda(doc_term_matrix, num_topics = 5, id2word = dictionary, passes = 50)


ldamodel.print_topics(num_topics = 5, num_words = 15)


