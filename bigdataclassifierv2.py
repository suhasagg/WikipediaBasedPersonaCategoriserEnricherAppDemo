import tagme
import wikipedia
import mediawikiapi
import wikidata
import collections
from newspaper import Article
import urllib.request
import requests
import json
import sys
import csv
from flask import Flask, request
from flask_restful import Resource, Api
import numpy as np
import gensim
from json import dumps

app = Flask(__name__)
api = Api(app)

class computeIAB(Resource):
    def get(self):
        #Connect to databse

        import urllib
        from flask import request
        args = request.args
        print(args)  # For debugging
        text = args['url']
        import urllib.parse
        text=urllib.parse.unquote(text)
        text1 = text
        article = Article(text1)
        article.download()
        article.parse()
        # article.nlp()
        text = article.title
        text = text.replace("’", "")
        print(text)

        r1 = requests.get("http://localhost:8080/SemanticClassifierv2/getTextAnalysis?text=" + text)

        jData = json.loads(r1.content)
        print(jData)

        for x in jData:
            if x['rho'] < 0.2:
                jData.remove(x)
        y = ""
        z = []
        k = ""

        with open('All_hidden_categories.txt', encoding="utf8") as f:
            hiddencategories = f.read().splitlines()
        # text1=article.meta_keywords[0]


        rankedcategories = {}
        with open('ranked-categories.csv', encoding="utf8") as csv_file:
            for row in csv.reader(csv_file, delimiter='\t'):
                if len(row) > 1:
                    rankedcategories[row[0]] = row[1]
        words1 = []
        for x in jData:
            y = y + " " + x['Title']
            # z.append(x['category'])
            words = x['category']
            for p in words:
                if "Article" not in p:
                    if "articles" not in p:
                        if "history" not in p:
                            if "Pages" not in p:
                                if p not in hiddencategories:
                                    if p in rankedcategories:
                                        words1.append(p)
        k = " ".join(str(v) for v in words1)
        print(y)
        print(k)
        if y is "":
            y = text

        r = requests.get("http://localhost:5000/IAB/" + y.lower().replace("-", ""))
        print(r.content)
        data = r.content.decode("utf-8").strip().replace('"','')
        print(data)
        return data


api.add_resource(computeIAB, '/getTextCategory',endpoint='getTextCategory')

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=80,threaded=True)



