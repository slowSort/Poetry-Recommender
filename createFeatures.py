from urllib.request import urlopen
import json

def poemsOfLength(lineNumber):
    postRequest = 'http://poetrydb.org/linecount/{}:abs'.format(lineNumber)
    content = urlopen(postRequest).read()
    contentJSON = json.loads(content.decode('utf-8')) #convert to json format
    return contentJSON

def poemsShorterOrEqualTo(lineNumber):
    poems = []
    for number in range(1, lineNumber+1):
        poems.extend(poemsOfLength(number))
    return poems

def findWordCount(poem):
    wordCount = 0
    for line in poem['lines']:
        wordsInLine = line.split(" ")
        wordCount += len(wordsInLine)
    return wordCount


poems = poemsShorterOrEqualTo(2)

for poem in poems:
    print("title: " + poem['title'])
    print("author: " + poem['author'])
    print("lines: " + poem['lines'][0] + "...")
    print("linecount: " + poem['linecount'])
    print("wordcount: " + str(findWordCount(poem)))
