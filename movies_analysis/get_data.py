import pandas as pd
import zipfile
import requests
from io import BytesIO

full_url = " https://s3-us-west-2.amazonaws.com/com.guild.us-west-2.public-data/project-data/the-movies-dataset.zip"

## * Input: should take a s3 endpoint to the file as a positional argument 
def get_data():
    r = requests.get(full_url, allow_redirects=True)
    z = zipfile.ZipFile(BytesIO(r.content))   
    list_of_dfs = {}
    for f in z.namelist():
        list_of_dfs[f.split('.')[0]] = pd.read_csv(z.open(f), sep=",", low_memory=False)      
    return list_of_dfs


## I have used boto3 heavily in my current work with lambda/EMR could probably continue to debug to find issue but aware resources doesnt require credentials 
## resource is not supposed to ask for credentials but it is.
# ##botocore.exceptions.NoCredentialsError: Unable to locate credentials
#def download_s3_file():
    # bucket_name = "com.guild.us-west-2.public-data"
    # prefix = "project-data"
    # files = 'project-data/the-movies-dataset.zip'
    # object_name ='the-movies-dataset'
    # file_name = 'the-movies-dataset.zip'
    # s3 = boto3.resource('s3')
    # s3client = boto3.client('s3', region_name='us-west-2')
    # objects = s3client.list_objects(Bucket=bucket_name)
    #s3 = boto3.resource('s3')
    #my_bucket = s3.Bucket(bucket_name)
    #my_bucket.download_file(files, 'the-movies-dataset.zip')