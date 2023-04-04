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

    # Input image and .csv directory
    input_images_directory = os.path.abspath("/home/server/QRcode_Crawler/Image_Crawler/Imagecapture/spiders/output/images") + '/' + sys.argv[1]
    input_images_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Image_Decoder/input") + '/' + sys.argv[2] 
    
    # Output .csv directory
    output_list_directory = os.path.abspath("/home/server/QRcode_Crawler/Image_Decoder/result") + '/' + sys.argv[3] 

    # Read a image info
    col_list = ["category", "image_name", "image_urls", "indomain", "layer", "relative_path"] 
    df = pd.read_csv(input_images_list_directory, usecols = col_list, encoding = 'unicode_escape')
        
    # Create a new df
    output_col = ["layer","category", "indomain", "image_name", "decode_url", "image_urls"]
    output_df = pd.DataFrame(columns = output_col)

    readable_images = 0
    QRcode_images = 0
    total_decode_QRcode = 0

    QRcode_list = []

    # Parse each row on the input .csv
    for i in df.index:
        filename = df["image_name"][i]
        file_ext = filename.split('.')
        file_ext = ((file_ext[len(file_ext) - 1].split('?'))[0]).split('&')[0]
        full_filename =  input_images_directory + filename
        print(filename)

        # Convert .svg to .png
        if file_ext == "svg":
            filename = filename.replace("svg", "png")
            new_full_filename = "./img/svg_to_png/" + filename
           
            try:
                cairosvg.svg2png(url=full_filename, write_to=new_full_filename)
            except Exception as e:
                print(e)
                continue
            else:
                full_filename = new_full_filename
           

        # Read the QRcode image
        try:
            image = Image.open(full_filename)
        except (OSError, EOFError):
            pass
        except Exception as e:
            print(e)
        else:
            readable_images += 1
            res = decode(image)
            print(image)

            # Decode Successfully
            if res != []:
                QRcode_images += 1
                decode_url = ""

                for item in res:
                    # Insert a new row to output file ["layer","category", "image_name", "decode_url", "image_urls", "indomain"]
                    total_decode_QRcode += 1
                    decode_url = item.data.decode("utf-8")
                    QRcode_list.append([df["layer"][i], df["category"][i], df["indomain"][i], df["image_name"][i], decode_url, df["image_urls"][i]])
                    
    output_df = pd.DataFrame(QRcode_list, columns = output_col)

    # Write results to output .csv
    output_df.to_csv(output_list_directory, index=False)    
    
    # Convert dataframe to dictionary
    bulk_data = output_df.to_dict('records')
    
    # MongoDB info
    mongodb_uri = "mongodb://localhost:27014"
    mongodb_db = "research"
    mongodb_collection = "parse"

    # Connect and open MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_db]
    collection = db[mongodb_collection]

    print(bulk_data)

    if bulk_data != []:
        try:
            collection.insert_many(bulk_data, ordered=False)
        except Exception as e:
            print(e)
    
    # Write data to .txt
    f = open("./result/analyze.txt", 'a')
    print(sys.argv[3], file=f)
    print("Readable / QRcode / total_QRcode: " + str(readable_images) + " / " + str(QRcode_images) + " / " + str(total_decode_QRcode), file=f)
    print("---------------------------------", file=f)
    f.close()


if __name__ == "__main__":
    main()
