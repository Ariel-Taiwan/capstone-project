import wget
import os
import sys
import pandas as pd


def main():
    # Input .csv directory
    input_images_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Image_Decoder/input/csv") + '/' + sys.argv[1] 

    # Output image and .csv directory
    output_images_directory = os.path.abspath("/home/server/QRcode_Crawler/Image_Decoder/input/images") + '/' + sys.argv[2]
    output_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Image_Decoder/input/csv") + '/' + sys.argv[3] 

    # Create a output directory if it is not exist
    if not os.path.exists(output_images_directory):
        try:
            os.makedirs(output_images_directory)
        except Exception as e:
            print(e)
            raise

    # Read a image info
    col_list = ["category", "image_name", "image_urls", "indomain", "layer", "relative_path"] 
    df = pd.read_csv(input_images_list_directory, usecols = col_list, encoding = 'unicode_escape')

    download_list = []

    # Parse each row on the input .csv
    for i in df.index:
        try:
            filename = wget.download(df["image_urls"][i], out=output_images_directory)
        except:
            pass
        else:
            filename = filename.split('/')
            download_list.append([df["category"][i], filename[len(filename) - 1], df["image_urls"][i], df["indomain"][i], df["layer"][i], df["relative_path"][i]])

    output_df = pd.DataFrame(download_list, columns = col_list)

    # Write results to output .csv
    output_df.to_csv(output_list_directory, index=False) 

if __name__ == "__main__":
    main()