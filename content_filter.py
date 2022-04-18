'''
This file contains helper functions that will be used for content based filtering
'''
import numpy as np

def find_similar_shows(anime_id, animes_df, dot_prod_show_df):
    '''
    Finds similar shows based on what genres/decades they have in common
    
    INPUT:
    anime_id - int, id of anime show that appears in the animes_df
    animes_df - the clean animes_df in the data directory
    dot_prod_show_df - a dataframe where the dot product of the anime shows 
                       was taken to get a show X show matrix of similarities
    
    OUTPUT:
    similar_shows - pandas dataframe of similar shows sorted by highest rated
    '''
    recs = []

    show_idx = np.where(animes_df['uid'] == anime_id)[0][0]
    
    similar_idxs = np.where(dot_prod_show_df.iloc[show_idx] > np.max(dot_prod_show_df.iloc[show_idx])-2)[0]
    
    similar_shows = animes_df.iloc[similar_idxs, ]
    similar_shows = similar_shows[similar_shows['uid'] != anime_id]
    similar_shows.sort_values(by=['score'], ascending=False)

    for name, img in zip(similar_shows['title'], similar_shows['img_url']):
        recs.append((name, img))
        if len(recs) > 7:
            break
    
    
    return recs

def is_in_favorites(show_id, favorite_shows):
    '''
    Will check if a show is already in favorites

    INPUT:
    show_id - a string of the show id
    favorite_shows - session data (session['favorite_shows']) as a string

    OUTPUT:
    True - if show is already in list of favorites
    False - if show is not in list of favorites
    '''
    if favorite_shows.find(show_id) > 0:
        return True
    return False
