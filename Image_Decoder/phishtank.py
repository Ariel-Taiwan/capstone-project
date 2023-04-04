import requests
from bs4 import BeautifulSoup

req = requests.get("http://data.phishtank.com/data/online-valid.csv") #將此頁面的HTML GET下來
#print(r.text) #印出HTML

url_content = req.content
csv_file = open('download_phishtank.csv', 'wb')

csv_file.write(url_content)
csv_file.close()
