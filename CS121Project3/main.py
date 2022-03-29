import re
import json
import sys
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from math import log
from operator import itemgetter

#import nltk
#nltk.download('wordnet')
#nltk.download('omw-1.4')

#constant of the corpus size used to calculate tf idf
CORPUS_SIZE = 37497
stopWords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as',
             'at',
             'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
             "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down',
             'during',
             'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having',
             'he', "he'd",
             "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i',
             "i'd",
             "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me',
             'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
             'other', 'ought', 'our', 'ours',
             'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should',
             "shouldn't", 'so', 'some', 'such',
             'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's",
             'these', 'they', "they'd",
             "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very',
             'was', "wasn't", 'we',
             "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where',
             "where's", 'which', 'while',
             'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll",
             "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
invertedIndex = defaultdict(list)
uniqueWords = set()

def tokenize(web_page,docID):
    global docIDLength
    #https://developer.mozilla.org/en-US/docs/Web/HTML/Element
    #https://www.geeksforgeeks.org/python-lemmatization-with-nltk/
    #http://www.tfidf.com/
    global stopWords
    strongWords = []
    titleWords = []
    boldWords =[]
    headerWords = []
    headers = ["h1","h2","h3","h4","h5","h6"]
    tokenList=[]
    soup = BeautifulSoup(web_page, 'lxml')
    lemmatizer = WordNetLemmatizer()
    for tag in soup.find_all(["p","b","title","h1","h2","h3","header","strong"]):
        words = (lemmatizer.lemmatize(t.lower()) for t in re.split(r'[^a-zA-Z]', tag.get_text()) if
                      t != '' and len(t) >= 3 and t not in stopWords)
        if tag in soup.find_all("strong"):
            for word in words:
                strongWords.append(word)
        if tag in soup.find_all("bold"):
            for word in words:
                boldWords.append(word)
        if tag in soup.find_all("title"):
            for word in words:
                titleWords.append(word)
        for header in headers:
            if tag in soup.find_all(header):
                for word in words:
                    headerWords.append([word,header])
        for word in words:
            tokenList.append(word)
    for word in tokenList:
        uniqueWords.add(word)
        for docInfo in invertedIndex[word]:
            if docID in docInfo:
                #index 0 holds the docID
                #index 1 holds the same word frequency in the doc
                #index 2 holds tf, the term frequency
                #index 3 holds the tfidf to be calculated later stays at 0
                #index 4 holds LengthD
                #index 5 holds metaTags the doc has for this word
                docInfo[1]+=1
                tf = docInfo[1]/len(tokenList)
                docInfo[2] = 1+log(tf)
                docInfo[4] = len(tokenList)
                if word in strongWords:
                    docInfo[5].add("strong")
                if word in titleWords:
                    docInfo[5].add("title")
                if word in boldWords:
                    docInfo[5].add("bold")
                for (headerList,headerName) in headerWords:
                    if word in headerList:
                        docInfo[5].add(str(headerName))
                if len(docInfo[5]) != 0:
                    print(docInfo[5])
                break
        else:
            invertedIndex[word].append([docID,1, 1+log(1/len(tokenList)), 0, len(tokenList),set()])
    print(docID)
def calculateTFIDF(invertedIndex):
    #t is the term and docInfo is a list of the postings[docID, wordF, termF, TFIDF=0]
    for t,docInfos in invertedIndex.items():
        for posting in docInfos:
            idf = log((CORPUS_SIZE)/len(docInfos))
            posting[3] = posting[2]*idf


if __name__ == "__main__":
    docCounter = 0;
    with open("C:/Users/doanc/OneDrive/Desktop/ICS121 Resources/WEBPAGES_RAW/bookkeeping.json") as book_keeping:
        book_data = json.load(book_keeping)
    for docID in book_data.keys():
        #docID is a string of a x/y; x being folder number and y being webpage number
        with open("C:/Users/doanc/OneDrive/Desktop/ICS121 Resources/WEBPAGES_RAW/"+docID, encoding = "utf-8") as web_page:
            docCounter+=1;
            tokenize(web_page,docID)
    calculateTFIDF(invertedIndex)
    indexSize = 0
    file = open("CS121Project3Deliverables.txt",'w')
    file.write("The number of documents is "+str(CORPUS_SIZE)+".\n")
    file.write("The number of unique words is "+str(len(uniqueWords))+".\n")
    indexSize += sys.getsizeof(invertedIndex)
    for k,v in invertedIndex.items():
        indexSize+=sys.getsizeof(k)
        indexSize+=sys.getsizeof(v)
        for posting in v:
            indexSize+=sys.getsizeof(posting)
            for info in posting:
                indexSize+=sys.getsizeof(info)

    file.write("The size of the index is "+str(indexSize*0.001)+"kB.\n")
    file.write("The query 'informatics' has "+str(len(invertedIndex["informatics"]))+ " results.\n")
    file.write("The first 20 are: \n")
    twentyCounter = 0
    for posting in sorted(invertedIndex["informatics"], key = itemgetter(3),reverse = True):
        file.write(book_data[posting[0]]+"\n")
        twentyCounter+=1
        if twentyCounter >= 20:
            break

    file.write("The query 'mondego' has "+str(len(invertedIndex["mondego"]))+ " results.\n")
    file.write("The first 20 are: \n")
    twentyCounter = 0
    for posting in sorted(invertedIndex["mondego"], key = itemgetter(3),reverse = True):
        file.write(book_data[posting[0]]+"\n")
        twentyCounter+=1
        if twentyCounter >= 20:
            break

    twentyCounter = 0
    file.write("The query 'irvine' has "+str(len(invertedIndex["irvine"]))+ " results.\n")
    file.write("The first 20 are: \n")
    for posting in sorted(invertedIndex["irvine"], key = itemgetter(3),reverse=True):
        file.write(book_data[posting[0]]+"\n")
        twentyCounter+=1
        if twentyCounter >= 20:
            break
    file.close()
    for term,postings in invertedIndex.items():
        for posting in postings:
            posting[5] = list(posting[5])
    with open("invertedIndex",'w') as myIndex:
        json.dump(invertedIndex, myIndex)
    query = input("Enter your query here: ").lower()
    print(query)