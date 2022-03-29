import json
from nltk.stem import WordNetLemmatizer
import re
from operator import itemgetter
from math import log
from tkinter import *
import webbrowser

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
def search(prequery):
    results = Tk()
    results.title("Search Results ")
    results.geometry("800x600")
    quitButtonResults = Button(results, text="Quit", command=results.destroy)
    quitButtonResults.place(x=750, y=0)
    startingy=30;
    querygen = set(lemmatizer.lemmatize(word.lower()) for word in re.split(r'[^a-zA-Z]', prequery) if
                   word != '' and len(word) >= 3 and word not in stopWords)
    query = ""
    for x in querygen:
        query += x + " "
    searchingFor = Label(results, text="Finding results for the query: "+query)
    searchingFor.place(x=0, y=0)
    #posting is [docID, wordF, termF, TFIDF=0]
    rankings = dict()
    lengthdict = dict()
    query_words = query.split()
    errorWords =[]
    for word in query_words:
        try:
            queryDF = len(invertedIndex[word])
            queryIDF = log(CORPUS_SIZE/queryDF)
            for posting in sorted(invertedIndex[word], key=itemgetter(3), reverse=True):
                url = book_data[posting[0]]
                if url in rankings:
                    rankings[url] += posting[3]*queryIDF
                else:
                    rankings[url] = posting[3]*queryIDF
                lengthdict[url] = posting[4]
        except:
            #search result continues however
            if word not in stopWords:
                errorWords.append(word)
    errorString = "The word(s): "
    for word in errorWords:
        errorString+= word+ " "
    if len(errorWords)>1:
        errorString+="are mispelled or are in no results."
    else:
        errorString+="is mispelled or is in no results."
    word_errors = Label(results, text=errorString)
    word_errors.place(x=0, y=startingy)
    startingy += 25
    for url in rankings:
        rankings[url] = rankings[url]/lengthdict[url]
    top20 = 0
    for x, y in sorted(rankings.items(), key=lambda item: item[1], reverse=True):
        result_ranked = Label(results, text=x, fg= "blue")
        result_ranked.bind("<Button-1>",lambda e, url = x:open_url(url))
        result_ranked.place(x=0, y=startingy)
        startingy+=25
        top20 += 1
        if top20 >= 20:
            break
    results.mainloop()

    return None
def open_url(url):
    webbrowser.open_new_tab(url)

def endTK():
    results.destroy
    searchEngine.destroy
if __name__ == "__main__":
    #https://www.geeksforgeeks.org/destroy-method-in-tkinter-python/
    #https://www.tutorialspoint.com/how-do-you-create-a-clickable-tkinter-label#:~:text=Label%20widgets%20in%20Tkinter%20are,use%20webbrowser%20module%20in%20Python.
    with open("C:/Users/doanc/OneDrive/Desktop/ICS121 Resources/WEBPAGES_RAW/bookkeeping.json") as book_keeping:
        book_data = json.load(book_keeping)
        with open("invertedIndex") as json_file:
            invertedIndex = json.load(json_file)
            lemmatizer = WordNetLemmatizer()
            searchEngine = Tk()
            searchEngine.title("Cleon's Search Engine :D")
            searchEngine.geometry("300x300")
            askLabel = Label(searchEngine, text="Please enter your search query below:")
            askLabel.place(x=40, y=125)
            prequery = Entry(searchEngine)
            prequery.place(x=80, y=150)
            searchButton = Button(searchEngine, text = "Search!", command = lambda x = prequery: search(prequery.get()))
            searchButton.place(x=125, y= 200)
            quitButtonSE = Button(searchEngine, text="Quit",command = searchEngine.destroy)
            quitButtonSE.place(x=250, y=0)
            searchEngine.mainloop()
