import numpy as np
import pandas as pd
import tensorflow as tf
import keras
import os
from keras.utils import get_file
import subprocess
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import json
from collections import Counter
from itertools import chain
import gensim
import random
import requests
import geopandas as gpd
import csv
from sklearn import svm

# 下载GoogleNews-vectors-negative300模型
MODEL = 'GoogleNews-vectors-negative300.bin.gz'
# path = get_file(MODEL + '.gz', 'https://deeplearning4jblob.blob.core.windows.net/resources/wordvectors/%s.gz' % MODEL)
# if not os.path.isdir('generated'):
#     os.mkdir('generated')
#
unzipped = os.path.join('generated', MODEL)
# if not os.path.isfile(unzipped):
#     with open(unzipped, 'wb') as fout:
#         zcat = subprocess.Popen(['zcat'],
#                                 stdin=open(path),
#                                 stdout=fout)
#         zcat.wait()

# 模型的加载
model = gensim.models.KeyedVectors.load_word2vec_format(unzipped, binary=True)

# model.most_similar(positive=['espresso'])
#
#
# def A_is_to_B_as_C_is_to(a, b, c, topn=1):
#     a, b, c = map(lambda x: x if type(x) == list else [x], (a, b, c))
#     res = model.most_similar(positive=b + c, negative=a, topn=topn)
#     if len(res):
#         if topn == 1:
#             return res[0][0]
#         return [x[0] for x in res]
#     return None
#
#
# for country in 'Italy', 'France', 'India', 'China':
#     print('%s is the capital of %s' %
#           (A_is_to_B_as_C_is_to('Germany', 'Berlin', country), country))


# beverages = ['espresso', 'beer', 'vodka', 'wine', 'cola', 'tea']
# countries = ['Italy', 'Germany', 'Russia', 'France', 'USA', 'India']
# sports = ['soccer', 'handball', 'hockey', 'cycling', 'basketball', 'cricket']
#
# items = beverages + countries + sports
# print(len(items))
#
# item_vectors = [(item, model[item]) for item in items if item in model]
#
# vectors = np.asarray([x[1] for x in item_vectors])
# lengths = np.linalg.norm(vectors, axis=1)
# print(vectors.shape)
# print(lengths.shape)
# norm_vectors = (vectors.T / lengths).T
#
# tsne = TSNE(n_components=2, perplexity=10, verbose=2).fit_transform(norm_vectors)
# print(tsne.shape)
# x = tsne[:, 0]
# y = tsne[:, 1]
#
# fig, ax = plt.subplots()
# ax.scatter(x, y)
#
# for item, x1, y1 in zip(item_vectors, x, y):
#     ax.annotate(item[0], (x1, y1), size=14)
#
# plt.show()
#
#
countries = list(csv.DictReader(open('countries.csv')))

# positive = [x['name'] for x in random.sample(countries, 40)]
# negative = random.sample(model.vocab.keys(), 5000)
# print(negative[:4])
#
# labelled = [(p, 1) for p in positive] + [(n, 0) for n in negative]
# random.shuffle(labelled)
# X = np.asarray([model[w] for w, l in labelled])
# y = np.asarray([l for w, l in labelled])
#
# TRAINING_FRACTION = 0.3
# cut_off = int(TRAINING_FRACTION * len(labelled))
# clf = svm.SVC(kernel='linear')
# clf.fit(X[:cut_off], y[:cut_off])
#
# res = clf.predict(X[cut_off:])
# missed = [country for (pred, truth, country) in zip(res, y[cut_off:], labelled[cut_off:]) if pred != truth]
# print(100 - 100 * float(len(missed)) / len(res), missed)
#
# all_predictions = clf.predict(model.syn0)
# res = []
# for word, pred in zip(model.index2word, all_predictions):
#     if pred:
#         res.append(word)
#         if len(res) == 150:
#             break
# print(random.sample(res, 10))


country_to_idx = {country['name']: idx for idx, country in enumerate(countries)}
country_vecs = np.asarray([model[c['name']] for c in countries])


#
#
# # dists = np.dot(country_vecs, country_vecs[country_to_idx['Canada']])
# # for idx in reversed(np.argsort(dists)[-10:]):
# #     print(countries[idx]['name'], dists[idx])
#
#
def rank_countries(term, topn=10, field="name"):
    if not term in model:
        return []
    vec = model[term]
    dists = np.dot(country_vecs, vec)
    return [(countries[idx][field], float(dists[idx]))
            for idx in reversed(np.argsort(dists)[-topn:])]


#
#
# print(rank_countries('cricket'))

# 加载数据
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
print(world.head())


def map_term(term):
    d = {k.upper(): v for k, v in rank_countries(term, topn=0, field="cc3")}
    world[term] = world["iso_a3"].map(d)
    world[term] /= world[term].max()
    world.dropna().plot(term, cmap='OrRd')


map_term("coffee")
plt.show()