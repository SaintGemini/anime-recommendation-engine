# Project Definition
## Problem Overview
I've always disliked the recommendations that Crunchyroll has given me when searching for a new anime show to watch. Most of their recommendations are for new shows that do not have a big following. I wanted to use what I learned about creating recommendation engines to build my own. The goal of this project is to build a web app that will allow a user to create an account and get personalized recommendations ***based on their favorite animes***. The data I used was scrapped from MyAnimeList.net which is a popular review site for all things anime. More information and a link to the original data set can be found on the "Special Shoutout" section of this README.

## Problem Statement
Creating the three types of filters for recommendation engines (Knowledge, Content and Collaborative) will solve the problem. Basic pandas manipulations to filter by genre and date will be enough to complete knowledge based recs. For content and collaborative based filtering, some of the concepts that were taught in the Recommendations with IBM could help complete these filters. For content based recs, calculating the similarity between any two pair of shows and putting that result in a matrix will provide a way to find similar shows based on a given shows attribute. For collaboritve based filtering, a user-item matrix needs to be created. This user-item matrix will be used in the same context as the Recs. with IBM project. The user-item matrix will provide the most similar users and from there the web app will grab their favorite shows. Each filter will return the recommendation based on rank.

## Metrics
Rank accuracy is how the recommendation system is measured. Metrics like accuracy cannot be used since I am not using a machine learning model (my computer kept crashing when trying to implement SVD or FunkSVD with such big datasets). To see if the recommendation engine is working correctly, each filter will have to return recommendations with higher ranked/rated shows first. For content based filtering, the recommendations returned will be of the same genre and in the same general area in rank (preferably higher). For collaborative filtering, the recommendations returned will be shows similar in genre, rank OR rating. The goal of the collaborative filtering is to not only find shows similar in genre or rank but shows outside of the users favorited list while still recommending high rated/ranked shows, regardless of genre.

# Analysis
## Data Exploration and Data Visualization
This section is found in the Jupyter NoteBook and goes into great detail! Go there to check it out!

# Methodology - Results
## These sections not required for web app project.
Per the rubric, "If you submit a web application, you only need to submit a link to your Github repository. In this case, since you won't be writing up a separate report, you need to make sure to address the Project Definition, Analysis, and Conclusion sections of the rubric in your README file, or in your Jupyter Notebook if you provide one."

<img width="620" alt="image" src="https://user-images.githubusercontent.com/28576229/166078726-01aaf360-9419-4eec-a187-14a3b8316817.png">


# Conclusion
## Reflection
The dataset taken from Kaggle made knowledge and content based recommendations straightforward. Using the matrix that calculates the similarity between any two shows (similar-shows.csv), content based recommendations are of high quality. The first two types of filtering were easy considering I just finished the Recommendations with IBM project for this course. The real difficulty of this project began with collaborative based filtering. In the jupyter notebook, the matrices I tried to create (similar-shows and the user-item-matrix) were causing memory errors because they were so big. This was the first time I was dealing with data over 1GB. I decided not to use SVD or Funk SVD because of these Memory Errors that kept coming up. I implemented a version of User-User Based Collaborative Filtering like in Part 3 of the Recommendations with IBM project. This type of collaborative filtering was easy on my computer and gave good results. I was only limited by the capability of my compter so I hope to implement a version of SVD in the future.<br>
Overall the recommendations given by the web app were good. As an anime fan I can say that the recommendations were what I was looking for. It would have been easier to evaluate the recommendations if I used a model, but my computer is not strong enough. The recommendations given were not like Crunchroll and are based on what was higher rated/ranked and what was better recieved by the fans.

## Improvements
Figuring out a way to quickly read in large datasets and manipulate large datasets would help improve this project. The initial start up of reading in the data sets take a few minutes. Another improvement I want to make is implementing SVD. My computer kept crashing when first trying to implement SVD which is why I decided not to pursue a model for this project.


## Special Shoutout
A big thanks to MARLESSON for scraping the data from MyAnimeList.net and putting the data on Kaggle. Original datasets can be found here: <br>
https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews

## Libraries Used
Flask, Pandas, Numpy, PyMySQL, Hashlib, DateTime, Bootstrap, git-lfs

## SPECIFIC INSTALLATION REQUIRED
To successfully clone and run this project on localhost, git-lfs (githubs large file storage) needs to be installed. Please follow the link and make sure to download the correct version of git-lfs for your OS BEFORE cloning the project. <br><br>
https://git-lfs.github.com/

## How to Install Libraries
- pip3 install Flask
- pip3 install pandas
- pip3 install numpy
- pip3 install pymysql
- ***hashlib apart of python standard library, no need to install***
- ***datetime apart of python standard library, no need to install***

## Python Version Used
***python 3.10.2***

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



## Possible errors when running Jupyter notebook
If running through the Jupyter notebook, please note that when trying to create the dot_prod_shows or the user_item_matrix pandas dataframes you might get the following error <br><br>
MemoryError: Unable to allocate X.XX GiB for an array with shape (X, Y) and data type float64 <br><br>
I found the solution at this link and it would be worth reading through BEFORE running cells in the notebook:<br>
https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type

## How to clone and run project
REMINDER: You need to have git-lfs installed on your own computer before cloning. When it's installed, make sure all of the other libraries are installed as well.<br><br>
To clone the repository, change directory to Desktop and use the command<br><br>
git clone https://github.com/SaintGemini/anime-recommendation-engine.git <br>
<br>Once the project is cloned, change directory into the 'anime-recommendation-engine' directory using: cd anime-recommendation-engine <br><br>
Run the command: python app.py <br><br>
# Notes:
Please be patient, it will take a few minutes to read in the large csv files, connect to AWS RDS database, do some initial filtering and load the Flask app. Once the app is running, everything is faster. The initial setup will take the longest to load. Loading personal user/collab based recommendations might take a minute when you first log in.

# Some tips for the app
You will need to log out and back in to see the changes to your personal recommendations. Add around 5 anime shows to your favorites for good content based recommendations and around 10 animes for good collaborative based recommendations. <br>
Example: After initially creating your profile, add about 5 shows to your favorites. Log out and back in to see your content based recommendations. Add another 5 shows to your favorites, log out/in to see collaborative filtering. Enjoy the project!

