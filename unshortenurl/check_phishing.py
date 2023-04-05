import os
import pandas as pd
import sys
import pymongo
# -*- coding: UTF-8 -*-


def main():

    start_urls = []
    input_urls_directory = os.path.abspath("/home/server/QRcode_Crawler/Phishing_Detect/input/" + sys.argv[1])

    # Read a URL file
    df = pd.read_csv(input_urls_directory, usecols = ["decode_url"], encoding= 'unicode_escape')
    
    start_urls = df["decode_url"].tolist()
    filtered_start_urls = list(filter(lambda i:type(i) is str, start_urls))

    total_decode_QRcode = df.shape[0]
    is_phishingqr = 0
    not_phishingqr = 0

    # MongoDB info
    mongodb_uri = "mongodb://localhost:27014"
    mongodb_db = "research"
    mongodb_collection = "Blocklist"

    # Connect and open MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_db]
    collection = db[mongodb_collection]

    for url in filtered_start_urls:
        test_domain = getDomain(url)
        domain_query = { "url": test_domain }

        domain_res = collection.find_one(domain_query)

        if domain_res is not None:
            is_phishingqr += 1
        else:
            not_phishingqr += 1

    # Write data to .txt
    f = open("./output/phishing_result.txt", 'a')
    print(sys.argv[1], file=f)
    print("total_QRcode / is_phishing_QRcode / not_phishing_QRcode: " + str(total_decode_QRcode) + " / " + str(is_phishingqr) + " / " + str(not_phishingqr), file=f)
    print("---------------------------------", file=f)
    f.close()

def getDomain(url):
    request_url = url.split('/')
    domain = ''
    
    # If it is regular url, return domain
    if len(request_url) >= 3:
        domain = request_url[2]
    
    return domain


if __name__ == "__main__":
    main()