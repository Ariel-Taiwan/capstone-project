from glob import glob
import pandas as pd

files = glob('/home/server/QRcode_Crawler/Twitter_Crawler/output/csv/v2/*.csv')
 
df = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
df.drop_duplicates(subset=["Tweet_id", "image_urls"], inplace=True)
df.to_csv("/home/server/QRcode_Crawler/Twitter_Crawler/output/csv/v2/merge.csv", index=False)