# Import Library
import sys
import os
import pandas as pd

def main():

    # Input .csv directory
    input_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Phishing_Detect/input/") + '/' + sys.argv[1] 
    
    # Output .csv directory
    output_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Phishing_Detect/output/") + '/' + sys.argv[2] 

    # Read a image info category,indomain,layer,urls
    col_list = ["indomain"] 
    df = pd.read_csv(input_list_directory, usecols = col_list, encoding = 'unicode_escape')
 
    indomain = 0
    outdomain = 0

    # Parse each row on the input .csv
    for i in df.index:
        if df["indomain"][i] == 1:
            indomain += 1
        else:
            outdomain += 1

    total = indomain + outdomain

    f = open(output_list_directory, 'a')

    print(sys.argv[1], file=f)
    print("Total / Indomain / Outdomain : " + str(total) + " / " + str(indomain) + " / " + str(outdomain), file=f)
    print("----------------------------------------------", file=f)

    f.close()

if __name__ == "__main__":
    main()