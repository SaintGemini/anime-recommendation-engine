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
    
    try:
        for i in range(n):
            recs.append((genre_df.iloc[i].title, genre_df.iloc[i].img_url))
    except:
        for i in range(len(genre_df['title'])):
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
    Gets the row of info about an anime by name.

    INPUT:
    show_name - a string of the anime title
    df - the clean animes df in the data directory

    OUTPUT:
    show.iloc[0] - the entire row in the df with all the show info
    '''
    show = df[df['title'] == show_name]
    return show.iloc[0]

def get_show_by_id(anime_id, df):
    '''
    INPUT:
    show_name - a string of the anime title
    df - the clean animes df in the data directory

    OUTPUT:
    show.iloc[0] - the entire row in the df with all the show info
    '''
    show = df[df['uid'] == int(anime_id)]['title']
    return show