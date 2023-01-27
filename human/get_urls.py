import threading
import time

import requests


MAX_THREADS = 6
ARTICLES = 120_000
articleCount = 0
pagelinks = set()
title = []
thearticle = []
textLength = []
currentLink=None

def getURLS():
    global pagelinks
    global articleCount
    # store the text for each article
    for _ in range(int(ARTICLES/MAX_THREADS)):
        page = requests.get('https://en.wikipedia.org/wiki/Special:Random')
        time.sleep(0.5)
        currentLink = page.url
        pagelinks.add(currentLink)
        print(str(articleCount) + " " + str(currentLink))
        articleCount += 1


t0 = time.time()
threads = []
for i in range(MAX_THREADS):
    thread = threading.Thread(target=getURLS)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
    with open('article-urls.txt', 'w') as txt:
        for url in pagelinks:
            txt.write("%s\n" % url)
t1 = time.time()
print(f"{t1-t0} seconds to download {articleCount} url.")