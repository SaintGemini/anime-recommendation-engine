# Project Definition
## Project Overview
I've always disliked the recommendations that Crunchyroll has given me when searching for a new anime show to watch. Most of their recommendations are for new shows that do not have a big following. I wanted to use what I learned about creating recommendation engines to build my own. The goal of this project is to build a web app that will allow a user to create an account and get personalized recommendations ***based on their favorite animes***. The data I used was scrapped from MyAnimeList.net which is a popular review site for all things anime. More information and a link to the original data set can be found on the "Special Shoutout" section of this README.

## Project Statement
Creating the three types of filters for recommendation engines (Knowledge, Content and Collaborative) will solve the problem. Basic pandas manipulations to filter by genre and date will be enough to complete knowledge based recs. For content and collaborative based filtering, some of the concepts that were taught in the Recommendations with IBM could help complete these filters. For content based recs, calculating the similarity between any two pair of shows and putting that result in a matrix will provide a way to find similar shows based on a given shows attribute. For collaboritve based filtering, a user-item matrix needs to be created. This user-item matrix will be used in the same context as the Recs. with IBM project. The user-item matrix will provide the most similar users and from there the web app will grab their favorite shows. Each filter will return the recommendation based on rank.

## Metrics
Rank accuracy is how the recommendation system is measured. Metrics like accuracy cannot be used since I am not using a machine learning model (my computer kept crashing when trying to implement SVD or FunkSVD with such big datasets). To see if the recommendation engine is working correctly, each filter will have to return recommendations with higher ranked/rated shows first. For content based filtering, the recommendations returned will be of the same genre and in the same general area in rank (preferably higher). For collaborative filtering, the recommendations returned will be shows similar in genre, rank OR rating. The goal of the collaborative filtering is to not only find shows similar in genre or rank but shows outside of the users favorited list that were recieved well by similar fans.

# Analysis
## Data Exploration and Data Visualization
This section is found in the Jupyter NoteBook and goes into great detail! Go there to check it out! Also check the methodology section below for a short summary.

# Methodology
## Data Preprocessing - Implementation
***Full*** details of the data preprocessing and implementation is in the Jupyter Notebook with the data exploration and data visualization. Please see notebook for details. I separated the Jupyter notebook into three sections (Knowledge Based, Content Based, Collaborative Based) and grouped the Analysis and Methodology sections together. A short summary is provided below.
- Section 1 is about knowledge based recommendations. Data exploration, visualization, preprocessing and implementation are grouped in this section.
  - After looking at the data, the first thing I had to do was separate the 'genre' column to find what genres shows belonged to and create an easy way to filter through shows by genre.
  - I then had to extract the original air dates of each show so I can separate shows into decades. I chose to group by decades because as a fan, I know that specific decades bring different animation styles and different types of storytelling. The 'aired' column was a mix of different formats so after trial and error I made a function that could extract the original air dates.
  - That's all of the preprocessing needed for knowledge based filtering. So next I had to create the functions for knowledge based recommendations. I created a function that returns all shows in order based on rank. Then I needed two functions that would filter shows based on genre or decade and return shows in order of highest rank.
- Section 2 is about content based recommendations. The only preprocessing needed was creating a matrix with the anime shows as the index and genres/decades as the columns. A 1 is in a cell if that show belongs to the genre/decase, 0 otherwise. This matrix contains all the attributes for every show in the animes.csv file. All that needed to be done was to take a subset of the animes dataframe from section 1 to get this attribute matrix. Then by taking the dot product of the attribute matrix with its transpose I would get a similarity matrix (the similarity between any two shows). This similarity matrix is what is needed for content based recommendations.
  - The first thing done was getting a subet of the animes dataframe to get the attribute matrix and take the dot product of the attribute matrix with its transpose. This returned a similarity matrix.
  - Next was creating a function to return similar shows (return anime show ids) based on any given show. Finding the cells with the higher numbers (higher similarities) in the similarity matrix would give me the similar shows I needed.
- Section 3 is about collaborative based recommendations. This section I spent the most time on because I tried to implement SVD and FunkSVD. My computer kept crashing and throwing memory errors so I decided not to pursue a model based web app. Thankfully there was a more simplistic approach similar to the Recommendaitons with IBM project. This involves creating a user-item matrix and finding similar users using matrix factorization. After some trial and error, I chose to use the profiles.csv file to create my user-item matrix. I used all of the shows that users have favorited as a guide.
  - Similar to how I had to separate the genres/decades in the animes dataframe, I had to separate the 'favorites_anime' column of the users dataframe with a 1 in a cell if a user has favorited an anime, 0 otherwise.
  - Using a subset of the users dataframes where users were the index and anime shows were the columns, I created a user-item matrix.
  - I then created a function that finds similar users given a user id and a function that gets the anime shows those similar users have favorited.
  - Finally I put together the two functions from above to create a function that gives a user recommendations based on what other similar users have favorited.
 
## Refinement
The algorithms used did not need much refinement. The similarity matrix and user-item matrix were easy and straightforward to work with. What needed refinement was the data itself. The original datasets were so large that it took too long to read in and manipulate the data. Starting the Flask app was another issue as it would take up to 3 minutes just to read in the similarity and user-item matrix. Initially I would get Memory Erors in the Jupyter Notebook that not enough space could be allocated for the datasets. Creating the similarity and user-item matrix would be impossible because of this. I knew this would not perform well and would be a burden to the graders so I chose to work with a subset of the animes.csv data instead. This greatly improved loading time of the Flask app and did not change the quality of the recommendations given.

# Results
## Model Evaluation and Validation
A model was not used for this project. I originally tried to implement SVD and FunkSVD but my computer kept crashing. I took a different approach and used basic matrix manipulation. The only section that really needed this was the Collaborative Based Recommendations. This section was similar to 'User-User Based Collaborative Filtering' section of the Recommendations with IBM project. This project has a slight advantage to the other tho. In the IBM project a 1 in the cell of the user-item matrix represents a user has interacted with an article. It was not known wether the interaction was positive or negative. This project on the other hand has a 1 in the cell of the user-item matrix that represents a ***positive*** interaction with an anime show. It's the most positive an interaction can be (to add a show to your favorites list). So finding similar users is based on favorite shows which means similar users have the same taste. With that, I could be confident that the recommendations given through collaborative filtering were of good quality.

## Justification
The reason a model wasn't used is clear. I think that the recommendations that ***could*** be given if I could perform SVD would be better than what it is currently and that is something I would love to do in the future. As an anime fan I could see that the recommendation given through collaborative filtering were accurate. I made an account and added my favorite animes to my favorited list. The collaborative recs given were shows that were actually recommended to me in real life by other anime fans.


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

