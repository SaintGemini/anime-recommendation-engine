# Anime Recommendation Engine

Link to blog post about project: https://medium.com/@chacone96/anime-recommendation-engine-84b3dbe9fdcb

## Project Overview
I've always disliked the recommendations that Crunchyroll, a popular anime streaming site, has given me when searching for a new anime show to watch. Most of their recommendations are for new shows that do not have a big following or they recommend all time highest rated shows that are also recommended on every other platform. I wanted to use what I learned about creating recommendation engines to build my own. This project will be a stepping stone into building (in the future) my own web application that runs off of a FunkSVD model (a machine learning algorithm).

## Special Shoutout
A big thanks to MARLESSON for scraping the data from MyAnimeList.net and putting the data on Kaggle. Original datasets can be found here: <br>
https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews

## Libraries Used
Pandas, Numpy, MatPlotLib, git-lfs

## How to install git-lfs
Git-lfs (git large file storage) is an extension of git that allows large files to be stored on public repositories.

To successfully clone and run the jupyter notebook, git-lfs (githubs large file storage) needs to be installed. Please follow the link and make sure to download the correct version of git-lfs for your OS BEFORE cloning the project. <br><br>
https://git-lfs.github.com/

## How to Install Libraries
- pip3 install pandas
- pip3 install numpy
- pip3 install matplotlib

## Python Version Used
***python 3.10.2***

## File Descriptions
- data (Directory that holds the csv files used for project.)
  -  animes.csv (Original csv apart of dataset used from Kaggle.)
  -  reviews.csv (Original csv apart of dataset used from Kaggle. Holds all data about each review on MyAnimeList.net)
- Anime-Recommendation-Engine.pdf (WriteUp/Documentation for project.)
- recommendation_engine (Jupyter Notebook containing data exploration/visualization, data cleaning/preprocessing, and implementation of recommendation engine.)

## Possible errors when running Jupyter notebook
If running through the Jupyter notebook, please note that you might get the following error <br><br>
MemoryError: Unable to allocate X.XX GiB for an array with shape (X, Y) and data type float64 <br><br>
I found the solution at this link and it would be worth reading through BEFORE running cells in the notebook:<br>
https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type

## How to clone and run project
REMINDER: You need to have git-lfs installed on your own computer before cloning. When it's installed, make sure all of the other libraries are installed as well.<br><br>
To clone the repository, change directory to Desktop and use the command<br><br>
git clone https://github.com/SaintGemini/anime-recommendation-engine.git <br>
<br>Once the project is cloned, change directory into the 'anime-recommendation-engine' directory using: cd anime-recommendation-engine <br><br>
Open the notebook with Jupyter Notebook app. <br><br>
