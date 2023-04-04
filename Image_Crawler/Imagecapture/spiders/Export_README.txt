# Export data from MongoDB command 
* Reference from https://www.mongodb.com/docs/database-tools/mongoexport/#cmdoption-out

1. Enter docker scrapy-mongodb container
    sudo docker exec -it scrapy-mongodb bash

2. Export data from MongoDB
    mongoexport --collection=<collection_name> --db=research --type=csv --out=<output_dir> -q='<query_string>' --fields=<field1,field2,...>
    
    The following command export test.csv from collection of image on research database to conatiner root directory
    Data on the test.csv are category 1 and at layer 0
    e.g. mongoexport --collection=images --db=research --type=csv --out=test.csv -q='{"layer":"0", "category":"1"}' --fields category,image_name,image_urls,indomain,layer,relative_path

3. Copy .csv file in conatiner to the host
    docker cp  <container_id>:<container_file_dir> <copy_to_local_dir>

    The following command copy from /test.csv in 9d0201db6422 to /home/server/ in the host
    e.g. sudo docker cp f7800775bdd9:/test.csv /home/server/