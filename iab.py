from flask import Flask, request
from flask_restful import Resource, Api
import numpy as np
import gensim
from json import dumps

app = Flask(__name__)
api = Api(app)

modeldata = None
staticVectors = {}
from gensim.models.keyedvectors import KeyedVectors

fn = "googlenews"


class computeIAB(Resource):
    def get(self, text):
        # Connect to databse
        model = loadModel()
        import urllib
        text = urllib.parse.unquote(urllib.parse.unquote(text))
        sentence_1 = text
        # Derive sentence word vector and pass it to category vector similarity function
        sentence_1_avg_vector = avg_feature_vector(sentence_1.split(), model, num_features=300,
                                                   index2word_set=set(model.wv.index2word))
        # print(sentence_1_avg_vector)
        return computeSimilarity(sentence_1_avg_vector, model)


# get average vector for sentence 2


# Perform query and return JSON data


# import redis
# redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
# model  = redis_db.get('model')
# if model is None:

def loadModel():
    # Connect to databse
    global modeldata
    if modeldata is None:
        # Load wikipedia word vectors
        modeldata = KeyedVectors.load_word2vec_format("/root/fastText-master/word2vecdata/wiki.en.vec")
    # redis_db.set('model', model)
    # modeldata= KeyedVectors.load_word2vec_format("googlenews",binary=True)
    return modeldata


import math


def cosine_similarity(v1, v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    from scipy.spatial.distance import cosine
    return 1 - (cosine(v1, v2))


def avg_feature_vector(words, model, num_features, index2word_set):
    # function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    # list containing names of words in the vocabulary
    # index2word_set = set(model.index2word) this is moved as input param for performance reasons
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1
            featureVec = np.add(featureVec, model[word])

    if (nwords > 0):
        featureVec = np.divide(featureVec, nwords)
    return featureVec


# get average vector for sentence 1
# Read Category Data from Category File
fname = "segments1.txt"
with open(fname) as f:
    content = f.readlines()


# get average vector for sentence 2

def computeSimilarity(sentence_1_avg_vector, model):
    i = 0
    highestScore = 0

    similarSentence = ""

    global content

    content1 = [x.strip() for x in content]
    # global modeldata
    # model = modeldata
    for y in content1:
        sentence_2 = y
        i = i + 1
        import memcache
        # Cache Category Word vectors in Memcached
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)

        #    mc.set(y, sentence_2_avg_vector)
        k = y.replace(" ", "").replace(",", "").replace("'", "")
        # print(k)
        # Get category word vectors from memcached
        value = mc.get(k + "wiki")

        #        print(i)
        # Derive cosine similarity with category word vectors to figure out the category
        if value is not None:
            sen1_sen2_similarity = cosine_similarity(sentence_1_avg_vector, value)

        else:

            # if staticVectors.get(y) is None:
            sentence_2_avg_vector = avg_feature_vector(sentence_2.split(), model, num_features=300,
                                                       index2word_set=set(model.wv.index2word))
            mc.set(k + "wiki", sentence_2_avg_vector)
            # else:
            # sentence_2_avg_vector = staticVectors[y]
            # print(sentence_2_avg_vector)
            sen1_sen2_similarity = cosine_similarity(sentence_1_avg_vector, sentence_2_avg_vector)

        #        print(sen1_sen2_similarity)
        #        print(highestScore)
        if sen1_sen2_similarity > highestScore:
            highestScore = sen1_sen2_similarity
            similarSentence = y
    #           print(highestScore)
    #           print(similarSentence)
    #           print(i)
    highestScore = 0
    i = 0
    return similarSentence


# print(similarSentence)
# print(highestScore)

api.add_resource(computeIAB, '/IAB/<string:text>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
