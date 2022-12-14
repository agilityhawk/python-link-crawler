import sys, getopt
import requests 
import validators
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urljoin
from multiprocessing import Pool, Queue, Manager
import sqlite3

con = sqlite3.connect("crawled.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS crawled_links(link text PRIMARY KEY, title text, crawl_date text)")

## Globals ##
m = Manager()
queue = m.Queue()

# default
argWebsiteUrl = 'https://www.google.com/search?q=test'
argMaxTasksPerChild = 100
argMaxDepth = 5

## End Globals ##

def main(argv):
    global argWebsiteUrl, argMaxTasksPerChild, argMaxDepth
    options, remaininArgs = getopt.getopt(argv,"w:t:d:",["website=", "maxTasksPerChild=", "maxDepth="])
    argWebsiteUrl = 'https://www.google.com/search?q=test'

    for option, value in options:
        if option in ("-w", "--website"):
            argWebsiteUrl = value
        elif  option in ("-t", "--maxTasksPerChild"):
            argMaxTasksPerChild = int(value)
        elif  option in ("-d", "--maxDepth"):
            argMaxDepth = int(value)

    parseCrawler(argWebsiteUrl, 0)
    print(queue.qsize())

    initializeProcessPool()
    print(queue.qsize())

def parseCrawler(URL, depth=0):
    (scheme, location, path, query, fragment ) = urlsplit(URL)
    baseUrl = scheme + '://' + location

    try:
        if(not validators.url(URL)):
            return 

        response = requests.get(URL)
        responseText = response.text

        soup = BeautifulSoup(responseText, 'html.parser')
        #print(soup)

        title = soup.title.text
        #print('TITLE ', title)

        cur.execute(f"""
            INSERT OR IGNORE INTO crawled_links VALUES
            (?,?,datetime())
        """, (URL, title))
        con.commit()

        for link in soup.find_all('a'):
            linkUrl = link.get('href')

            # Convert relative URL to absolute
            if linkUrl[0] == '/':
                linkUrl = urljoin(baseUrl, linkUrl)

            print(linkUrl)
            queue.put((linkUrl, depth))
    except Exception as err:
        print(err)
        pass

def processQueueItem(que):
    global argMaxDepth

    linkURL, depth = que.get()
    #print(linkURL)
    #print('DEPTH - ', depth)

    if(depth == argMaxDepth):
        print('MAX DEPTH REACHED - RETURNING')
        return

    parseCrawler(linkURL, depth+1)

def initializeProcessPool():
    global argMaxTasksPerChild

    print(argMaxTasksPerChild)

    with Pool(maxtasksperchild=argMaxTasksPerChild) as p:
        #p.apply_async(processQueueItem, (queue,))
        while not queue.empty():
            p.apply_async(processQueueItem, (queue,))
    
    # Wait for the asynchrounous reader threads to finish
    #[r.get() for r in readers]

if __name__=="__main__":
    main(sys.argv[1:])