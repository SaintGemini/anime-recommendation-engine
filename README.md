# Anime Recommendation Engine
I've always disliked the recommendations that Crunchyroll has given me when searching for a new anime show to watch. Most of their recommendations are for new shows that do not have a big following. I wanted to use what I learned about creating recommendation engines to build my own. The goal of this project is to build a web app that will allow a user to create an account and get personalized recommendations <u>based on their favorite animes</u>. The data I used was scrapped from MyAnimeList.net which is a popular review site for all things anime. More information and a link to the original data set can be found on the "Special Shoutout" section of this README.

## Special Shoutout
A big thanks to MARLESSON for scraping the data from MyAnimeList.net and putting the data on Kaggle. Original datasets can be found here: <br>
https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews

## Python Libraries Used
Flask, Pandas, Numpy, PyMySQL, Hashlib, DateTime

## How to Install Libraries
- pip3 install Flask
- pip3 install pandas
- pip3 install numpy
- pip3 install pymysql
- *** hashlib apart of python standard library, no need to install ***
- *** datetime apart of python standard library, no need to install ***

## Python Version Used
*** python 3.10.2 ***

## File Descriptions
- data (Directory that holds the csv files used for project.)
  -  animes-clean.csv (Clean csv file generated after data prep and cleaning holding data about all anime shows.)
  -  animes.csv (Original csv apart of dataset used from Kaggle.)
  -  profiles.csv (Original csv apart of dataset used from Kaggle. Holds all data about each user profile.)
  -  reviews.csv (Original csv apart of dataset used from Kaggle. Holds all data about each review on MyAnimeList.net)
  -  similar-shows.csv (A matrix where the similarity of any two shows have been computed. The higher the number in a cell, the more similar two shows are. More info about this csv file can be found in the juypter notebook for data preparation. Used for content based recommendations.)
  -  user-item-matrix.csv (Users are the index and shows are the columns. A matrix of 1's and 0's where a 1 represents a user favorited an anime, 0 otherwise. Used to find user collaborative based recommendations.)
- static/stylesheets (Directory holding all of the css files for the web app.)
- templates (Directory holding all of the html pages for the web app.)
- anime_users.db (Database holding the users for the web app. Connected to Amazon RDS database.)
- app.py (The main application file that will run the Flask app.)
- collab_filter.py (Python file holding all functions used for collaboritve filtering.)
- content_filter.py (Python file holding all functions used for content based filtering.)
- data-preparation.ipynb (Jupyter notebook that goes through data preparation and cleaning.)
- filter.py (Python file that holds basic ranked based filtering functions.)


## Analysis
The dataset taken from Kaggle made knowledge and content based recommendations straightforward. Using the matrix that calculates the similarity between any two shows (similar-shows.csv), content based recommendations are of high quality. The first two types of filtering were easy considering I just finished the Recommendations with IBM project for this course. The real difficulty of this project began with collaborative based filtering. In the jupyter notebook, the matrices I tried to create (similar-shows and the user-item-matrix) were causing memory errors because they were so big. This was the first time I was dealing with data over 1GB. I decided not to use SVD or Funk SVD because of these Memory Errors that kept coming up. I implemented a version of User-User Based Collaborative Filtering like in Part 3 of the Recommendations with IBM project. This type of collaborative filtering was easy on my computer and gave good results. I was only limited by the capability of my compter so I hope to implement a version of SVD in the future.

## Conclusion
Overall the recommendations given by the web app were good. As an anime fan I can say that the recommendations were what I was looking for. It would have been easier to evaluate the recommendations if I used a model, but my computer is not strong enough. The recommendations given were not like Crunchroll. The recommendations are based on what was higher rated and ranked and what was better recieved by the fans.

## Possible errors when running Jupyter notebook
If running through the Jupyter notebook, please note that when trying to create the dot_prod_shows or the user_item_matrix pandas dataframes you might get the following error <br>
MemoryError: Unable to allocate X.XX GiB for an array with shape (X, Y) and data type float64 <br>
I found the solution at this link and it would be worth reading through BEFORE running cells in the notebook:<br>
https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type
