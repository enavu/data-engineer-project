import pandas as pd
import datetime as dt
from .get_data import *
import pandasql as ps

def manipData():
    dfs = get_data()
    list_of_df = list(dfs.keys())
    interested_set = ['movies_metadata']
    insterested_details = ['release_date','genres','budget']
    movies = dfs["{}".format(interested_set[0])]
    ## Create a year for Movie Genre details
    movies['year'] = pd.to_datetime(movies['release_date'],format='%Y-%m-%d',  errors='coerce').dt.to_period('Y')
    ## Scrubbing/forcing float and ignore bad data data as data set - can automate this by generating list of errors
    # better way is to identify why jpgs are showing in some budget columns and fix the dilimeters
    movies['revenue'].fillna(0)
    movies['budget'].fillna(0)
    movies['budget'] = pd.to_numeric(movies['budget'], errors='coerce').astype(float)
    movies['popularity'] = pd.to_numeric(movies['popularity'], errors='coerce').astype(float)
    ##Assuming to calculate the profit - we subtrat budget to revenue
    movies['profit'] = movies['revenue'] - movies['budget']
    return movies

###Request
def companyDetails():
    print("###############Getting zip from s3 bucket with request, unzipping and setting 6 files to list of dataframes ######")
    movies = manipData()
    
    ##budget/revenue/profit/average popularity
    ## exmaple in python
    function_dict = {"budget": "sum", "revenue": "sum", "profit": "sum", "popularity" : "mean"}
    ##, "revenue": "sum", "profit": "sum", "popularity" : "mean"}
    grouped_df = movies.groupby("year").aggregate(function_dict)
    
    ##pandas to csv
    grouped_df.to_csv("movies_analysis/data/company_details.csv", index=False)

def movieGenreDetails():
    print("###############Getting zip from s3 bucket with request, unzipping and setting 6 files to list of dataframes ######")
    movies = manipData()
    ##transforming and designing data 
    movies['year'] = movies['year'].astype(str)
    ## Two issues to correct to be able to apply explode and pd.series
    ## One column has an extra text of GATORADE and some columns have empty lists.
    ## Remove the column that contains Gatorade - as I dont trust that data
    movies[movies['genres'].str.contains('GATORADE')].index
    movies = movies.drop(movies[movies['genres'].str.contains('GATORADE')].index)
    
    ## Remove any strings that are = 2/ empty list
    movies = movies[movies['genres'].str.len() != 2]
    
    ##apply eval to conver back to list of dictionaries
    movies['genres'] = movies.genres.apply(eval)

    ## Use explode to expand, transform dictionaries - one dictionary in each row
    movies = movies.explode('genres')
    
    ## Convert the key-values into separate columns, clean up genres or leave to evaluate
    movies[['genres.id','genres.name']] = movies.genres.apply(pd.Series)
    movies.drop('genres', axis=1, inplace=True)
    movies = pd.DataFrame(movies.reset_index(drop=True))
    
    ## Code must contain SQL query for gathering `Movie Genre Details:revenue by genre by year` with your data model
    genre = ps.sqldf("select year, `genres.name`, sum(revenue), sum(budget), sum(profit) from movies group by year, `genres.name`")

    ## Breaking some sql out to see the window functions here against the 
    count_genre = ps.sqldf("select year, `genres.name` as genre, count(*) count_release from movies group by year, `genres.name`")
    top_genre = ps.sqldf("select year, genre, count_release from" +  
                            "(" +
                                "select year, genre, count_release, row_number() OVER (partition by year order by count_release desc) as rn from count_genre" +
                            ")a where rn = 1")
    
    ##pandas to csv
    genre.to_csv("movies_analysis/data/genre_details.csv",  index=False)
    top_genre.to_csv("movies_analysis/data/genre_top.csv",  index=False)