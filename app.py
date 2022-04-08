from flask import Flask, render_template, request
import pandas as pd
import filter as flt

animes_df = pd.read_csv('data/animes-clean.csv')
genres = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']
decades = ['Pre 1970s', '1970s', '1980s', '1990s', '2000s', '2010s']

app = Flask(__name__)



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

if __name__ == "__main__":
    app.run(debug=True)