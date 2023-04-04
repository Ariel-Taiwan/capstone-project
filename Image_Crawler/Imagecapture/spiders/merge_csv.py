import pandas as pd
from glob import glob
 
files = ['third_cat7_record3.csv','third_cat7_record2.csv']
  
df = pd.concat((pd.read_csv(file, usecols=['category','image_name','image_urls','indomain','layer','relative_path'], dtype={'category': str ,'image_name': str ,'image_urls': str ,'indomain': str ,'layer': str ,'relative_path': str}) for file in files), ignore_index=True)
print(df)

print(df.head(40))
df.to_csv('third_cat7_record.csv')
