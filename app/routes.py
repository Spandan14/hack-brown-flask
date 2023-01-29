from flask import render_template, flash, redirect, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app import app, db  # import instance of Flask class
from app.forms import LoginForm, RegistrationForm, ArtistReviewForm, AlbumReviewForm, SongReviewForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, ArtistReview, AlbumReview, SongReview
from werkzeug.urls import url_parse

cid = '96132db6fb1845b7bf44a382863d6b41'  # CLIENT ID
secret = 'f41e8c7aadb24543a0f9f572b7a9078e'  # CLIENT SECRET

# these next two lines will establish our Spotify object
# that will let us make API calls to gather data
client_cred_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_cred_manager)


@app.route('/artist/<artist_id>')
def artist(artist_id):
    api_data = sp.artist(artist_id=artist_id)  # API call is made here
    sp.artist_albums(artist_id=artist_id)
    return render_template('artist.html', artist=api_data)


@app.route('/login', methods=['GET', 'POST'])  # add HTTP methods
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # check to make sure user with username doesn't exist
        user = User.query.filter_by(username=login_form.username.data).first()
        # if user is not active or has the incorrect password
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid username or password")
            return redirect('/login')

        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = redirect('/index')
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=login_form)


@app.route('/')
@app.route('/index')
def home():
    artist_reviews = ArtistReview.query.all()
    album_reviews = AlbumReview.query.all()
    song_reviews = SongReview.query.all()
    return render_template('index.html', artist_reviews=artist_reviews,
                           album_reviews=album_reviews, song_reviews=song_reviews)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('index')
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have registered for Spotify Reviews!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=register_form)


@app.route('/review_artist', methods=['GET', 'POST'])
@login_required
def review_artist():
    artist_form = ArtistReviewForm()
    if artist_form.validate_on_submit():
        try:
            api_data = sp.artist(artist_form.artist_id.data)
            review = ArtistReview(content=artist_form.content.data, artist_id=api_data['name'], author=current_user)
            db.session.add(review)
            db.session.commit()
            flash('Review Submitted Successfully!')
            return redirect('/index')
        except spotipy.SpotifyException:
            flash("Invalid Spotify Artist ID")
            return redirect('/review_artist')
    return render_template('artist_form.html', title='Artist Review', form=artist_form)


@app.route('/review_album', methods=['GET', 'POST'])
@login_required
def review_album():
    album_form = AlbumReviewForm()
    if album_form.validate_on_submit():
        try:
            api_data = sp.album(album_form.album_id.data)
            review = AlbumReview(content=album_form.content.data, album_id=api_data['name'],
                                  artist_id=api_data['artists'][0]['name'], author=current_user)
            db.session.add(review)
            db.session.commit()
            flash('Review Submitted Successfully!')
            return redirect('/index')
        except spotipy.SpotifyException:
            flash("Invalid Spotify Album ID")
            return redirect('/review_album')
    return render_template('album_form.html', title='Album Review', form=album_form)


@app.route('/review_song', methods=['GET', 'POST'])
@login_required
def review_song():
    song_form = SongReviewForm()
    if song_form.validate_on_submit():
        try:
            api_data = sp.track(song_form.song_id.data)
            review = SongReview(content=song_form.content.data, song_id=api_data['name'],
                                 album_id=api_data['album']['name'],
                                 artist_id=api_data['artists'][0]['name'], author=current_user)
            db.session.add(review)
            db.session.commit()
            flash('Review Submitted Successfully!')
            return redirect('/index')
        except spotipy.SpotifyException:
            flash("Invalid Spotify Track ID")
            return redirect('/review_song')
    return render_template('song_form.html', title='Song Review', form=song_form)
