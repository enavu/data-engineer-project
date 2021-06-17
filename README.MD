
# Overview

Data used https://s3-us-west-2.amazonaws.com/com.guild.us-west-2.public-data/project-data/the-movies-dataset.zip

The summary of this project was to take the movie data set and understand how the data was generated, perform transformation on cleaned and primed data, and be able to perform analysis on the movies by genre or year but not limited to it.

These are the things that I wished I had time for:

* Input designed so we can list each metric besides genre that are along the lines of: adult, belongs_to_collection, budget, genres, homepage, id, imdb_id, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count. I have implemented it here:  https://github.com/enavu/sdr_avail/blob/main/sdr_availability/input_prompts.py
* logging - more advanced and more warnings/errors
* try catch on being able to connect to the s3 bucket to get 
* convert setup.py to requirements.txt for packaging since legacy style

# Instructions

* Open and unzip project
* cd into root
* run cmd with -e so we don't have to redo instsall, this will use setup.py pip install -e .
* run cmd python app.py
* caveats - need python 3+

```
cd movies_analysis
pip install -e . 
python app.py
```

# Deliverables
There are three goals to this project:
* Design a data model that can be used to answer a series of questions. 
* Implement a program that transforms the input data into a form usable by the data model
* Explain how you would scale this pipeline

The designed data model must be able to at least answer the following questions: 

* Production Company Details:
    * budget per year
    * revenue per year
    * profit per year
    * releases by genre per year
    * average popularity of produced movies per year
    
* Movie Genre Details:
    * most popular genre by year
    * budget by genre by year
    * revenue by genre by year
    * profit by genre by year


## Code 
Clone this repo and provide the final tarball of the finished product. The code should be written in Java or Python
* Code must be runnable - Document how to build/run the code
* Code must solve the problem at hand (this is not supposed to be a big data problem)
* Code must contain SQL query for gathering `Movie Genre Details:revenue by genre by year` with your data model
* Input: should take a s3 endpoint to the file as a positional argument (e.g. `cmd s3://com.guild.us-west-2.public-data/project-data/the-movies-dataset.zip`)
* Output: 
  * Directory of output files of the processed data: logging contains directory, but it is also at movies_analysis/data
  * Error log file:  Please visit logging.ini file for location.

## Data Model

![alt text](https://github.com/enavu/data-engineer-project/blob/master/movies_analysis/images/erdiagram.png)

Please provide a data model that meets the following requirements:
* Modeling these files were based on ids and kaggle documentation and same id names.
* Relational ERD diagram (included relationships) 
* Evolvable for future needs (don’t just aggregate the exact questions): Ran out of time for this - but this is in my to do list, on being able to enhance the requested analytics.

## Design: Scaling and maintain the system.
* Current Pandas switch to pyspark dataframes Job: AWS, Terraform module implementation, lambda, and emr for logging.  - Stack Python, pyspark, and common tools.
![alt text](https://github.com/enavu/data-engineer-project/blob/master/movies_analysis/images/smartflow.png)
* SNS example of emailing team when data thresholds are met
* Utilize systems such as data dog as well for notifications

Other potential designs:

![alt text](https://github.com/enavu/data-engineer-project/blob/master/movies_analysis/images/bigdataanalytics.png)
![alt text](https://github.com/enavu/data-engineer-project/blob/master/movies_analysis/images/datawarehousing.png)
* Data reprocessing:
  * Reprocessing large amount of data usually occurrs after business hours and utilized with spark. We will drop the files into the s3 buckets and make sure we write up a job that takes date ranges or use databricks in AWS to optimize the process.  When jobs are ran with correct spark session configurations this will smoothly reprocess data without memory issues and continue to run smoothly with well written functional coding.  Make sure you have a CI/CD environment to test out your runs prior. 
* What kind of error handling would you put in place?
  * Apply ML for growth of files landed for this set, how often is is growing, what size is it expected, if it falls below the previous file size by % alert team with SNS email
  * Row count, if dat is set into a table - what does the row count look like day over day, if row count dips or is under % - notify team

Sample code for running against any table

```
def check_table_counts(table_dict, spark_session, stop_spark_flag=True):
    """
    @param table_dict: table_dict
    @param spark_session
    @return results: Dictionary with the source counts, encrypted (enc) counts and the results of the test
    """
    source_info = get_table_info(table_dict['source_table'])
    enc_info = get_table_info(table_dict['enc_table'])
    spark = spark_session
    yesterday_date = (table_dict['enc_date'] - dt.timedelta(days = 1))
    sourceCount = spark.sql(f"select count(*) count from {table_dict['source_table']} where {source_info['part_key_names'][0]}='{table_dict['source_date']}'").first()['count']
    tableCount = spark.sql(f"select count(*) count from {table_dict['enc_table']} where {enc_info['part_key_names'][0]}='{table_dict['enc_date']}'").first()['count']
    yesterdayCount = spark.sql(f"select count(*) count from {table_dict['enc_table']} where {enc_info['part_key_names'][0]}='{yesterday_date}'").first()['count']
    print(f"###### Counts are source: {sourceCount} === enc: {tableCount}, yesterday: {yesterdayCount} ######") 
    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq
    }
    if stop_spark_flag:
        spark.stop()
    results = {
        'source_count' : sourceCount,
        'enc_count': tableCount,
        'yesterday' : yesterdayCount,
        'test_result': ops[table_dict['operator']](sourceCount, tableCount)
    }
    return results
```

  * Monitoring: Visualization for operational monitoring - map out raw data and if there is a dip, look into dat. 

Sample visualiation monitoring
![alt text](https://github.com/enavu/data-engineer-project/blob/master/movies_analysis/images/dipnotification.png)
