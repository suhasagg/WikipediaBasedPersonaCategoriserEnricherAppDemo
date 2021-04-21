from twisted.internet import reactor, threads
#import httplib
import itertools

from newspaper import Article


concurrent = 500
finished=itertools.count(1)
reactor.suggestThreadPoolSize(concurrent)

def getStatus(ourl):
    article = Article(ourl)
    article.download()
     #  print(article.html)
    article.parse()
    a=article.authors
    print(a)
    b=article.publish_date
    print(b)
    c=article.top_image
    print(c)
    d=article.title
    print(d)
    

def processResponse(response,url):
   # print response, url
    processedOne()

def processError(error,url):
    #print "error", url#, error
    processedOne()

def processedOne():
    if finished.next()==added:
        reactor.stop()

def addTask(url):
    req = threads.deferToThread(getStatus, url)
    req.addCallback(processResponse, url)
    req.addErrback(processError, url)   

added=0
for url in open('shopcluesurl2.txt'):
    added+=1
    addTask(url.strip())

try:
    reactor.run()
except KeyboardInterrupt:
    reactor.stop()
