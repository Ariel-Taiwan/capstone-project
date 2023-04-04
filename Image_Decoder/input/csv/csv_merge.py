import pandas as pd
import os
import sys


def main():
    filepath = os.path.abspath('/home/server/QRcode_Crawler/Image_Decoder/input/csv/')

    argc = len(sys.argv)
    files = []

    for i in range(1, argc):
        files.push(filepath + '/' + sys.argv[i])
    
    df = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
    df.drop_duplicates(subset=["image_name"], inplace=True)
    df.to_csv("/home/server/QRcode_Crawler/Image_Decoder/input/csv/merge.csv", index=False)

if __name__ == "__main__":
    main()