# Import Library
import sys
import os
import pandas as pd
import pymongo
import cairosvg
from PIL import Image
from pyzbar.pyzbar import decode
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def main():
    # Input .csv directory
    input_images_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Twitter_Crawler/output/csv/v2") + '/' + sys.argv[1] 
    
    # Output .csv directory
    output_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Twitter_Crawler/output/csv/v2") + '/' + sys.argv[2] 

    # The delete tempates 
    delete_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Twitter_Crawler/output/csv/v2/tmp") + '/' + sys.argv[3] 

    # Read a image info
    col_list = ["Datetime", "Main_Tag", "hashtags", "Tweet_id", "image_urls"]
    df = pd.read_csv(input_images_list_directory, usecols = col_list, encoding = 'unicode_escape')

    # Read a delete info
    delete_df = pd.read_csv(delete_list_directory, usecols = col_list, encoding = 'unicode_escape')

    # Convert a delete list to a set
    delete_set = set()

    for i in delete_df.index:
        delete_set.add((delete_df["Tweet_id"][i], delete_df["image_urls"][i]))

    # Parse each row on the input .csv
    list = []

    for i in df.index:
        if (df["Tweet_id"][i], df["image_urls"][i]) not in delete_set:
            list.append([df["Datetime"][i], df["Main_Tag"][i], df["hashtags"][i], df["Tweet_id"][i], df["image_urls"][i]])
          
    output_df = pd.DataFrame(list, columns = col_list)

    # Write results to output .csv
    output_df.to_csv(output_list_directory, index=False)    



if __name__ == "__main__":
    main()
