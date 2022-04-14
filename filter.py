'''
This file contains all of the functions that filter anime shows. 
'''

def get_top_rated(n, df):
    '''
    INPUT:
    n - number of recs to return
    df - the clean animes df in the data directory
    
    OUTPUT:
    recs -  the name and img url of the all time top rated animes
    '''
    recs = []
    top_ranked = df.sort_values(by='ranked', ascending=True).drop_duplicates()
    
    for i in range(n):
        recs.append((top_ranked.iloc[i].title, top_ranked.iloc[i].img_url))
                    
    return recs


def get_top_rated_genre(genre, n, df):
    '''
    INPUT:
    genre - a string containing the genre that will be filtered by
    n - the number of recommendations to be returned
    df - the clean animes df in the data directory
    
    OUTPUT:
    recs - a list of recommendations with title and url link
    '''
    
    recs = []
    genre_df = df[df[genre] == 1].sort_values(by='score', ascending=False).drop_duplicates()
    
    for i in range(n):
        recs.append((genre_df.iloc[i].title, genre_df.iloc[i].img_url))
    
    return recs

def get_top_rated_decade(decade, n, df):
    '''
    INPUT:
    decade - a string containing the decade that will be filtered by
    n - the number of recommendations to be returned
    df - the clean animes df in the data directory
    
    OUTPUT:
    recs - a list of recommendations with title and url link
    '''
    
    recs = []
    decade_df = df[df[decade] == 1].sort_values(by='score', ascending=False).drop_duplicates()
    
    for i in range(n):
        recs.append((decade_df.iloc[i].title, decade_df.iloc[i].img_url))
    
    return recs


def get_show_by_name(show_name, df):
    '''
    Gets all the info about an anime by name.

    INPUT:
    show_name - a string of the anime title
    df - the clean animes df in the data directory

    OUTPUT:
    show.iloc[0] - the entire row in the df with all the show info

    INDEXES AND THEIR MEANING
    0 - the id of the anime
    1 - the title of the anime
    2 - the description of the anime
    3 - the genre the show belongs to
    4 - the aired dates
    5 - the num of episodes
    6 - the number of members in the show group in myanimelist.net
    7 - the popularity of the show
    8 - the rank of the show
    9 - the average rating of the show
    10 - the img_url
    11 - the link to myanimelist.net for the show

    '''
    show = df[df['title'] == show_name]
    return show.iloc[0]