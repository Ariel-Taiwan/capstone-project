import os
import pandas as pd
import sys
import pymongo
import requests
import validators

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

def main():

    input_urls_directory = os.path.abspath("/home/server/QRcode_Crawler/unshortenurl/input/" + sys.argv[1])
    input_col = ["Datetime","Tag", "Tweet_id", "image_name", "image_urls", "decode_url"]
    df = pd.read_csv(input_urls_directory, usecols = input_col, encoding= 'unicode_escape')

    # Initialize the parameters
    total_decode_QRcode = df.shape[0]
    valid_url = 0
    is_phishingqr = 0
    not_phishingqr = 0
    shorturl = 0
    phishing_shorturl = 0
    phishing_list = []
    exist = 0
    unshorten_fail = 0

    # MongoDB info
    mongodb_uri = "mongodb://localhost:27014"
    mongodb_db = "research"
    mongodb_collection = "Blocklist_v2"

    # Connect and open MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_db]
    collection = db[mongodb_collection]

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Parse each row on the input .csv
    for i in df.index:
        if type(df["decode_url"][i]) is str:
            RAW_URL = df["decode_url"][i]
            INITIAL_URL = addHTTP(RAW_URL)
            url = INITIAL_URL

            # Skip if it's not a url
            if validators.url(INITIAL_URL) != True:
                continue

            is_shorturl = False
            is_exist = False
            origin_domain = getDomain(INITIAL_URL)

            # Check if it's a short url
            if isShorturl(origin_domain) == True:
                is_shorturl = True
                shorturl += 1

                # Unshorten url by sending a GET request
                res = GetRequest(INITIAL_URL)
                unshorten_url = res["url"]
                is_exist = res["is_exist"]

                # Decode fails, use Ushorten.it to decode
                if INITIAL_URL == unshorten_url and unshorten_url != None or unshorten_url == None:
                    unshorten_url = unshorten(driver, INITIAL_URL)

                    if INITIAL_URL == unshorten_url:
                        unshorten_fail += 1
                    
                unshorten_domain = getDomain(unshorten_url)
    
                # print(url)
                
            # Check if it's phishing by a unshorten url
            no_protocol_url = removeProtocol(url)

            if is_shorturl == False:
                query = {"$or": [{"url": no_protocol_url}, {"url": addHTTP(no_protocol_url)},  {"url": addHTTPS(no_protocol_url)}, {"url": origin_domain}]}
            else:
                no_protocol_unshorten_url = removeProtocol(unshorten_url)
                query = {"$or": [{"url": no_protocol_url}, {"url": addHTTP(no_protocol_url)}, {"url": addHTTPS(no_protocol_url)}, {"url": origin_domain}, {"url": no_protocol_unshorten_url}, {"url": addHTTP(no_protocol_unshorten_url)}, {"url": addHTTPS(no_protocol_unshorten_url)}, {"url": unshorten_domain}]}
            query_res = collection.find_one(query)

            if query_res is not None:
                is_phishingqr += 1

                # Check if the phishing page still exists 
                if is_shorturl == True:
                    phishing_shorturl += 1
                else:
                    res = GetRequest(url)
                    is_exist = res["is_exist"]

                if is_exist == True:
                    exist += 1

                phishing_list.append([is_exist, is_shorturl, df["Datetime"][i], df["Tag"][i], df["Tweet_id"][i], df["image_name"][i], df["decode_url"][i], url, df["image_urls"][i]])

            else:
                not_phishingqr += 1

    # Write results to output .csv
    output_col = ["exist", "shorturl", "Datetime", "Tag", "Tweet_id", "image_name", "decode_url", "unshorten_url", "image_urls"]
    output_list_directory = os.path.abspath("./output/csv/v2/" + sys.argv[2])
    output_df = pd.DataFrame(phishing_list, columns = output_col)
    output_df.to_csv(output_list_directory, index=False)    
    valid_url = is_phishingqr + not_phishingqr

    # Write data to .txt
    f = open("./output/phishing_result_unshorten_v2.txt", 'a')
    print(sys.argv[1], file=f)
    print("total_QRcode / Valid_URL / is_phishing_QRcode / not_phishing_QRcode: " + str(total_decode_QRcode) + " / " + str(valid_url) + " / " + str(is_phishingqr) + " / " + str(not_phishingqr), file=f)
    print("ShortUrl / Unshorten_fail / Phishing_shorturl: " + str(shorturl) + " / " + str(unshorten_fail) + " / " + str(phishing_shorturl), file=f)   
    #print("Phishing_Indomain / Phishing_Outdomain: " + str(indomain) + " / " + str(outdomain), file=f)
    print("Phishing_Exist: " + str(exist), file=f)
    print("---------------------------------", file=f)
    f.close()

def addHTTP(url):
    if url.startswith("http") == False:
        url = "http://" + url
    return url   

def addHTTPS(url):
    if url.startswith("https") == False:
        url = "https://" + url
    return url   

def GetRequest(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        res = requests.get(url, headers=headers, allow_redirects=True, timeout=5)   
    except Exception as e:
        print(e)
        return { "url": None, "is_exist": False }
    else:
        if res.status_code == 404:
            return { "url": res.url, "is_exist": False }
        else:
            return { "url": res.url, "is_exist": True }


def unshorten(driver, input_url):
    
    #the web that helps us to unshorten our url
    driver.get("https://unshorten.it/")

    #locating element in html
    element = driver.find_element(By.ID, "short-url")
    
    #type in the shorten url that want to expand
    element.send_keys(input_url)

    button = driver.find_element(By.ID, "unshorten-button")
    button.submit()

    time.sleep(6)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    url = soup.find('p',{'class':"data"})

    return url.string

def isShorturl(domain):
    shorturl_domain = { "forms.gle", "reurl.cc", "bit.ly", "rebrand.ly", "tinyurl.com", "tiny.cc", "ppt.cc", "risu.io", "www.shorturl.at", "offf.to", "supr.link", "s.yam.com", "is.gd", "rb.gy", "cutt.ly", "shycmedi.com", "yt2.piee.pw",  "0rz.tw", "t.ly"}

    if domain in shorturl_domain:
        return True
    else:
        return False

def getDomain(url):
    request_url = url.split('/')
    domain = ''
    
    # If it is regular url, return domain
    if url.startswith("http"):
        domain = request_url[2]
    elif len(request_url) >= 2:
        domain = request_url[0]

    return domain

def removeProtocol(url):
    if url.startswith("https"):
        url = url[8:]
    elif url.startswith("http"):
        url = url[7:]
    
    return url

if __name__ == "__main__":
    main()
