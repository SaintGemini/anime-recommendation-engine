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