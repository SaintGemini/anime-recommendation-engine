'''
This file contains all functions that are used in collaborative
filtering.
'''
import random

def split_shows(shows):
    '''
    Used to split the favorited shows of a user that is
    stored in the database.

    INPUT:
    shows - session['favorite_shows'] data

    OUTPUT:
    shows - a list of anime show ids
    '''
    shows = shows.split('|')
    shows.pop(0)
    return shows

def add_user_to_user_item(fav_animes, user_item):
    '''
    Uses a users favorited shows to create a new row
    in the user item matrix. This row will help find
    similar users and their recs.

    INPUT:
    fav_animes - session['favorited_animes'] after calling split_ids (func above)
    user_item - (pandas dataframe) matrix of users by articles: 
                1's when a user has favorited an anime, 0 otherwise

    OUTPUT:
    row - a row of 1's and 0's that will fit in the user item matrix
    '''
    row = []
    for col in user_item.columns:
        if col in fav_animes:
            row.append(1)
        else:
            row.append(0)
    return row

def find_similar_users(user_id, user_item):
    '''
    Computes the similarity of every pair of users based on the dot product
    Returns an ordered list of user ids

    INPUT:
    user_id - (int) the last row (index number) of user item matrix (the current user id)
    user_item - (pandas dataframe) matrix of users by articles: 
                1's when a user has favorited an anime, 0 otherwise
    
    OUTPUT:
    similar_users - (list) an ordered list where the closest users (largest dot product users)
                    are listed first
    '''
    # compute similarity of each user to the provided user
    similarity = user_item[user_item.index == user_id].dot(user_item.T)
    # sort by similarity
    similarity = similarity.sort_values(user_id, axis=1, ascending=False)

    # create list of just the ids
    most_similar_users = list(similarity.columns)
    # remove the own user's id
    most_similar_users.remove(user_id)
    
    return most_similar_users # return a list of the users in order from most to least similar



def get_anime_by_id(anime_id, animes_df):
    '''
    Returns the title and img url of an anime based on 
    anime id.

    INPUT:
    anime_id - (int) the anime id found in the global animed_df
    animes_df - (pandas dataframe) the global dataframe declared
                in app.py
    '''
    anime = animes_df[animes_df['uid'] == int(anime_id)]
    return (anime['title'].values[0], anime['img_url'].values[0])


def get_user_animes(user_id,user_item):
    '''
    Returns all the animes a specific user has favorited.

    INPUT:
    user_id - (int) user id
    user_item - (pandas dataframe) matrix of users by articles: 
                1's when a user has favorited an anime, 0 otherwise

    OUTPUT:
    a list of anime ids (integers)
    '''
    user_row = user_item[user_item.index == user_id]
    user_row = user_row.loc[:, (user_row.sum(axis=0) > 0)]
    return list(user_row.columns.values.astype(int))



def user_user_recs(user_id, m, user_item):
    '''
    Loops through the users based on closeness to the input user_id
    For each user - finds articles the user hasn't seen before and provides them as recs
    Does this until m recommendations are found

    INPUT:
    user_id - (int) a user id
    m - (int) the number of recommendations you want for the user
    
    OUTPUT:
    recs - (list) a list of recommendations for the user
    
    Notes:
    Users who are the same closeness are chosen arbitrarily as the 'next' user
    
    For the user where the number of recommended articles starts below m 
    and ends exceeding m, the last items are chosen arbitrarily
    
    '''

    recs = []
    similar_users = find_similar_users(user_id, user_item)
    random.shuffle(similar_users)
    viewed_anime_ids = get_user_animes(user_id, user_item)
    
    for user in similar_users:
        anime_ids = get_user_animes(user, user_item)
        for anime_id in anime_ids:
            if anime_id in viewed_anime_ids:
                pass
            else:
                recs = list(set().union(recs, anime_ids))
        if len(recs) >= m:
            break
        
    
    return recs[:m]