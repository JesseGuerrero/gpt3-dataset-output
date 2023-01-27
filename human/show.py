from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from selenium import webdriver

pagelinks = []
title = []
thearticle = []
textLength = []
currentLink = None
driver = webdriver.Chrome()
with open("news-urls.txt", "r") as txt:
    for i, url in enumerate(txt):
        if i == 100:
            break
        pagelinks.append(url)
        paragraphtext = []
        driver.get(url.replace("\n", ""))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

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
data = {'Title': title,
        'Characters': textLength,
        'PageLink':pagelinks,
        'Article':myarticle,
        'Date':datetime.now()}

oldnews = pd.read_excel('quartz\\news.xlsx')
news = pd.DataFrame(data=data)
cols = ['Title', 'Characters', 'PageLink', 'Article', 'Date']
news = news[cols]

afronews = oldnews.append(news)
afronews.drop_duplicates(subset='Title', keep='last', inplace=True)
afronews.reset_index(inplace=True)
afronews.drop(labels='index', axis=1, inplace=True)

filename = 'quartz\\news.xlsx'
wks_name = 'Data'

writer = pd.ExcelWriter(filename)
afronews.to_excel(writer, wks_name, index=False)

writer.save()
