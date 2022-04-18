'''
This file contains helper functions that will be used for content based filtering
'''

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
