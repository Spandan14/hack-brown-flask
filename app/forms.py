from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, ArtistReview, AlbumReview, SongReview


class LoginForm(FlaskForm):
    # the validators in the field add special modifiers to those fields
    # without these  successfully completing and not raising any errors
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ArtistReviewForm(FlaskForm):
    artist_id = StringField('Spotify Artist ID', validators=[DataRequired()])
    content = TextAreaField('Review Content', validators=[DataRequired(), Length(min=1, max=20000)])
    submit = SubmitField('Submit')


class AlbumReviewForm(FlaskForm):
    album_id = StringField('Spotify Album ID', validators=[DataRequired()])
    content = TextAreaField('Review Content', validators=[DataRequired(), Length(min=1, max=20000)])
    submit = SubmitField('Submit')


class SongReviewForm(FlaskForm):
    song_id = StringField('Spotify Song ID', validators=[DataRequired()])
    content = TextAreaField('Review Content', validators=[DataRequired(), Length(min=1, max=20000)])
    submit = SubmitField('Submit')

