# Test python crawler 

## Prerequisites
- Python 3
- The file `requirements.txt` has the list of dependent python modules needed to run this crawler script.

- Before initiating the crawler, please run the following command to install all the dependencies.

```
pip install -r requirements.txt
```

## Initiating the crawler
Run the following command in your terminal to start the crawler.

Provide the URL of the website to crawl as an argument to the script as shown below.

```
python src/runcrawler.py -w https://www.google.com/search?q=test

# Alternatives
# short options
python src/runcrawler.py -w https://www.google.com/search?q=test -t 50 -d 2


# long options
python src/runcrawler.py --website https://www.google.com/search?q=test --maxTasksPerChild 50 --maxDepth 2
```