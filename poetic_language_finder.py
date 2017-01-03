# pylint: disable-all
import os
import codecs

import requests
from bs4 import BeautifulSoup

def replace_unicode(string):
    return string.replace("\u2019", "'")

def get_poem(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return replace_unicode(soup.find("div", class_="poem").text)

def poem_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    titles = soup.find_all("a", class_="title")
    return [(t.text, t["href"]) for t in titles]

if __name__ == "__main__":
    for i in range(1, 669):
        print(i)
        poems = poem_list("http://www.poetryfoundation.org/searchresults?page={}".format(i))
        for title, url in poems:
            poem = get_poem("http://www.poetryfoundation.org" + url)
            filename = url.split("/")[-1]
            with codecs.open(os.path.join("scraped_poems", "{}.txt".format(filename)), "w", "utf-8") as f:
                f.write(poem)
