# How to get blocklist
You can use get_blocklist_and_parse.py to download blocklist from https://phishing.army/download/phishing_army_blocklist_extended.txt.
Original project from https://phishing.army/index.html.

Usage: python3 get_blocklist_and_parse.py 

# How to check phishing
<1> You can just run run_phishing_check.sh to check csv files listed in run_phishing_check.sh
Usage: ./run_phishing_check.sh

<2> Or check the specific csv file
Usage: python3 check_phishing.py <input csv filename>
e.g. python3 check_phishing.py second_cat1_parse.csv