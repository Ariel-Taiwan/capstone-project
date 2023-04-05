This section introduce how to use data_crawler.py
You can crawler tweets by a tag and decide the amount of data you want to download

python3 data_crawler.py <tag> <amount of data> <output_filename>

e.g. python3 data_crawler.py bitcoin 100 bitcoin_out.csv


# This section introduce how to use csv_merge.py
You can merge all csv file in ./output/csv

1. Put files in ./output/csv
2. Execute csv_merge.py => python3 csv_merge.py
3. Generate a output merge csv file named merge.csv
