from bs4 import BeautifulSoup
import requests, heapq, re

import nltk
#nltk.download()

while(True):
    search = input("Search: ")
    if search=="":
        break
    search.lower()
    search.replace(" ","_")
    URL = "https://en.wikipedia.org/wiki/"+search

    page = requests.get(URL)
     
    soup = BeautifulSoup(page.content, 'html.parser')

    text = ""
    for e in soup.find_all('p'):
        text+=e.text

    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    ftext = re.sub('[^a-zA-Z]', ' ', text )
    ftext = re.sub(r'\s+', ' ', ftext)

    stopwords = nltk.corpus.stopwords.words('english')
    sentences = nltk.sent_tokenize(text)

    freqs = {}
    for word in nltk.word_tokenize(ftext):
        if word not in stopwords:
            if word not in freqs.keys():
                freqs[word] = 1
            else:
                freqs[word] += 1

    max_freq= max(freqs.values())

    for word in freqs.keys():
        freqs[word] = (freqs[word]/max_freq)

    scores = {}
    for s in sentences:
        for word in nltk.word_tokenize(s.lower()):
            if word in freqs.keys():
                if len(s.split(' ')) < 30:
                    if s not in scores.keys():
                        scores[s] = freqs[word]
                    else:
                        scores[s] += freqs[word]

    summary = heapq.nlargest(7, scores, key=scores.get)

    summary = ' '.join(summary)
    print(summary)
