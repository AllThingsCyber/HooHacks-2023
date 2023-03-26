import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def insider_trades(s, ticker, exchange):
    url = "https://www.marketbeat.com/stocks/%s/%s/insider-trades/" % (exchange, ticker)
    r = s.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        NA = soup.find_all(string = re.compile("insiders have not sold"), limit=1)
        if NA:
            print("No insider transactions detected.")
            return pe_ratio(s, ticker, exchange)

        sells = soup.find_all(string = re.compile("Insiders have sold"), limit=1) 
        if sells:
            print(sells)
        else:
            print("There has been no insider selling within the past 24 months.")


        buys = soup.find_all(string = re.compile("Insiders have purchased"), limit=1)
        if buys:
            print(buys)
        else:
            print("There has been no insider buying in the past 24 months.")
    else:
        sys.exit(-2)
                         
def pe_ratio(s, ticker, exchange): 
    url = "https://www.marketbeat.com/stocks/%s/%s/" % (exchange, ticker)
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    pe = soup.find_all(string = re.compile("The P/E"), limit=1)
    if pe:
        print(pe)
    else:
        pe_check_2 = soup.find_all(string = re.compile("P/E Ratio"), limit=1)
        if pe_check_2:
            print(pe_check_2)

def revenue(s, ticker, exchange):
    url =  "https://www.marketbeat.com/stocks/%s/%s/" % (exchange, ticker)
    r = s.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        tags = soup.find_all('div', {'class': "price-data"})
        top_list = []
        for i in range(1,len(tags)+1):
            news = tags[i-1].text
            
            top_list.append(news)
            print("INFO: " +str(i)+ ":" + news)



def main():
    if len(sys.argv) != 3:
        print("(-) Usage: python scraper.py <Stock Ticker Here> <Stock Exchange Here>")
        print("(-) Example: python scrapyer.py CACI NASDAQ")
        sys.exit(-1)
    
    s = requests.Session()
    ticker = sys.argv[1]
    exchange = sys.argv[2]
    insider_trades(s, ticker, exchange)
    pe_ratio(s, ticker, exchange)
    revenue(s, ticker, exchange)

if __name__ == '__main__':
    main()