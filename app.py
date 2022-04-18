from flask import Flask, redirect, render_template, request, flash, session
import pandas as pd
import filter as flt
import content_filter as cont_flt
from flask_sqlalchemy import SQLAlchemy
import pymysql as sql
import hashlib
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
genres = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']
decades = ['Pre 1970s', '1970s', '1980s', '1990s', '2000s', '2010s']

top_rated = flt.get_top_rated(40, animes_df)

historical_top_rated = flt.get_top_rated_genre('Historical', 40, animes_df)
action_top_rated = flt.get_top_rated_genre('Action', 40, animes_df)
romance_top_rated = flt.get_top_rated_genre('Romance', 40, animes_df)
old_top_rated = flt.get_top_rated_decade('Pre 1970s', 40, animes_df)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req = request.form['usr-filter']      
        return redirect('/results/'+req)

    return render_template('index.html', top_rated=top_rated, action=action_top_rated, romance=romance_top_rated, historical=historical_top_rated, old=old_top_rated, genres=genres, decades=decades)

@app.route('/results/<req>', methods=['GET', 'POST'])
def results(req):
    if request.method == 'POST':
        req = request.form['usr-filter']
        return redirect('/results/'+req)

    top_rated_by_flt = get_top_rated_by_flt(req=req)
    return render_template('results.html', req=req,  genres=genres, decades=decades, top_rated=top_rated_by_flt)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            pass_confirm = request.form['password-confirm']

            query = 'SELECT * FROM database_anime.users WHERE username = (%s)'
            cursor.execute(query,(username))
            data = cursor.fetchone()
            if data is None:
                print(username, password, pass_confirm)
                usr_len = len(username)
                pass_len = len(password)
                if usr_len < 5 or usr_len > 20:
                    flash('Username must be between 5 and 20 characters.', category='error')
                elif pass_len < 8 or pass_len > 22:
                    flash('Password must be between 8 and 22 characters.', category='error')
                elif not username.isalnum() or not password.isalnum():
                    flash('Username/Password most only contain letters and numbers.', category='error')
                elif password != pass_confirm:
                    flash('Password does not match!', category='error')
                else:
                    query = 'INSERT INTO database_anime.users (username, password) VALUES (%s, %s)'
                    hash_pass = create_hash_password(password=password)
                    vals = (username, hash_pass)
                    cursor.execute(query, vals)
                    db.commit()
                    flash('Account Created!', category='success')
                    
            else:
                flash('Username already taken. Try another one.', category='error')

        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
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
                session.permanent = True
                session['user'] = username
                session['favorite_shows'] = user[3]
                if session['favorite_shows'] == None:
                    session['favorite_shows'] = ''
                return redirect('/')
            else:
                flash('Username or password is incorrect', category='error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('favorite_shows', None)
    return redirect('/')



@app.route('/show-info/<show_name>', methods=['GET', 'POST'])
def show_info(show_name):
    if request.method == 'POST':
        # if adding or removing show from favorites
        if request.form.get('usr-filter') == None:
            # if removing
            if request.form.get('add-to-favorite') == None:
                show_id = '|' +request.form['remove-favorite']
                session['favorite_shows'] = session['favorite_shows'].replace(show_id, '')

                query = 'UPDATE database_anime.users SET watched = %s WHERE username = %s'
                vals = (session['favorite_shows'], session['user'])
                cursor.execute(query, vals)
                db.commit()
                flash('Show removed from favorites', category='success')
                return redirect('/show-info/'+show_name)
            # if adding
            else:
                query = 'UPDATE database_anime.users SET watched = %s WHERE username = %s'
                session['favorite_shows'] = session['favorite_shows'] + '|' + request.form['add-to-favorite']
                vals = (session['favorite_shows'], session['user'])
                cursor.execute(query, vals)
                db.commit()
                flash('Show added to favorites', category='success')
                return redirect('/show-info/'+show_name)

        if request.form.get('add-to-favorite') == None and request.form.get('remove-favorite') == None:
            req = request.form['usr-filter']
            return redirect('/results/'+req)
            
    
    fav_btn = True
    show = flt.get_show_by_name(show_name=show_name, df=animes_df)

    if 'user' in session:
        if cont_flt.is_in_favorites(str(show[1]), session['favorite_shows']):
            fav_btn = False

    return render_template('show_info.html',  genres=genres, decades=decades, show=show, fav_btn=fav_btn)



def get_top_rated_by_flt(req):
        if req in genres:
            top_rated_by_filter = flt.get_top_rated_genre(req, 50, animes_df)
        else:
            top_rated_by_filter = flt.get_top_rated_decade(req, 50, animes_df)
        return top_rated_by_filter

def create_hash_password(password):
    salt = 'ra30a'
    db_password = salt + password
    return hashlib.md5(db_password.encode()).hexdigest()

if __name__ == "__main__":

    app.run(debug=True)