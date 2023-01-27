import time

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

pagelinks = []
title = []
thearticle = []
textLength = []
currentLink=None

with open("urls.txt", "r") as txt:
    for i, url in enumerate(txt):
        # if i == 50:
        #     break
        pagelinks.append(url)
        paragraphtext = []
        page = requests.get(url.replace("\n", ""))
        soup = BeautifulSoup(page.content, 'html.parser')

        # get article title
        atitle = soup.find('h1')
        thetitle = atitle.get_text()
        print(str(i) + " " + thetitle)
        # get text
        articletext = soup.find_all('p')[1:]
        characterCount = 0
        for paragraph in articletext[:-1]:
            # get the text only
            text = paragraph.get_text()
            paragraphtext.append(text)
            characterCount += len(text)
        # combine all paragraphs into an article
        thearticle.append(paragraphtext)
        title.append(thetitle)
        textLength.append(characterCount)

pagelinks = list(pagelinks)
# join paragraphs to re-create the article
myarticle = [' '.join(article) for article in thearticle]

# save article data to file
print(len(title))
print(len(textLength))
print(len(pagelinks))
print(len(myarticle))
data = {'Title': title,
        'Characters': textLength,
        'PageLink':pagelinks,
        'Article':myarticle,
        'Date':datetime.now()}

oldnews = pd.read_excel('wiki\\news.xlsx')
news = pd.DataFrame(data=data)
cols = ['Title', 'Characters', 'PageLink', 'Article', 'Date']
news = news[cols]

afronews = oldnews.append(news)
afronews.drop_duplicates(subset='Title', keep='last', inplace=True)
afronews.reset_index(inplace=True)
afronews.drop(labels='index', axis=1, inplace=True)

filename = 'wiki\\news.xlsx'
wks_name = 'Data'

writer = pd.ExcelWriter(filename)
afronews.to_excel(writer, wks_name, index=False)

writer.save()
