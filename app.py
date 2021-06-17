from movies_analysis import *
import pandas as pd 
import logging.config

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

## TODO ##
### Request the user to select a data set - currently only care about movies set
### Generate list of availabilities but only display movies - designed 
### Then display columns of movies to see which company details they are interested in
### Movie Genre Details
### Improve with options of other columns as well
### >>> list_of_dfs['movies_metadata'].columns
# Index(['adult', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id',
#        'imdb_id', 'original_language', 'original_title', 'overview',
#        'popularity', 'poster_path', 'production_companies',
#        'production_countries', 'release_date', 'revenue', 'runtime',
#        'spoken_languages', 'status', 'tagline', 'title', 'video',
#        'vote_average', 'vote_count'],

logging.info('We will be running Company Details')

data = manipData()

companyDetails(data)

movieGenreDetails(data)