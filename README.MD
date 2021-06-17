
# Overview

Data used https://s3-us-west-2.amazonaws.com/com.guild.us-west-2.public-data/project-data/the-movies-dataset.zip

The summary of this project was to take the movie data set and understand how the data was generated, perform transformation on cleaned and primed data, and be able to perform analysis on the movies by genre or year but not limited to it.

These are the things that I wished I had time for:

* Input designed so we can list each metric besides genre that are along the lines of: adult, belongs_to_collection, budget, genres, homepage, id, imdb_id, original_language, original_title, overview, popularity, poster_path, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count. I have implemented it here:  https://github.com/enavu/sdr_avail/blob/main/sdr_availability/input_prompts.py
* logging
* try catch on being able to connect to the s3 bucket to get 

 
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
  * Directory that contains the output files of the processed data
  * Error log file

## Data Model

![alt text](https://github.com/enavu/data-engineer-project/blob/master/movies_analysis/images/erdiagram.png)

Please provide a data model that meets the following requirements:
* Document describing modeling decisions
* Relational ERD diagram (included relationships) 
* Evolvable for future needs (don’t just aggregate the exact questions) 

## Design
The goal of the design task is to see how you would scale and maintain the system.
* Propose solutions for an 100x increase in data volume, and an hourly update cadence
* Propose ideas for data reprocessing:
  * How would you go about backfilling 1 year worth of data?
  * How would you avoid impact on the production flow (e.g. concurrent job runs)?
* What kind of error handling would you put in place?

Be sure to discuss issues and trade-offs around scaling, monitoring, failure recovery, authentication, etc... 
