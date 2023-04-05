from cgi import test
import os
from socket import timeout
from textwrap import shorten
import pandas as pd
import sys
import pymongo
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

#exist = 0
def main():

    input_urls_directory = os.path.abspath("/home/server/QRcode_Crawler/Phishing_Detect/input/" + sys.argv[1])
    input_col = ["Datetime","Tag", "Tweet_id", "image_name", "image_urls", "decode_url"]
    df = pd.read_csv(input_urls_directory, usecols = input_col, encoding= 'unicode_escape')

    # Initialize the parameters
    total_decode_QRcode = df.shape[0]
    is_phishingqr = 0
    not_phishingqr = 0
    indomain = 0
    outdomain = 0
    shorturl = 0
    phishing_shorturl = 0
    phishing_list = []
    exist = 0
    bo = False
    unshorten_fail = 0
    flag = 0

    # MongoDB info
    mongodb_uri = "mongodb://localhost:27014"
    mongodb_db = "research"
    mongodb_collection = "Blocklist"

    # Connect and open MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_db]
    collection = db[mongodb_collection]
    
    is_phishing = 'This link has been flagged as redirecting to malicious or spam content.'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Parse each row on the input .csv
    for i in df.index:
        if type(df["decode_url"][i]) is str:
            is_shorturl = False
            is_exist = False
            url =  df["decode_url"][i]
            test_domain = getDomain(url)

            # Skip if it's not a url
            if test_domain == '':
                not_phishingqr += 1
            else:
                # Check if it's a short url
                if isShorturl(test_domain) == True:
                    print("here4")
                    is_shorturl = True
                    shorturl += 1
                    orgin_url = url
                    """if getDomain(url) == 'bit.ly':
                        url_for_bit = url + '+'
                        try:
                            #print("here11")
                            a = requests.get(url_for_bit, headers=headers, allow_redirects=True, timeout=5)
                            time.sleep(1)
                        except  Exception as e:
                            print(e)
                            #print("here12")
                            url_for_bit = addHTTP(url_for_bit)
                            try:
                                #print("here13")
                                a = requests.get(url_for_bit, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=True, timeout=5)
                                #print("here131")
                                time.sleep(1)
                            except  Exception as e:
                                #print("here132")
                                print(e)
                                #print("here14")

                        print("Original URL is: {}".format(url))
                        if a.text.find(is_phishing) > 0:
                            #print("here15")
                            is_phishingqr += 1
                            phishing_shorturl += 1
                            bo = Check_phishing_page_exists(url)
                            if bo == True:
                                exist += 1
                            phishing_list.append([is_exist, is_shorturl, df["Datetime"][i], df["Tag"][i], df["Tweet_id"][i], df["image_name"][i], df["decode_url"][i], url, df["image_urls"][i]])
                        else:
                            print("here16")
                            not_phishingqr += 1
                    else:
                    """
                    try:
                        request_res = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
                        time.sleep(1)
                        a = url
                    except  Exception as e:
                        print(e)
                        flag = 1
                        url = addHTTP(url)
                        try:
                            a = requests.get(url, headers=headers, allow_redirects=True, timeout=5).url
                            time.sleep(1)
                        except  Exception as e:
                            print(e)

                    if request_res.url == url or a == url:
                        #print("here22")
                        driver.get("https://unshorten.it/")
                        email = driver.find_element(By.ID, "short-url")
                        email.send_keys(url)
                        button = driver.find_element(By.ID, "unshorten-button")
                        button.submit()
                        time.sleep(5)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        url = soup.find('p',{'class':"data"}).text
                        print("selenium: " + url)
                    else:
                        print("here23")
                        if flag == 1:
                            url = a
                        url = request_res.url
                        
                    print("here24")
                    no_protocol_url = removeProtocol(url)
                    query = {"$or": [{"url": no_protocol_url}, {"url": addHTTP(no_protocol_url)},  {"url": addHTTPS(no_protocol_url)}, {"url": test_domain}]}
                    query_res = collection.find_one(query)
                    print("here25")
                    if query_res is not None:
                        print("here26")
                        is_phishingqr += 1
                        phishing_shorturl += 1

                        bo = Check_phishing_page_exists(url)
                        if bo == True:
                            exist += 1
                        print("here27")
                        phishing_list.append([is_exist, is_shorturl, df["Datetime"][i], df["Tag"][i], df["Tweet_id"][i], df["image_name"][i], df["decode_url"][i], url, df["image_urls"][i]])
                    else:
                        not_phishingqr += 1
                    print("here5")
                else:
                    no_protocol_url = removeProtocol(url)
                    query = {"$or": [{"url": no_protocol_url}, {"url": addHTTP(no_protocol_url)},  {"url": addHTTPS(no_protocol_url)}, {"url": test_domain}]}
                    query_res = collection.find_one(query)
                    if query_res is not None:
                        is_phishingqr += 1
                        
                        bo = Check_phishing_page_exists(url)
                        if bo == True:
                            exist += 1
                        phishing_list.append([is_exist, is_shorturl, df["Datetime"][i], df["Tag"][i], df["Tweet_id"][i], df["image_name"][i], df["decode_url"][i], url, df["image_urls"][i]])
                    else:
                        not_phishingqr += 1

    # Write results to output .csv
    output_col = ["exist", "shorturl", "Datetime", "Tag", "Tweet_id", "image_name", "decode_url", "unshorten_url", "image_urls"]
    file_name = 'test_' + sys.argv[1]
    output_list_directory = os.path.abspath("./output/csv/" + file_name)
    output_df = pd.DataFrame(phishing_list, columns = output_col)
    output_df.to_csv(output_list_directory, index=False)    
    print("csv done")

    # Write data to .txt
    f = open("./output/phishing_result_unshorten_test.txt", 'w')
    f.write(file_name + '\n')
    f.write("total_QRcode / is_phishing_QRcode / not_phishing_QRcode: " + str(total_decode_QRcode) + " / " + str(is_phishingqr) + " / " + str(not_phishingqr) + '\n')
    f.write("ShortUrl / Unshorten_fail / Phishing_shorturl: " + str(shorturl) + " / " + str(unshorten_fail) + " / " + str(phishing_shorturl) + '\n')   
    #print("Phishing_Indomain / Phishing_Outdomain: " + str(indomain) + " / " + str(outdomain), file=f)
    f.write("Phishing_Exist: " + str(exist) + '\n')
    f.write("---------------------------------" + '\n')
    f.close()

def addHTTP(url):
    if url.startswith("http") == False:
        url = "http://" + url
    return url
def addHTTPS(url):
    if url.startswith("https") == False:
        url = "https://" + url
    return url
def Check_phishing_page_exists(url):
    # Check if the phishing page still exists 
    is_exist = False
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        request_res = requests.get(addHTTP(url), headers=headers, allow_redirects=True, timeout=5)
    except Exception as e:
        print(e)
    else:
        # print("url=" + df["decode_url"][i] + " status code=" + str(request_res.status_code))
        if request_res.status_code != 404:
            is_exist = True
    return is_exist
    
def addHTTP(url):
    if url.startswith("http") == False:
        url = "http://" + url
    return url   

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
    shorturl_domain = { "forms.gle", "reurl.cc", "bit.ly", "rebrand.ly", "tinyurl.com", "tiny.cc", "ppt.cc", "risu.io", "www.shorturl.at", "offf.to", "supr.link", "s.yam.com", "is.gd", "rb.gy", "cutt.ly", "shycmedi.com", "yt1.piee.pw",  "0rz.tw", "t.ly"}

    if domain in shorturl_domain:
        return True
    else:
        return False

def getDomain(url):
    request_url = url.split('/')
    domain = ''
    
    # If it is regular url, return domain
    if url.startswith("http"):
        try:
            domain = request_url[2]
        except  Exception as e:
            print(e)
    elif len(request_url) >= 2:
        try:
            domain = request_url[0]
        except  Exception as e:
            print(e)

    return domain

def removeProtocol(url):
    if url.startswith("https"):
        url = url[8:]
    elif url.startswith("http"):
        url = url[7:]
    
    return url

if __name__ == "__main__":
    main()

