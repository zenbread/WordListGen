from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import json
import threading
from queue import Queue


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
        json.dump(dict, f, indent=2)
        f.close()
    else:
        with open('test.txt', 'a') as f:
            json.dump(dict, f , indent=2)


def getInfo(word):
    url = "https://www.merriam-webster.com/dictionary/" + word
    try:
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        category = str(soup.find('span', class_='main-attr').find_all('em'))[5:-6]
        with lock:
            dict[word] = category
        time.sleep(.5)
        print(word)
    except:
        pass


def threader():
    while True:
        word = q.get()
        getInfo(word)
        q.task_done()

q = Queue()
lock = threading.Lock()
dict = {}
getList()
for x in range(10):
    t = threading.Thread(target=threader, daemon=True)
    t.start()

for word in words[0:1000]:
    q.put(word)

q.join()
makeFiles(dict)
