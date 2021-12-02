from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

path = 'C:/Users/user/Documents/tickers.xlsx'

chromedriver = 'C:\\Users\\user\\Downloads\\chromedriver_win32\\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

df = pd.read_excel(path, sheet_name=0)
data=df["ticker"].tolist()

for item in data:
    browser.get('https://duckduckgo.com/')
    search_box= WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
    search_box.send_keys('region:us site:https://www.bloomberg.com/ inurl:'+item+':US "www."')
    search_box.submit()
    results = browser.find_elements_by_xpath("//div[@id='links']/div/div/h2/a[@class='result__a']")
    results3 = browser.find_elements_by_xpath("//div[@id='links']/div/div/div[1]/div/a/span[2]")
    lists = ['companies/' + item + ':US', 'companies/' + item + '/A:US','quote/' + item + ':US', 'quote/' + item + '/A:US','company/' + 

item + ':US', 'company/' + item + '/A:US']

    try:
        results2 = WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@id='links']/div/div/div[2]")))
        urls = []
        description = []

    except Exception:
        print(item +": no website showed up search in results")
        continue

    for result in results:
        urls.append(result.get_attribute("href"))
        iterate = len(urls)

    counter=0

    for i in range(0,iterate):
        u = results3[i].text

        if any(x in u for x in lists):
            s = str(results2[i].text)
            start = s.find('www.')
            s= s[start:]
            end = s.find(' ')
            s= s[:end]
            urls1=urls[i]
            counter += 1

            if s.endswith('.'):
                s=s[:-1]

            if '/' in s:
                end = s.find('/')
                s= s[:end]

            if item+":US" in urls1:
                breaker=True
                print(item + ":" + s)
                break

            description.append(s)
            description=list(set(description))

    if breaker:
        continue

    if counter == 0:
        print(item +": search results did not find any relevant result(s)")
        continue

    if description==['']:
        print(item +": relevant result(s) found but company website not found/listed")
        continue

    description = ''.join(description)
    description = description.replace("['","")
    description = description.replace("']","")
    print(item +":"+description)
