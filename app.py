from flask import Flask, redirect, render_template, request, flash, session
import pandas as pd
import numpy as np
import collab_filter as clb_flt
import filter as flt
import content_filter as cont_flt
import pymysql as sql
import hashlib
import random
from datetime import timedelta


# create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'el rata alada'
app.permanent_session_lifetime = timedelta(hours=3)

# set up database
db = sql.connect(host='database-anime-1.c3v8mzuixvpi.us-east-2.rds.amazonaws.com', user='admin', password='animerds', port=3306)
cursor = db.cursor()

def create_table():
    query = 'CREATE TABLE IF NOT EXISTS database_anime.users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE, password VARCHAR(255), watched VARCHAR(10000))'
    cursor.execute(query)

create_table()

# data for easy filtering
animes_df = pd.read_csv('data/animes-clean.csv')
animes_df = animes_df.drop(['Unnamed: 0'], axis=1)
genres = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']
decades = ['Pre 1970s', '1970s', '1980s', '1990s', '2000s', '2010s']

# create dot product dataframe used for content based filtering
dot_prod_shows_df = pd.read_csv('data/similar-shows.csv')
dot_prod_shows_df = dot_prod_shows_df.drop(['Unnamed: 0'], axis=1)

# load user item matrix for collaborative filtering
user_item = pd.read_csv('./data/user-item-matrix.csv')
user_item_matrix = user_item.drop(['Unnamed: 0'], axis=1)

# create top rated recommendations to populate home page
top_rated = flt.get_top_rated(40, animes_df)
historical_top_rated = flt.get_top_rated_genre('Historical', 80, animes_df)
action_top_rated = flt.get_top_rated_genre('Action', 80, animes_df)
romance_top_rated = flt.get_top_rated_genre('Romance', 80, animes_df)
old_top_rated = flt.get_top_rated_decade('Pre 1970s', 80, animes_df)

'''
---------- Start of routes ----------
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Load home page and get content/collaborative recommendations
    if user is logged in
    '''
    # variables for personal recommendations
    similar_shows = []
    similar_usr_recs = []
    show_name = ''

    # if user is logged in
    if 'user' in session:
        # if content based recs can be calculated
        if 'content-flt' in session:
            fav_shows = clb_flt.split_shows(session['favorite_shows'])
            show_id = random.choice(fav_shows)
            show_name = flt.get_show_by_id(show_id, animes_df).values[0]
            similar_shows = cont_flt.find_similar_shows(int(show_id), animes_df, dot_prod_shows_df)

            # collaborative based recs
            for anime_id in session['collab-flt']:
                similar_usr_recs.append(clb_flt.get_anime_by_id(anime_id, animes_df))

    # if searching anime by filter
    if request.method == 'POST':
        req = request.form['usr-filter']      
        return redirect('/results/'+req)

    return render_template('index.html', similar_usr_recs = similar_usr_recs, show_name=show_name, similar_shows=similar_shows, top_rated=top_rated, action=action_top_rated, romance=romance_top_rated, historical=historical_top_rated, old=old_top_rated, genres=genres, decades=decades)

@app.route('/results/<req>', methods=['GET', 'POST'])
def results(req):
    '''
    Load results of filter (the button on the nav bar)
    '''
    if request.method == 'POST':
        req = request.form['usr-filter']
        return redirect('/results/'+req)

    # get the top rated shows
    top_rated_by_flt = get_top_rated_by_flt(req=req)
    return render_template('results.html', req=req,  genres=genres, decades=decades, top_rated=top_rated_by_flt)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
        '''
        Validate sign up user input.
        '''
        if request.method == 'POST':
            # get user input
            username = request.form['username']
            password = request.form['password']
            pass_confirm = request.form['password-confirm']

            # check to see if username is already taken
            query = 'SELECT * FROM database_anime.users WHERE username = (%s)'
            cursor.execute(query,(username))
            data = cursor.fetchone()

            # if username is available
            if data is None:
                usr_len = len(username)
                pass_len = len(password)
                # if username/password is too short or long
                if usr_len < 5 or usr_len > 20:
                    flash('Username must be between 5 and 20 characters.', category='error')
                elif pass_len < 8 or pass_len > 22:
                    flash('Password must be between 8 and 22 characters.', category='error')
                # if non alphanumeric characters were used
                elif not username.isalnum() or not password.isalnum():
                    flash('Username/Password most only contain letters and numbers.', category='error')
                # if passwords do not match
                elif password != pass_confirm:
                    flash('Password does not match!', category='error')
                # if everything checks out, create account
                else:
                    query = 'INSERT INTO database_anime.users (username, password) VALUES (%s, %s)'
                    hash_pass = create_hash_password(password=password)
                    vals = (username, hash_pass)
                    cursor.execute(query, vals)
                    db.commit()
                    flash('Account Created!', category='success')
             # if username is not available       
            else:
                flash('Username already taken. Try another one.', category='error')

        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
    '''
    validate login input from user.
    '''
    global user_item_matrix
    flash('Loading personal recommendations might take a minute.', category='success')
    # if user already logged in, redirect to home
    if 'user' in session:
        return redirect('/')

    if request.method == 'POST':
            username = request.form['username']          
            password = request.form['password']
            hash_pass = create_hash_password(password=password)

            query = 'SELECT * FROM database_anime.users WHERE username = (%s)'
            cursor.execute(query,(username))
            user = cursor.fetchone()

            if user == None:
                flash('Username not recognized', category='error')

            elif username == user[1] and hash_pass == user[2]:
                # load username and favorited shows to session data
                session.permanent = True
                session['user'] = username
                session['favorite_shows'] = user[3]

                # if no favorite shows
                if session['favorite_shows'] == None:
                    flash('Add some shows to your favorites to get personal recommendations!', category='success')
                    session['favorite_shows'] = ''

                # if 3 or more favorited shows, allow content/collab filtering on home page
                if len(session['favorite_shows']) > 2:
                    session['content-flt'] = True

                    # load user data into the user item matrix
                    fav_shows = clb_flt.split_shows(session['favorite_shows'])
                    last_row = len(user_item_matrix['1'])
                    user_item_matrix.loc[last_row] = clb_flt.add_user_to_user_item(fav_shows, user_item_matrix)

                    # get collaborative recs, save in session data
                    usr_recs = clb_flt.user_user_recs(last_row, 20, user_item=user_item_matrix)
                    session['collab-flt'] = [str(w) for w in usr_recs]

                    # remove user data from user item matrix
                    user_item_matrix.drop(last_row)

                    flash('Log back in after adding shows to your favorites to see updated recommendations after!', category='success')
                return redirect('/')

            # if error with user input
            else:
                flash('Username or password is incorrect', category='error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    '''
    Remove all session data
    '''
    session.pop('user', None)
    session.pop('favorite_shows', None)
    session.pop('content-flt', None)
    session.pop('collab-flt', None)
    
    return redirect('/')



@app.route('/show-info/<show_name>', methods=['GET', 'POST'])
def show_info(show_name):
    '''
    Load show data for page. Add/Remove from user favorites.
    '''
    if request.method == 'POST':
        # if adding or removing show from favorites
        if request.form.get('usr-filter') == None:
            # if removing
            if request.form.get('add-to-favorite') == None:
                show_id = request.form['remove-favorite']
                #clb_flt.remove_from_fav(show_id, int(session['uid']), user_item)
                show_id = '|' + show_id
                session['favorite_shows'] = session['favorite_shows'].replace(show_id, '')

                query = 'UPDATE database_anime.users SET watched = %s WHERE username = %s'
                vals = (session['favorite_shows'], session['user'])
                cursor.execute(query, vals)
                db.commit()
                flash('Show removed from favorites', category='success')
                return redirect('/show-info/'+show_name)
            # if adding
            else:
                show_id = request.form['add-to-favorite']
                #clb_flt.add_to_fav(show_id, int(session['uid']), user_item)
                query = 'UPDATE database_anime.users SET watched = %s WHERE username = %s'
                session['favorite_shows'] = session['favorite_shows'] + '|' + show_id
                vals = (session['favorite_shows'], session['user'])
                cursor.execute(query, vals)
                db.commit()
                flash('Show added to favorites', category='success')
                return redirect('/show-info/'+show_name)

        # if searching for more shows by filter button
        if request.form.get('add-to-favorite') == None and request.form.get('remove-favorite') == None:
            req = request.form['usr-filter']
            return redirect('/results/'+req)
            
    # True - show 'add to favorites' button
    # False - show 'remove from favorites' button
    fav_btn = True

    # get show info
    show = flt.get_show_by_name(show_name=show_name, df=animes_df)

    if 'user' in session:
        fav_shows = clb_flt.split_shows(session['favorite_shows'])
        # if show in favorites, show remove button
        if str(show[1]) in fav_shows:
            fav_btn = False

    return render_template('show_info.html',  genres=genres, decades=decades, show=show, fav_btn=fav_btn)


'''
---------- End routes ----------
'''



'''
---------- Small helper functions ----------
'''

def get_top_rated_by_flt(req):
    '''
    Find what filter the usr chose and get the top rated
    shows in that genre.
    '''
    if req in genres:
        top_rated_by_filter = flt.get_top_rated_genre(req, 100, animes_df)
    else:
        top_rated_by_filter = flt.get_top_rated_decade(req, 100, animes_df)
    return top_rated_by_filter

def create_hash_password(password):
    '''
    Use hashlib library to has a password that will be 
    put in database.
    '''
    salt = 'ra30a'
    db_password = salt + password
    return hashlib.md5(db_password.encode()).hexdigest()

'''
---------- End helper functions ----------
'''

if __name__ == "__main__":

    app.run(debug=True)