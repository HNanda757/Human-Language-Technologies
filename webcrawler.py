import stopwords as stopwords
from bs4 import BeautifulSoup
import urllib
from urllib import request
import nltk
import requests
from nltk import word_tokenize
from nltk.corpus import stopwords
import itertools
import nltk
import string
import pickle
import re

# Written by Harshith Nanda and Charith Muppidi
start_url = "https://en.wikipedia.org/wiki/Inflation"
headers = {'User-Agent': 'Mozilla/5.0'}
stopwords = stopwords.words('english')


# Build a web crawler function that starts with a URL representing a topic (a sport, your
# favorite film, a celebrity, a political issue, etc.) and outputs a list of at least 15 relevant
# URLs. The URLs can be pages within the original domain but should have a few outside
# the original domain.
def crawl(url, keyword):
    r = requests.get(url, headers=headers)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    url_list = []
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if keyword.capitalize() in link_str or keyword.lower() in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str:
                url_list.append(link_str)
    return url_list


# Write a function to loop through your URLs and scrape all text off each page. Store each
# page’s text in its own file.
def scrape(list_urls):
    file_num = 0
    file_list = []
    for i in list_urls:
        req = request.Request(i, headers=headers)
        res = requests.get(i)
        if res.status_code == 404:
            continue
        html = request.urlopen(req).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        filename = "file" + str(file_num) + ".txt"
        with open(filename, "w", encoding="utf-8") as fp:
            fp.write(soup.get_text())
        file_list.append(filename)
        file_num += 1
    return file_list


# Write a function to clean up the text from each file. You might need to delete newlines
# and tabs first. Extract sentences with NLTK’s sentence tokenizer. Write the sentences for
# each file to a new file. That is, if you have 15 files in, you have 15 files out.
def clean(list_files):
    file_num = 0
    file_list = []
    for i in list_files:
        filename = "newfile" + str(file_num) + ".txt"
        with open(i, 'r', encoding="utf-8") as fp:
            text = fp.read()
        text = re.sub('[\n\t]+', ' ', text)
        text_list = nltk.sent_tokenize(text)
        with open(filename, 'w', encoding="utf-8") as fp:
            [fp.write(str(t)) for t in text_list]
        file_list.append(filename)
        file_num += 1
    return file_list


# Write a function to extract at least 25 important terms from the pages using an
# importance measure such as term frequency, or tf-idf.
# First, it’s a good idea to lowercase everything, remove stopwords and punctuation. Print the top 25-40 terms.
def important_terms(list_pages):
    list_tokens = []
    for i in list_pages:
        with open(i, 'r', encoding="utf-8") as fp:
            text = fp.read()
        tokens = word_tokenize(text)
        english = set(nltk.corpus.words.words())
        tokens = [w.lower() for w in tokens if w not in stopwords and w not in string.punctuation and w in english]
        [list_tokens.append(w) for w in tokens]
    token_set = set(list_tokens)
    tf_dict = {t: list_tokens.count(t) for t in token_set if len(t) > 3}
    tf_dict = dict(sorted(tf_dict.items(), key=lambda x: x[1], reverse=True))
    top = dict(itertools.islice(tf_dict.items(), 40))
    print("Top 40")
    [print(k, ":", v) for k, v in top.items()]
    top = dict(itertools.islice(tf_dict.items(), 10))
    return top


def knowledge_base(list_pages, words):
    kb = {}
    for i in words:
        sent_list = []
        for j in list_pages:
            with open(j, 'r', encoding="utf-8") as fp:
                text = fp.read()
            text = re.sub('[\n\t]+', ' ', text)
            sentences = nltk.sent_tokenize(text)
            [sent_list.append(s) for s in sentences if i in s]
        kb[i] = sent_list
    return kb


if __name__ == '__main__':
    list_one = crawl(start_url, 'inflation')
    list_two = scrape(list_one)
    list_three = clean(list_two)
    dict_one = important_terms(list_three)
    dict_kb = knowledge_base(list_three, dict_one.keys())
    print("Knowledge Base")
    print(dict_one.keys())
    print(dict(itertools.islice(dict_kb.items(), 1)))
    with open('kb.pickle', 'wb') as file:
        pickle.dump(dict_kb, file)
