from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import json


def getList():
    global words
    words = []
    f = open('words.txt', 'r')
    for line in f:
        words.append(line.replace('\n',''))
    f.close()

def makeFiles(dict):
    if not os.path.exists('test.txt'):
        f = open('test.txt', 'w+')
        json.dump(dict, f)
        f.close()
    else:
        with open('test.txt', 'a') as f:
            json.dump(dict, f)

getList()
dict = {}
for word in words[1000:2000]:
    url = "https://www.merriam-webster.com/dictionary/" + word
    try:
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        category = str(soup.find('span', class_='main-attr').find_all('em'))[5:-6]
        dict[word] = category
        time.sleep(.5)
        print(word)
    except:
        pass


makeFiles(dict)