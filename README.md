# Search Engine
Contributors: Cleon Doan

## IMPORTANT
The invertedIndex MUST BE BUILT FIRST in indexer.py.  
The CORPUS_SIZE must be changed to match the number of webpages to ensure proper scoring in both indexer.py and searcher.py.  
The PATH string must reference to a file mapping a document ID to the actual webpage in both indexer.py and searcher.py.  

### CORPUS.zip CAN BE DOWNLOADED TO BUILD THE INVERTED INDEX in indexer.py

After the inverted index is built, searcher.py can be ran to open the GUI for the search engine. 
INDEX_PATH references the name of the inverted index built during indexer.py, this is by default named invertedIndex. 

## Background
This project consists of two components: the indexer and searcher.  
- The indexer creates the invertedIndex.  
- The searcher allows user queries and yield the top 20 results based on cosine simlarity scoring calculated from the user query score and the inverted index's scores.  

- This is supported by a GUI made with tkinter.  

The inverted index is created from a json_file referencing a corpus (total set of webpages) that maps a webpage to a number x/y:  
x = the folder number and y = file ID.  The final number x/y is considered the docID.  

An inverted index tracks all the words found in the CORPUS and creates a posting containing data such as term frequency and docIDs(webpage ID).  

This search engine yields query results under 300 ms.

### Libraries used: 
- BeautifulSoup
- nltk, WordNetLemmatizer
- webbrowser
- tkinter 

## Some Weaknesses
The indexer creates a posting that stores string literals that will describe whether a word found in a webpage was also found in the webpage's anchor text.  
However, this information is not used to calculate the final score, this is because I have not yet found an efficient implementation for having it affect the scoring.
