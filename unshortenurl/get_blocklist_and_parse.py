# Import Library
import sys
import os
import pandas as pd
import pymongo
import wget


def main():
    
    # Download blocklist from https://phishing.army/download/phishing_army_blocklist_extended.txt
    # Original project from https://phishing.army/index.html
    try:    
        Phishing_Army_filename = wget.download("https://phishing.army/download/phishing_army_blocklist_extended.txt", out="phishing_army_blocklist_extended.txt")
        Phishtank_filename = wget.download("http://data.phishtank.com/data/online-valid.csv", out="phishtank_blocklist.csv")
    except Exception as e:
        print(e)
    else:
        Phishing_Army_list = []

        # Read a Phishing Army blocklist
        f = open(Phishing_Army_filename, 'r')

        # Parse blocklist file
        for line in f.readlines():
            if line[0] != '#' and line[0] != '\n':
                url = line.strip()
                Phishing_Army_list.append(url)

        f.close()

        # Read a Phishtank blocklist
        df = pd.read_csv(Phishtank_filename, usecols = ["url"], encoding= 'unicode_escape')
        Phishtank_list = df['url'].tolist()
        Phishtank_list_new = []

        # Extract domains from urls
        for line in Phishtank_list:
            Phishtank_list_new.append(line)


        # Combine two blocklist
        block_list = Phishing_Army_list + Phishtank_list_new

        # Remove duplicated urls
        block_list =  list(set(block_list))

        # Convert list to dataframe
        output_df = pd.DataFrame(block_list, columns = ["url"]) 
        
        # Convert dataframe to dictionary
        bulk_data = output_df.to_dict('records')

        # MongoDB info
        mongodb_uri = "mongodb://localhost:27014"
        mongodb_db = "research"
        mongodb_collection = "Blocklist_v2"

        # Connect and open MongoDB
        client = pymongo.MongoClient(mongodb_uri)
        db = client[mongodb_db]
        collection = db[mongodb_collection]
        collection.create_index('url', unique = True)

        if bulk_data != []:
            try:
                collection.insert_many(bulk_data, ordered=False)
            except Exception as e:
                print(e)

def getDomain(url):
    request_url = url.split('/')
    domain = ''
    
    # If it is regular url, return domain
    if url.startswith("http"):
        domain = request_url[2]
    elif len(request_url) >= 2:
        domain = request_url[0]

    return domain


if __name__ == "__main__":
    main()