import requests
import bs4
from bs4 import BeautifulSoup
import datetime

base_link = "https://finviz.com/quote.ashx?t="

def get_arkg_tickers():
    #this is the link that downloads the csv of the current ARKG holdings
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}
    arkg_holdings_csv = "https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv"
    arkg_holdings = str(requests.get(arkg_holdings_csv, headers=hdr).content).split("ARKG")
    arkg_holdings = arkg_holdings[1:len(arkg_holdings)-1]
    arkg_tickers = []
    arkg_names = []
    for line in arkg_holdings:
        ticker = line.split(",")[2].replace('"',"")
        if ticker.find(" ") != -1:
            ticker = ticker.split(" ")[0]
        if ticker != "":
            arkg_tickers.append(ticker)
            name = line.split(",")[1].replace('"',"")
            name = name.replace(" INC", "")
            name = name.replace(" CORP", "")
            name = name.replace("CLASS-A","")
            name = name.replace("C-A","")    
            name = name.replace("-A","")     
            name = name.replace(" - ADR","")
            name = name.replace(" -CLASS A","")  
            name = name.replace("-SP ADR","")  
            name = name.replace(" AG","")  
            name = name.replace(" - CLASS A","")
            name = name.replace("-CLASS A","")
            arkg_names.append(name)


    tickers = arkg_tickers
    return tickers
