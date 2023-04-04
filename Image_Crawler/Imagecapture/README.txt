# Setting image output directory !! Most Important !!
Please modify FILES_STORE in settings.py

FILES_STORE = '/home/server/QRcode_Crawler/Image_Crawler/Imagecapture/spiders/output/images/catX'

* catX: X can be 1~7
e.g. If you want to generate category 1 image, please modify FILES_STORE like the below
FILES_STORE = '/home/server/QRcode_Crawler/Image_Crawler/Imagecapture/spiders/output/images/cat1'


# Crwal links and generate results
scrapy crawl example -a input=<input_name.csv> -a MONGODB_URI=<Mongodb_URL> -a MONGODB_DATABASE=<DATABASE_NAME> -a layer=<Layer> -a category=<category_No> -O <output_name.csv>

e.g. input: root_cat1.csv, output: root_cat1_record.csv, MONGODB_URI: mongodb://localhost:27014, MONGODB_DATABASE: research, layer: 0, category: 1
scrapy crawl example -a input=root_cat1.csv -a MONGODB_URI="mongodb://localhost:27014" -a MONGODB_DATABASE="research" -a layer=0 -a category=1 -O root_cat1_record.csv
