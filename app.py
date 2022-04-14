from flask import Flask, redirect, render_template, request, flash, sessions
import pandas as pd
import filter as flt
from flask_sqlalchemy import SQLAlchemy
import pymysql as sql
import hashlib
from os import path


# create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'el rata alada'

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

top_rated = flt.get_top_rated(10, animes_df)

historical_top_rated = flt.get_top_rated_genre('Historical', 10, animes_df)
action_top_rated = flt.get_top_rated_genre('Action', 10, animes_df)
romance_top_rated = flt.get_top_rated_genre('Romance', 10, animes_df)
old_top_rated = flt.get_top_rated_decade('Pre 1970s', 10, animes_df)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        req = request.form['usr-filter']
        if req in genres:
            top_rated_by_filter = flt.get_top_rated_genre(req, 50, animes_df)
        else:
            top_rated_by_filter = flt.get_top_rated_decade(req, 50, animes_df)

        return render_template('results.html',  genres=genres, decades=decades, req=req, top_rated=top_rated_by_filter)
    return render_template('index.html', top_rated=top_rated, action=action_top_rated, romance=romance_top_rated, historical=historical_top_rated, old=old_top_rated, genres=genres, decades=decades)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        req = request.form['usr-filter']
        if req in genres:
            top_rated_by_filter = flt.get_top_rated_genre(req, 50, animes_df)
        else:
            top_rated_by_filter = flt.get_top_rated_decade(req, 50, animes_df)

        return render_template('results.html',  genres=genres, decades=decades, req=req, top_rated=top_rated_by_filter)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            pass_confirm = request.form['password-confirm']

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
                salt = 'ra30a'
                db_password = salt + password
                hash_pass = hashlib.md5(db_password.encode()).hexdigest()
                vals = (username, hash_pass)
                cursor.execute(query, vals)
                db.commit()
                flash('Account Created! Head over to the login page!', category='success')

        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
            username = request.form['username']
            
            password = request.form['password']
            salt = 'ra30a'
            db_password = salt + password
            hash_pass = hashlib.md5(db_password.encode()).hexdigest()

            query = 'SELECT username, password from database_anime.users'
            cursor.execute(query)
            data =  cursor.fetchall()
            user_input = (username, hash_pass)
            if user_input in data:
                return redirect('/')
            else:
                flash('Username or password is incorrect', category='error')
    return render_template('login.html',  genres=genres, decades=decades)


@app.route('/show-info/<show_name>', methods=['GET', 'POST'])
def show_info(show_name):
    if request.method == 'POST':
        req = request.form['usr-filter']
        if req in genres:
            top_rated_by_filter = flt.get_top_rated_genre(req, 50, animes_df)
        else:
            top_rated_by_filter = flt.get_top_rated_decade(req, 50, animes_df)

        return render_template('results.html',  genres=genres, decades=decades, req=req, top_rated=top_rated_by_filter)

    show = flt.get_show_by_name(show_name=show_name, df=animes_df)
    print(show)
    return render_template('show_info.html',  genres=genres, decades=decades, show=show)


if __name__ == "__main__":

    app.run(debug=True)